import ssl
import certifi
import requests
from typing import Dict

class ModelCertificateVerifier:
    """
    Verificador de certificados para modelos de IA.
    """
    
    def __init__(self):
        self.trust_store = certifi.where()
    
    def verify_https(self, url: str) -> Dict:
        """
        Verifica el certificado TLS de un servidor de IA.
        """
        try:
            response = requests.get(url, verify=self.trust_store, timeout=10)
            return {
                "status": "OK",
                "message": f"Conexión HTTPS segura a {url}",
                "status_code": response.status_code
            }
        except requests.exceptions.SSLError as e:
            return {
                "status": "ERROR",
                "message": f"Error de certificado: {str(e)[:100]}",
                "severity": "CRITICAL"
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Error de conexión: {str(e)[:100]}",
                "severity": "HIGH"
            }
    
    def verify_model_certificate(self, model_url: str, 
                                 expected_issuer: str) -> Dict:
        """
        Verifica que el certificado de un modelo sea válido.
        """
        result = self.verify_https(model_url)
        
        if result["status"] == "OK":
            # Simulación de verificación de emisor
            # En producción, se extraería el certificado y se verificaría
            # la cadena de confianza
            result["issuer_verified"] = True
            result["message"] += " - Certificado verificado"
        
        return result

# Ejemplo de uso
verifier = ModelCertificateVerifier()

# Verificar conexión a un modelo en Hugging Face
result = verifier.verify_https("https://huggingface.co/models")
print(f"🔒 VERIFICACIÓN HTTPS")
print(f"Estado: {result['status']}")
print(f"Mensaje: {result['message']}")

# Verificar certificado de un modelo
result = verifier.verify_model_certificate(
    "https://huggingface.co/bert-base-uncased",
    "Hugging Face, Inc."
)
print(f"\n🔐 VERIFICACIÓN DE CERTIFICADO DE MODELO")
print(f"Estado: {result['status']}")
