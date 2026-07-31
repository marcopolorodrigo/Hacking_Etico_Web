from typing import Dict

class SSLStrippingDetector:
    """
    Simulación de detección de SSL Stripping en red.
    """
    
    def __init__(self):
        self.hsts_headers = {}
    
    def check_hsts(self, domain: str, response_headers: Dict) -> Dict:
        """
        Verifica si un dominio tiene HSTS habilitado.
        """
        if "Strict-Transport-Security" in response_headers:
            hsts = response_headers["Strict-Transport-Security"]
            max_age = int(hsts.split(";")[0].split("=")[1])
            
            return {
                "domain": domain,
                "hsts_enabled": True,
                "max_age": max_age,
                "secure": max_age > 0
            }
        else:
            return {
                "domain": domain,
                "hsts_enabled": False,
                "secure": False,
                "risk": "Vulnerable a SSL Stripping"
            }
    
    def detect_downgrade(self, tls_version: str) -> Dict:
        """
        Detecta si se está utilizando una versión TLS obsoleta.
        """
        secure_versions = ["TLSv1.3", "TLSv1.2"]
        if tls_version in secure_versions:
            return {"tls_version": tls_version, "secure": True}
        else:
            return {"tls_version": tls_version, "secure": False, "risk": "Versión TLS obsoleta"}

# Ejemplo de uso
detector = SSLStrippingDetector()

# Simular respuesta HTTP
response_headers = {
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Type": "text/html"
}

result = detector.check_hsts("ejemplo.com", response_headers)
print(f"HSTS: {result['domain']} - {'✅ Habilitado' if result['hsts_enabled'] else '❌ No habilitado'}")

# Simular versión TLS
tls_result = detector.detect_downgrade("TLSv1.3")
print(f"TLS: {tls_result['tls_version']} - {'✅ Seguro' if tls_result['secure'] else '❌ Inseguro'}")
