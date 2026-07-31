import json
from cryptography.fernet import Fernet

def encrypt_backup(config_data: bytes, key: bytes) -> bytes:
    """
    Simula el cifrado de un backup de configuración de pfSense.
    """
    cipher = Fernet(key)
    encrypted = cipher.encrypt(config_data)
    return encrypted

def decrypt_backup(encrypted_data: bytes, key: bytes) -> bytes:
    """
    Simula el descifrado de un backup de configuración de pfSense.
    """
    cipher = Fernet(key)
    decrypted = cipher.decrypt(encrypted_data)
    return decrypted

# Ejemplo de uso
print("🔐 CIFRADO DE BACKUPS DE PFSENSE")

# Configuración simulada
config = {
    "hostname": "firewall",
    "lan_ip": "192.168.1.1",
    "rules": [
        {"action": "pass", "protocol": "tcp", "source": "192.168.1.0/24", "port": 80}
    ]
}
config_data = json.dumps(config).encode()

# Generar clave de cifrado
key = Fernet.generate_key()
print(f"Clave de cifrado: {key[:20]}...")

# Cifrar backup
encrypted = encrypt_backup(config_data, key)
print(f"Backup cifrado: {encrypted[:20]}...")

# Descifrar backup
decrypted = decrypt_backup(encrypted, key)
print(f"Backup descifrado: {decrypted[:50]}...")

# Verificar integridad
if config_data == decrypted:
    print("✅ Integridad verificada")
else:
    print("❌ Error: los datos no coinciden")
