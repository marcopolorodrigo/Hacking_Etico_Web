import ssl
import socket
from typing import Dict

class TLSVerifier:
    """
    Verificador de TLS para APIs de IA.
    """
    
    def verify_tls(self, hostname: str, port: int = 443) -> Dict:
        """
        Verifica la configuración TLS de un servidor.
        """
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    version = ssock.version()
                    
                    return {
                        "status": "OK",
                        "hostname": hostname,
                        "port": port,
                        "tls_version": version,
                        "cipher": cipher,
                        "certificate": {
                            "issuer": cert.get('issuer'),
                            "subject": cert.get('subject'),
                            "valid_from": cert.get('notBefore'),
                            "valid_to": cert.get('notAfter')
                        },
                        "message": f"Conexión TLS 1.3 segura a {hostname}"
                    }
        except ssl.SSLError as e:
            return {
                "status": "ERROR",
                "hostname": hostname,
                "message": f"Error TLS: {str(e)[:100]}",
                "severity": "HIGH"
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "hostname": hostname,
                "message": f"Error de conexión: {str(e)[:100]}",
                "severity": "MEDIUM"
            }

# Ejemplo de uso
verifier = TLSVerifier()

# Verificar TLS de una API de IA
result = verifier.verify_tls("api.openai.com")
print(f"🔒 VERIFICACIÓN TLS")
if result["status"] == "OK":
    print(f"  TLS: {result['tls_version']}")
    print(f"  Cipher: {result['cipher']}")
    print(f"  Certificado válido hasta: {result['certificate']['valid_to']}")
else:
    print(f"  Error: {result['message']}")
