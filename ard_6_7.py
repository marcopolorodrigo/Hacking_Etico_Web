from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
from typing import Dict

class CertificateManager:
    """
    Simulación de gestión de certificados en pfSense.
    """
    
    def __init__(self):
        self.ca_cert = None
        self.ca_key = None
        self.server_certs = []
        self.client_certs = []
    
    def create_ca(self, common_name: str = "pfSense CA") -> Dict:
        """
        Crea una Autoridad de Certificación (CA) interna.
        """
        print(f"🔐 Creando CA: {common_name}")
        
        # Generar clave privada
        self.ca_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        
        # Crear certificado de CA
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "ES"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Empresa"),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
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
        
        print(f"✅ CA creada: {self.ca_cert.subject.rfc4514_string()}")
        return {
            "status": "CREATED",
            "ca_name": common_name,
            "ca_cert": self.ca_cert,
            "valid_until": self.ca_cert.not_valid_after
        }
    
    def create_server_cert(self, common_name: str) -> Dict:
        """
        Crea un certificado de servidor firmado por la CA.
        """
        if not self.ca_cert:
            return {"status": "ERROR", "message": "CA no creada"}
        
        print(f"🔐 Creando certificado de servidor: {common_name}")
        
        # Generar clave privada para el servidor
        server_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        
        # Crear certificado firmado por la CA
        subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "ES"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Empresa"),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ])
        
        server_cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            self.ca_cert.subject
        ).public_key(
            server_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.now() - datetime.timedelta(days=1)
        ).not_valid_after(
            datetime.datetime.now() + datetime.timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName(common_name),
            ]),
            critical=False,
        ).sign(self.ca_key, hashes.SHA256())
        
        cert_info = {
            "name": common_name,
            "cert": server_cert,
            "key": server_key,
            "valid_until": server_cert.not_valid_after
        }
        self.server_certs.append(cert_info)
        print(f"✅ Certificado de servidor creado: {common_name}")
        return cert_info
    
    def create_client_cert(self, common_name: str) -> Dict:
        """
        Crea un certificado de cliente firmado por la CA.
        """
        if not self.ca_cert:
            return {"status": "ERROR", "message": "CA no creada"}
        
        print(f"🔐 Creando certificado de cliente: {common_name}")
        
        # Generar clave privada para el cliente
        client_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        
        # Crear certificado firmado por la CA
        subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "ES"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Empresa"),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ])
        
        client_cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            self.ca_cert.subject
        ).public_key(
            client_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.now() - datetime.timedelta(days=1)
        ).not_valid_after(
            datetime.datetime.now() + datetime.timedelta(days=365)
        ).sign(self.ca_key, hashes.SHA256())
        
        cert_info = {
            "name": common_name,
            "cert": client_cert,
            "key": client_key,
            "valid_until": client_cert.not_valid_after
        }
        self.client_certs.append(cert_info)
        print(f"✅ Certificado de cliente creado: {common_name}")
        return cert_info
    
    def revoke_cert(self, common_name: str) -> Dict:
        """
        Simula la revocación de un certificado.
        """
        print(f"🔒 Revocando certificado: {common_name}")
        # Simular CRL
        return {
            "status": "REVOKED",
            "cert_name": common_name,
            "reason": "Compromiso de clave"
        }

# Ejemplo de uso
cert_mgr = CertificateManager()

# Crear CA
ca = cert_mgr.create_ca("pfSense CA Internal")

# Crear certificado de servidor
server_cert = cert_mgr.create_server_cert("firewall.empresa.com")
print(f"  Servidor: {server_cert['name']} - Válido hasta: {server_cert['valid_until']}")

# Crear certificado de cliente
client_cert = cert_mgr.create_client_cert("juan.perez")
print(f"  Cliente: {client_cert['name']} - Válido hasta: {client_cert['valid_until']}")

# Revocar certificado
revocation = cert_mgr.revoke_cert("juan.perez")
print(f"  Revocación: {revocation['status']} - {revocation['reason']}")
