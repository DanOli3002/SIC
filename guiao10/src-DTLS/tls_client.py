#!/usr/bin/python3

import sys

import socket
import ssl

HOST = 'localhost'
PORT = 443

def main( args ):
    if len(args) == 2:
        port = int(args[1])
    else:
        port = PORT

    # context is fundamental for validation

    # context = ssl.create_default_context()
    # context.check_hostname = False      # !!
    # context.verify_mode = ssl.CERT_NONE # !!
    context = ssl.SSLContext( ssl.PROTOCOL_TLS_CLIENT )
    context.load_verify_locations( "ca_crt.pem" )

    with socket.create_connection( (HOST, port) ) as sock:
        with context.wrap_socket( sock, server_hostname=HOST ) as tls_sock:
            tls_sock.send( b"ping" )
            data = tls_sock.recv( 1024 )
            print( "Received:", data.decode() )

if __name__ == "__main__":
    main( sys.argv )
