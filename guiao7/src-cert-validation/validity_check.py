#!/usr/bin/python3

import sys
import os
from cryptography import x509
from datetime import datetime, timezone

def load_certificate( file ):
    try:
        with open( file, "rb" ) as fd:
            return x509.load_pem_x509_certificate( fd.read() )
    except Exception as e:
        print( f"Cannot load certificate from file {file}: {e}" )
        return None

def valid( certificate ):
    # Certificate times refer to UTC
    now = datetime.now( timezone.utc )

# TODO: add your code here
    if now < certificate.not_valid_before_utc or now > certificate.not_valid_after_utc:
        print("Certificate is not valid.")
        return False
    else:
        print("Certificate is valid.")
        return True
    
# until here

def main( argv ):
    if len(argv) < 2:
        print( "Usage: %s certificate_file" % (argv[0]) )
        return

    certificate = load_certificate( argv[1] )
    if certificate != None:
        valid( certificate )

if __name__ == "__main__":
    main( sys.argv )
