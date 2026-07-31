from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization

def asymmetric_encryption_demo():
    """
    Simulación de cifrado asimétrico (RSA) en Python.
    """
    print("🔐 CIFRADO ASIMÉTRICO (RSA)")
    
    # Generar par de claves
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    
    # Mensaje original
    message = b"Este es un mensaje secreto para el administrador"
    print(f"Mensaje original: {message}")
    
    # Cifrar con clave pública
    encrypted = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print(f"Mensaje cifrado: {encrypted[:20]}...")
    
    # Descifrar con clave privada
    decrypted = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print(f"Mensaje descifrado: {decrypted}")
    
    # Mostrar claves (simulación)
    print(f"Clave pública: {public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)[:30]}...")
    return private_key, public_key

# Ejemplo de uso
asymmetric_encryption_demo()
