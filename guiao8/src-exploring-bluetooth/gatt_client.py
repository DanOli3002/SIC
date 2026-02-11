#!/usr/bin/env python3
import sys
import threading
import dbus
import dbus.mainloop.glib
from gi.repository import GLib

BLUEZ_SERVICE_NAME = 'org.bluez'
DBUS_OM_IFACE = 'org.freedesktop.DBus.ObjectManager'
DBUS_PROP_IFACE = 'org.freedesktop.DBus.Properties'
GATT_SERVICE_IFACE = 'org.bluez.GattService1'
GATT_CHRC_IFACE = 'org.bluez.GattCharacteristic1'
DEVICE_IFACE = 'org.bluez.Device1'

# Must match the server
CHAT_SERVICE_UUID = '12345678-1234-5678-1234-56789abcdef0'
CHAT_MSG_UUID = '12345678-1234-5678-1234-56789abcdef1'

def find_chat_characteristic(bus, adapter):
    obj = bus.get_object(BLUEZ_SERVICE_NAME, '/')
    manager = dbus.Interface(obj, DBUS_OM_IFACE)
    objects = manager.GetManagedObjects()

    target_service_path = None
    target_device_path = None
    target_char_path = None

    for path, ifaces in objects.items():
        svc = ifaces.get(GATT_SERVICE_IFACE)
        if svc is not None:
            uuid = str(svc.get('UUID'))
            if uuid.lower() == CHAT_SERVICE_UUID.lower():
                target_service_path = path
                # GattService1 typically has a 'Device' property on some setups; otherwise the Device is implied
                # Some BlueZ versions expose 'Device' on service, others do not. Try to find device owning the service.
                target_device_path = svc.get('Device') if 'Device' in svc else None
                break

    if not target_service_path:
        print('Chat service UUID not found in managed objects')
        return None, None, None

    # find characteristic under service
    for path, ifaces in objects.items():
        ch = ifaces.get(GATT_CHRC_IFACE)
        if ch is not None:
            if str(ch.get('Service')) == target_service_path and str(ch.get('UUID')).lower() == CHAT_MSG_UUID.lower():
                target_char_path = path
                # Get device property maybe from parent service if missing
                if not target_device_path:
                    # try walking parents: service object may have a 'Device' property elsewhere
                    svc_iface = objects.get(target_service_path)
                    if svc_iface:
                        svc_props = svc_iface.get(GATT_SERVICE_IFACE, {})
                        target_device_path = svc_props.get('Device')
                break

    return target_device_path, target_service_path, target_char_path

def on_props_changed(interface, changed, invalidated, path):
    # This handler will be called for many PropertiesChanged signals; filter by interface
    try:
        if interface != GATT_CHRC_IFACE:
            return
        if 'Value' in changed:
            val = changed['Value']
            # val is an array of bytes (dbus Array of bytes)
            data = bytes(val)
            try:
                text = data.decode('utf-8')
            except Exception:
                text = data.hex()
            print('\n[NOTIFICATION] ' + text)
            print('> ', end='', flush=True)
    except Exception as e:
        print('Error in props handler:', e)

def input_thread_func(char_iface):
    # Read user input and send to characteristic
    try:
        while True:
            msg = input('> ')
            if msg is None:
                break
            msg = msg.strip()
            if msg == '':
                continue
            data = [dbus.Byte(b) for b in msg.encode('utf-8')]
            try:
                char_iface.WriteValue(data, {})
            except Exception as e:
                print('Failed to write value:', e)
                break
    except (EOFError, KeyboardInterrupt):
        pass

def main(argv):
    if len(argv) < 2:
        print('Usage: %s hciX' % argv[0])
        return 1
    adapter = argv[1]
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()

    dev_path, svc_path, char_path = find_chat_characteristic(bus, adapter)
    if not char_path:
        print('Chat characteristic not found')
        return 2

    print('Found chat characteristic at', char_path)
    print('Device path:', dev_path)

    device = None
    if dev_path:
        device = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, dev_path), DEVICE_IFACE)
        props = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, dev_path), DBUS_PROP_IFACE)
        connected = False
        try:
            connected = bool(props.Get(DEVICE_IFACE, 'Connected'))
        except Exception:
            connected = False
        if not connected:
            print('Connecting to device', dev_path)
            try:
                device.Connect()
            except Exception as e:
                print('Failed to connect to device:', e)
                return 3

    # Get characteristic interface for read/write/notify
    char_obj = bus.get_object(BLUEZ_SERVICE_NAME, char_path)
    char_iface = dbus.Interface(char_obj, GATT_CHRC_IFACE)

    # Subscribe to PropertiesChanged signals on the characteristic path for GattCharacteristic1
    bus.add_signal_receiver(on_props_changed,
                            signal_name='PropertiesChanged',
                            dbus_interface=DBUS_PROP_IFACE,
                            path=char_path,
                            arg0=GATT_CHRC_IFACE)
    # Start notifications
    try:
        char_iface.StartNotify()
    except Exception as e:
        print('StartNotify failed (maybe already started):', e)

    # Start input thread to send messages
    it = threading.Thread(target=input_thread_func, args=(char_iface,), daemon=True)
    it.start()

    # Run main loop to process incoming notifications
    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        print('Exiting...')
        try:
            char_iface.StopNotify()
        except Exception:
            pass
        loop.quit()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
