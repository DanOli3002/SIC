#!/usr/bin/python3

import sys

import socket
from dtls.sslconnection import SSLConnection
from dtls.err import SSLError, SSL_ERROR_WANT_READ, SSL_ERROR_ZERO_RETURN
import ssl

HOST = 'localhost'
PORT = 443

def main( args ):
    if len(args) == 2:
        port = int(args[1])
    else:
        port = PORT

    with socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) as sock:
        sock.connect( (HOST, port ) )
        dtls_session = SSLConnection( sock, 
                                 ca_certs="ca_crt.pem",
                                 server_side=False,
                                 cert_reqs = ssl.CERT_REQUIRED,
                                 do_handshake_on_connect=False )

        dtls_session.do_handshake()

        dtls_session.write( b"ping" )
        data = dtls_session.read()
        print( "Received:", data.decode() )
        dtls_session.shutdown()

if __name__ == "__main__":
    main( sys.argv )
