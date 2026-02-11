#!/usr/bin/python3

import sys
import socket
import ssl

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

    context = ssl.SSLContext( ssl.PROTOCOL_TLS_SERVER )
    context.load_cert_chain( certfile = CERT, keyfile = KEY )

    with socket.socket( socket.AF_INET, socket.SOCK_STREAM, 0 ) as sock:
        sock.bind( (HOST, port) )
        sock.listen( 5 )
        with context.wrap_socket( sock, server_side=True ) as tls_sock:
            while True:
                print( "TLS server listening..." )
                conn, addr = tls_sock.accept()
                print( "Connection from:", addr )
                data = conn.recv(1024)
                print( "Received:", data.decode() )
                conn.send( b"pong" )
                conn.close()

if __name__ == "__main__":
    main( sys.argv )
