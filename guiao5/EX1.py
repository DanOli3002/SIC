import sys
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def main():
    # Verificar se foram passados 3 argumentos (nomes dos arquivos e tamanho da chave)
    if len(sys.argv) != 4:
        print("Uso: python keygen.py <arquivo_publico> <arquivo_privado> <tamanho_chave>")
        print("Exemplo: python keygen.py pub.txt priv.txt 4096")
        return
    
    pub_filename = sys.argv[1]
    priv_filename = sys.argv[2]
    key_size = int(sys.argv[3])

    valid_sizes = [1024, 2048, 3072, 4096]
    if key_size not in valid_sizes:
        print(f"Tamanho inválido. Escolha entre {valid_sizes}.")
        return

    # Gerar par de chaves
    key_pair = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size
    )

    # Serializar chave privada em PEM sem encriptação
    priv_key_pem = key_pair.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Serializar chave pública em PEM
    pub_key_pem = key_pair.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Salvar arquivos
    with open(priv_filename, 'wb') as f:
        f.write(priv_key_pem)
    with open(pub_filename, 'wb') as f:
        f.write(pub_key_pem)
    
    print(f"Chaves RSA geradas com tamanho {key_size} bits.")
    print(f"Chave pública salva em: {pub_filename}")
    print(f"Chave privada salva em: {priv_filename}")

if __name__ == "__main__":
    main()