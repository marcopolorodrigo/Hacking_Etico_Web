import hashlib


def hashing_demo():
    """
    Simulación de hashing (SHA-256) en Python.
    """
    print("🔐 HASHING (SHA-256)")

    # Mensaje original (se codifica a bytes con UTF-8 para soportar acentos/ñ)
    message = "Configuración del firewall pfSense".encode("utf-8")
    print(f"Mensaje original: {message}")

    # Calcular hash SHA-256
    sha256_hash = hashlib.sha256(message).hexdigest()
    print(f"Hash SHA-256: {sha256_hash}")

    # Calcular hash SHA-512
    sha512_hash = hashlib.sha512(message).hexdigest()
    print(f"Hash SHA-512: {sha512_hash[:20]}...")

    # Verificar integridad (simulación)
    modified_message = "Configuración del firewall pfSense (modificada)".encode("utf-8")
    modified_hash = hashlib.sha256(modified_message).hexdigest()
    print(f"Hash del mensaje modificado: {modified_hash[:20]}...")

    if sha256_hash == modified_hash:
        print("✅ Los hashes coinciden: integridad verificada")
    else:
        print("❌ Los hashes no coinciden: el mensaje ha sido alterado")


# Ejemplo de uso
hashing_demo()