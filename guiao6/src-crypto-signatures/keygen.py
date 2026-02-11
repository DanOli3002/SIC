from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

key_sizes = [1024, 2048, 3072, 4096]

for k in key_sizes:
    print(f"Generating RSA {k}-bit key pair...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=k,
        backend=default_backend()
    )

    priv_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    pub_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    priv_path = f"rsa_private_{k}.pem"
    pub_path = f"rsa_public_{k}.pem"

    with open(priv_path, "wb") as f:
        f.write(priv_pem)
    with open(pub_path, "wb") as f:
        f.write(pub_pem)

    print(f"Written {priv_path} and {pub_path}")

print("All keys generated.")