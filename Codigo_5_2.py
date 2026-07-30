import re
from typing import List, Dict

class SensitiveDataFilter:
    def __init__(self):
        # Patrones para detectar información sensible en salidas
        self.patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "credit_card": r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
            "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
            "api_key": r'(?:api[_-]?key|apikey|token|secret)[\s:=]+[\w-]+',
            "password": r'(?:password|passwd|pwd)[\s:=]+[\w-]+'
        }
        self.compiled = {k: re.compile(v, re.IGNORECASE) for k, v in self.patterns.items()}
    
    def scan_output(self, text: str) -> Dict:
        """
        Escanea la salida del modelo en busca de información sensible.
        """
        findings = {}
        for name, pattern in self.compiled.items():
            matches = pattern.findall(text)
            if matches:
                findings[name] = matches
        
        return {
            "has_sensitive_data": len(findings) > 0,
            "findings": findings,
            "redacted_text": self._redact(text, findings)
        }
    
    def _redact(self, text: str, findings: Dict) -> str:
        """Reemplaza información sensible con [REDACTADO]"""
        redacted = text
        for name, matches in findings.items():
            for match in matches:
                redacted = redacted.replace(match, f"[{name.upper()}_REDACTADO]")
        return redacted

# Ejemplo de uso
filter_ = SensitiveDataFilter()

output = "El usuario maria@banco.com tiene una tarjeta 4111-1111-1111-1111 y su teléfono es 555-123-4567."
result = filter_.scan_output(output)

print(f"¿Contiene datos sensibles? {result['has_sensitive_data']}")
print(f"Texto redactado: {result['redacted_text']}")
