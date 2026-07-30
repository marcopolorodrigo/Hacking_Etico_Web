import html
import re
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class OutputValidationResult:
    """Resultado de la validación de una salida"""
    is_safe: bool
    sanitized_output: str
    sensitive_data_detected: bool
    warnings: List[str]

class OutputSanitizationFilter:
    """
    Filtro de salida para prevenir divulgación de información sensible y XSS.
    """
    
    def __init__(self):
        self.sensitive_patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "credit_card": r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
            "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
            "api_key": r'(?:api[_-]?key|apikey|token|secret)[\s:=]+[\w-]+',
            "password": r'(?:password|passwd|pwd)[\s:=]+[\w-]+',
            "aws_key": r'AKIA[0-9A-Z]{16}',
            "jwt": r'eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*'
        }
        self.dangerous_tags = ['script', 'iframe', 'object', 'embed', 'applet', 'form', 'input', 'textarea', 'button']
        self.dangerous_attrs = ['onclick', 'onload', 'onerror', 'onmouseover', 'onfocus', 'onchange', 'onblur', 'onkeydown']
        self.redact_message = "[DATOS_REDACTADOS]"
    
    def validate_and_sanitize(self, output: str, 
                              allow_html: bool = False,
                              redact_sensitive: bool = True) -> OutputValidationResult:
        """
        Valida y sanitiza la salida del LLM.
        """
        warnings = []
        sanitized = output
        sensitive_detected = False
        
        # 1. Detectar y redactar información sensible
        if redact_sensitive:
            for name, pattern in self.sensitive_patterns.items():
                matches = re.findall(pattern, sanitized, re.IGNORECASE)
                if matches:
                    warnings.append(f"Se detectó información sensible: {name}")
                    sensitive_detected = True
                    for match in matches:
                        sanitized = sanitized.replace(match, self.redact_message)
        
        # 2. Sanitizar HTML si se permite
        if allow_html:
            sanitized = self._sanitize_html(sanitized)
        else:
            sanitized = html.escape(sanitized)
        
        # 3. Eliminar posibles inyecciones de comandos
        sanitized = re.sub(r'[;&|`$()]', '', sanitized)
        
        # 4. Verificar si la salida contiene tokens JWT (especialmente peligrosos)
        if re.search(self.sensitive_patterns["jwt"], sanitized, re.IGNORECASE):
            warnings.append("Se detectó un token JWT en la salida")
            sensitive_detected = True
            sanitized = re.sub(self.sensitive_patterns["jwt"], self.redact_message, sanitized, flags=re.IGNORECASE)
        
        is_safe = not sensitive_detected
        
        return OutputValidationResult(
            is_safe=is_safe,
            sanitized_output=sanitized,
            sensitive_data_detected=sensitive_detected,
            warnings=warnings
        )
    
    def _sanitize_html(self, html_text: str) -> str:
        """Sanitiza HTML eliminando etiquetas y atributos peligrosos"""
        for tag in self.dangerous_tags:
            # Eliminar etiquetas completas con contenido
            html_text = re.sub(f'<{tag}[^>]*>.*?</{tag}>', '', html_text, 
                               flags=re.IGNORECASE | re.DOTALL)
            # Eliminar etiquetas de apertura sin cierre
            html_text = re.sub(f'<{tag}[^>]*>', '', html_text, flags=re.IGNORECASE)
            html_text = re.sub(f'</{tag}>', '', html_text, flags=re.IGNORECASE)
        
        for attr in self.dangerous_attrs:
            html_text = re.sub(f'{attr}\\s*=\\s*["\'][^"\']*["\']', '', html_text, 
                               flags=re.IGNORECASE)
        
        return html_text

# Ejemplo de uso
filter_ = OutputSanitizationFilter()

outputs = [
    "El usuario maria@banco.com tiene una tarjeta 4111-1111-1111-1111.",
    "<script>alert('XSS')</script><h1>Informe seguro</h1>",
    "La clave API es AKIAIOSFODNN7EXAMPLE y el secreto es wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY."
]

for out in outputs:
    result = filter_.validate_and_sanitize(out, allow_html=True)
    print(f"Original: {out}")
    print(f"Sanitizado: {result.sanitized_output}")
    print(f"Seguro: {result.is_safe}")
    print(f"Advertencias: {result.warnings}")
    print()
