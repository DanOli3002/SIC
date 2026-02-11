#!/usr/bin/python3

import sys
import socket
import wolfssl

HOST = '127.0.0.1'
PORT = 443
CERT = 'server_crt.pem'
KEY = 'server_keys.pem'

def main( args ):
    if len(args) == 2:
        port = int(args[1])
    else:
        port = PORT

    # context is fundamental for validation

    context = wolfssl.SSLContext( wolfssl.PROTOCOL_TLS, server_side=True )
    context.load_cert_chain( certfile = CERT, keyfile = KEY )

    with socket.socket( socket.AF_INET, socket.SOCK_STREAM, 0 ) as sock:
        sock.bind( (HOST, port) )
        sock.listen( 5 )
        while True:
            client, addr = sock.accept()
            print( "Connection from:", addr )

            tls_sock = context.wrap_socket( client, server_side=True )
            print( "TLS server listening..." )
            data = tls_sock.recv( 1024 )
            print( "Received:", data.decode() )
            tls_sock.send( b"pong" )
            tls_sock.close()

if __name__ == "__main__":
    main( sys.argv )
