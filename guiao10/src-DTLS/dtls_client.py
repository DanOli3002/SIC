#!/usr/bin/python3

import sys

import socket
import ssl
from dtls import do_patch

HOST = 'localhost'
PORT = 443

def main( args ):
    if len(args) == 2:
        port = int(args[1])
    else:
        port = PORT

    do_patch()

    # context is fundamental for validation

    context = ssl.SSLContext( ssl.PROTOCOL_TLS_CLIENT )
    context.load_verify_locations( "ca_crt.pem" )

    with socket.socket( socket.AF_INET, socket.SOCK_DGRAM) as sock:
        with context.wrap_socket( sock ) as dtls_sock:
            dtls_sock.connect( (HOST, port) )
            dtls_sock.send( b"ping" )
            data = tls_sock.recv()
            print( "Received:", data.decode() )
            dtls_sock.close()

if __name__ == "__main__":
    main( sys.argv )
