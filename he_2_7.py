from cryptography.fernet import Fernet
import pickle
import os
from typing import Dict, Any

class ModelEncryption:
    """
    Cifrado de modelos de IA para protección en reposo.
    """
    
    def __init__(self):
        self.key = None
        self.cipher = None
    
    def generate_key(self) -> bytes:
        """Genera una clave de cifrado"""
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        return self.key
    
    def load_key(self, key: bytes):
        """Carga una clave existente"""
        self.key = key
        self.cipher = Fernet(key)
    
    def encrypt_model(self, model_path: str, output_path: str):
        """Cifra un modelo de IA"""
        if not self.cipher:
            raise ValueError("Clave no configurada. Usar generate_key() o load_key()")
        
        # Cargar modelo (simulado)
        with open(model_path, 'rb') as f:
            model_data = f.read()
        
        # Cifrar
        encrypted_data = self.cipher.encrypt(model_data)
        
        # Guardar modelo cifrado
        with open(output_path, 'wb') as f:
            f.write(encrypted_data)
        
        # Guardar clave (en producción, usar un KMS)
        key_path = output_path + '.key'
        with open(key_path, 'wb') as f:
            f.write(self.key)
        
        return output_path, key_path
    
    def decrypt_model(self, encrypted_path: str, key_path: str, output_path: str):
        """Descifra un modelo de IA"""
        # Cargar clave
        with open(key_path, 'rb') as f:
            key = f.read()
        self.load_key(key)
        
        # Cargar modelo cifrado
        with open(encrypted_path, 'rb') as f:
            encrypted_data = f.read()
        
        # Descifrar
        model_data = self.cipher.decrypt(encrypted_data)
        
        # Guardar modelo descifrado
        with open(output_path, 'wb') as f:
            f.write(model_data)
        
        return output_path

# Ejemplo de uso
enc = ModelEncryption()

# Generar clave
key = enc.generate_key()
print(f"Clave generada: {key[:20]}...")

# Simular guardado de modelo cifrado
# (En producción, se cifraría un modelo real)
encrypted_path, key_path = enc.encrypt_model("modelo.pkl", "modelo_encrypted.bin")
print(f"Modelo cifrado: {encrypted_path}")
print(f"Clave guardada: {key_path}")

# Simular descifrado
decrypted_path = enc.decrypt_model(encrypted_path, key_path, "modelo_decrypted.pkl")
print(f"Modelo descifrado: {decrypted_path}")
