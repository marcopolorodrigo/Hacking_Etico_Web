from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
import datetime
from typing import Dict

class TLSInspector:
    """
    Simulación de inspección TLS (SSL inspection) en Python.
    """
    
    def __init__(self):
        self.ca_cert = None
        self.ca_key = None
        self._generate_ca()
    
    def _generate_ca(self):
        """Genera un certificado raíz de CA (simulación)"""
        # Generar clave privada de la CA
        self.ca_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        
        # Generar certificado de la CA
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "ES"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Madrid"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Empresa Proxy"),
            x509.NameAttribute(NameOID.COMMON_NAME, "Proxy CA"),
        ])
        
        self.ca_cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            self.ca_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.now() - datetime.timedelta(days=1)
        ).not_valid_after(
            datetime.datetime.now() + datetime.timedelta(days=3650)
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=None),
            critical=True,
        ).sign(self.ca_key, hashes.SHA256())
    
    def inspect_traffic(self, url: str, encrypted_data: bytes) -> Dict:
        """
        Simula la inspección de tráfico TLS.
        """
        print(f"🔒 Inspeccionando tráfico TLS para {url}")
        
        # Simular descifrado del tráfico
        decrypted = f"Contenido descifrado de {url}".encode()
        
        # Simular inspección de contenido (detección de malware)
        threat_detected = any(word in decrypted.decode().lower() for word in ["malware", "phishing", "exploit"])
        
        # Simular re-cifrado
        re_encrypted = f"Re-cifrado: {decrypted.decode()}".encode()
        
        return {
            "url": url,
            "threat_detected": threat_detected,
            "action": "BLOCK" if threat_detected else "ALLOW",
            "decrypted_content": decrypted[:50],
            "ca_cert_used": self.ca_cert.subject.rfc4514_string()
        }

# Ejemplo de uso
inspector = TLSInspector()

# Simular inspección de tráfico
traffic = [
    ("https://www.ejemplo.com", b"encrypted_data_1"),
    ("https://www.malware.com/exploit", b"encrypted_data_2"),
    ("https://www.ejemplo.com/products", b"encrypted_data_3"),
]

print("🔍 INSPECCIÓN SSL/TLS")
for url, data in traffic:
    result = inspector.inspect_traffic(url, data)
    status = "🚫 BLOQUEADO" if result["threat_detected"] else "✅ PERMITIDO"
    print(f"{status}: {url} - {result['action']}")
