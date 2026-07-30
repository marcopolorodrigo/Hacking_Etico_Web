import html
import re
from typing import Dict

class OutputSanitizer:
    def __init__(self):
        # Lista de etiquetas HTML peligrosas
        self.dangerous_tags = ['script', 'iframe', 'object', 'embed', 'applet', 'form', 'input']
        # Lista de atributos peligrosos
        self.dangerous_attrs = ['onclick', 'onload', 'onerror', 'onmouseover', 'onfocus', 'onchange']
    
    def sanitize(self, text: str, allow_html: bool = False) -> Dict:
        """
        Sanitiza la salida de IA para prevenir XSS.
        """
        original = text
        sanitized = text
        
        if allow_html:
            # Permitir HTML pero eliminar etiquetas y atributos peligrosos
            for tag in self.dangerous_tags:
                # Eliminar etiquetas completas con su contenido
                sanitized = re.sub(f'<{tag}[^>]*>.*?</{tag}>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)
                # Eliminar etiquetas de apertura sin cierre
                sanitized = re.sub(f'<{tag}[^>]*>', '', sanitized, flags=re.IGNORECASE)
                # Eliminar etiquetas de cierre
                sanitized = re.sub(f'</{tag}>', '', sanitized, flags=re.IGNORECASE)
            
            for attr in self.dangerous_attrs:
                sanitized = re.sub(f'{attr}\\s*=\\s*["\'][^"\']*["\']', '', sanitized, flags=re.IGNORECASE)
        else:
            # Escapar todo el contenido HTML
            sanitized = html.escape(text)
        
        return {
            "original": original,
            "sanitized": sanitized,
            "was_modified": original != sanitized,
            "risk_reduced": True
        }

# Ejemplo de uso
sanitizer = OutputSanitizer()

output = '<script>alert("XSS")</script><b>Texto seguro</b><img src=x onerror="alert(1)">'
result = sanitizer.sanitize(output, allow_html=True)

print(f"Original: {result['original']}")
print(f"Sanitizado: {result['sanitized']}")
