#!/usr/bin/python3

import sys
import os
from cryptography import x509
from datetime import datetime, timezone
import urllib.request

def load_certificate( file ):
    try:
        with open( file, "rb" ) as fd:
            return x509.load_pem_x509_certificate( fd.read() )
    except Exception as e:
        print( f"Cannot load certificate from file {file}: {e}" )
        return None

def get_issuer_certificate( url ):
# TODO: add your code here
    print(url)
# until here

def build_cert_path( certificate ):
    if certificate.subject == certificate.issuer:
        print( "The chain ended, this is a self-certified certificate" )
        return  # Cannot continue

# TODO: add your code here
    certificate.extensions.get_extension_for_oid(x509.AuthorityInformationAccess)
    for d in description_list:
        if d.access_method == x509.AuthorityInformationAccess.CA_ISSUERS:
            url_location = d.access_location
            emissor = get_issuer_certificate(url_location)
            build_cert_path(emissor)
# until here

def main( argv ):
    if len(argv) < 2:
        print( "Usage: %s certificate_file" % (argv[0]) )
        return

    certificate = load_certificate( argv[1] )
    if certificate != None:
        print( "Built path for %s" % (certificate.subject.rfc4514_string()) )

        build_cert_path( certificate )

if __name__ == "__main__":
    main( sys.argv )
