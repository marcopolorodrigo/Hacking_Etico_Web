# Uso de la librería oqs (Open Quantum Safe) para firma post-cuántica
# Instalación: pip install liboqs-python
import oqs

def sign_and_verify_post_quantum(message):
    # Generar par de claves Dilithium (Nivel de seguridad 2)
    with oqs.Signature("Dilithium2") as signer:
        # Generar clave pública y privada
        public_key = signer.generate_keypair()
        # Firmar el mensaje
        signature = signer.sign(message.encode())
        # Verificar firma
        is_valid = signer.verify(message.encode(), signature, public_key)
        return is_valid, public_key, signature

# Ejemplo
mensaje = "Contrato de confidencialidad 2026-07-22"
valido, pub_key, sig = sign_and_verify_post_quantum(mensaje)
print(f"Firma Dilithium válida: {valido}")
print(f"Clave pública (truncada): {pub_key[:20]}...")
