#!/usr/bin/python3

import sys

import socket
import wolfssl

HOST = 'localhost'
PORT = 443

def main( args ):
    if len(args) == 2:
        port = int(args[1])
    else:
        port = PORT

    # context is fundamental for validation

    context = wolfssl.SSLContext( wolfssl.PROTOCOL_TLSv1_2)
    context.verify_mode = wolfssl.CERT_REQUIRED # Server authentication required
    context.load_verify_locations( "ca_crt.pem" )

    with socket.socket( socket.AF_INET, socket.SOCK_STREAM ) as sock:
        tls_sock = context.wrap_socket( sock )

        tls_sock.connect( (HOST, port ) )
        tls_sock.send( b"ping" )
        data = tls_sock.recv( 1024 )
        print( "Received:", data.decode() )

        tls_sock.close()

if __name__ == "__main__":
    main( sys.argv )
