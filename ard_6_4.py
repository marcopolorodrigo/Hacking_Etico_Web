from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


def digital_signature_demo():
    """
    Simulación de firmas digitales en Python.
    """
    print("🔐 FIRMA DIGITAL (RSA)")

    # Generar par de claves
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # Mensaje original (se codifica a bytes con UTF-8 para soportar acentos/ñ)
    message = "Configuración del firewall pfSense version 2.0".encode("utf-8")
    print(f"Mensaje original: {message}")

    # Firmar el mensaje
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print(f"Firma: {signature[:20]}...")

    # Verificar la firma (correcta)
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("✅ Firma verificada correctamente")
    except Exception:
        print("❌ Firma inválida")

    # Verificar con mensaje modificado
    modified_message = "Configuración del firewall pfSense version 2.1".encode("utf-8")
    try:
        public_key.verify(
            signature,
            modified_message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("✅ Firma verificada correctamente (mensaje modificado)")
    except Exception:
        print("❌ Firma inválida (mensaje modificado)")


# Ejemplo de uso
digital_signature_demo()