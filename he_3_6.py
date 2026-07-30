from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
import os

# ============= CIFRADO SIMÉTRICO (AES) =============
def sym_encrypt_decrypt():
    print("🔐 CIFRADO SIMÉTRICO (AES)")
    
    # Generar clave
    key = Fernet.generate_key()
    cipher = Fernet(key)
    
    # Cifrar
    message = b"Datos sensibles del modelo de IA"
    encrypted = cipher.encrypt(message)
    print(f"Texto cifrado: {encrypted[:20]}...")
    
    # Descifrar
    decrypted = cipher.decrypt(encrypted)
    print(f"Texto descifrado: {decrypted.decode()}")
    
    return key

# ============= CIFRADO ASIMÉTRICO (RSA) =============
def asym_encrypt_decrypt():
    print("\n🔐 CIFRADO ASIMÉTRICO (RSA)")
    
    # Generar par de claves
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    
    # Cifrar con clave pública
    message = b"Clave para el modelo de IA"
    encrypted = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print(f"Texto cifrado: {encrypted[:20]}...")
    
    # Descifrar con clave privada
    decrypted = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print(f"Texto descifrado: {decrypted.decode()}")
    
    return private_key, public_key

# ============= CIFRADO HÍBRIDO =============
def hybrid_encrypt(message: bytes, public_key):
    """
    Cifrado híbrido: cifrado simétrico del mensaje + cifrado asimétrico de la clave.
    """
    # 1. Generar clave simétrica aleatoria
    sym_key = Fernet.generate_key()
    cipher = Fernet(sym_key)
    
    # 2. Cifrar mensaje con cifrado simétrico
    encrypted_message = cipher.encrypt(message)
    
    # 3. Cifrar clave simétrica con cifrado asimétrico
    encrypted_key = public_key.encrypt(
        sym_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return encrypted_message, encrypted_key

def hybrid_decrypt(encrypted_message, encrypted_key, private_key):
    """Descifrado híbrido."""
    # 1. Descifrar clave simétrica con cifrado asimétrico
    sym_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    # 2. Descifrar mensaje con cifrado simétrico
    cipher = Fernet(sym_key)
    decrypted = cipher.decrypt(encrypted_message)
    return decrypted

# Ejemplo de uso
sym_encrypt_decrypt()
private_key, public_key = asym_encrypt_decrypt()

print("\n🔐 CIFRADO HÍBRIDO")
message = b"Datos de entrenamiento del modelo"
enc_msg, enc_key = hybrid_encrypt(message, public_key)
dec_msg = hybrid_decrypt(enc_msg, enc_key, private_key)
print(f"Mensaje original: {message.decode()}")
print(f"Mensaje descifrado: {dec_msg.decode()}")
