#!/usr/bin/python3

import sys
import socket
from dtls.sslconnection import SSLConnection
from dtls.err import SSLError, SSL_ERROR_WANT_READ, SSL_ERROR_ZERO_RETURN

HOST = '127.0.0.1'
PORT = 443
CERT = 'server_crt.pem'
KEY = 'server_keys.pem'

def main( args ):
    if len(args) == 2:
        port = int(args[1])
    else:
        port = PORT

    with socket.socket( socket.AF_INET, socket.SOCK_DGRAM, 0 ) as sock:
        sock.bind( (HOST, port) )

        # context is fundamental for validation

        context = SSLConnection( sock, 
                                 keyfile=KEY,
                                 certfile=CERT,
                                 server_side=True,
                                 do_handshake_on_connect=False )

        # Wait for a new client

        while True:
            addr = context.listen()
            print( "Connection from:", addr )

            # Setup a security association with the client 

            dtls_session = context.accept()[0]
            dtls_session.do_handshake()

            print( "DTLS server listening..." )
            data = dtls_session.read()
            print( "Received:", data.decode() )
            dtls_session.write( b"pong" )
            dtls_session.shutdown()

if __name__ == "__main__":
    main( sys.argv )
