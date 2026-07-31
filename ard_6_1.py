from cryptography.fernet import Fernet
import os

def symmetric_encryption_demo():
    """
    Simulación de cifrado simétrico (AES) en Python.
    """
    print("🔐 CIFRADO SIMÉTRICO (AES)")
    
    # Generar una clave simétrica
    key = Fernet.generate_key()
    cipher = Fernet(key)
    
    # Mensaje original
    message = b"Este es un mensaje secreto para la red corporativa"
    print(f"Mensaje original: {message}")
    
    # Cifrar
    encrypted = cipher.encrypt(message)
    print(f"Mensaje cifrado: {encrypted[:20]}...")
    
    # Descifrar
    decrypted = cipher.decrypt(encrypted)
    print(f"Mensaje descifrado: {decrypted}")
    
    # Guardar la clave (simulación)
    print(f"Clave (guardar de forma segura): {key[:20]}...")
    return key

# Ejemplo de uso
symmetric_encryption_demo()
