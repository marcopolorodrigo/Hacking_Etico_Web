import html
import re
import json
from typing import Dict, List, Optional

class OutputSanitizer:
    """
    Sanitizador de salidas de LLM para prevenir XSS, inyección de comandos y fuga de datos.
    """
    
    def __init__(self):
        # Etiquetas HTML peligrosas
        self.dangerous_tags = ['script', 'iframe', 'object', 'embed', 'applet', 
                               'form', 'input', 'textarea', 'button']
        # Atributos peligrosos (event handlers)
        self.dangerous_attrs = ['onclick', 'onload', 'onerror', 'onmouseover', 
                                'onfocus', 'onchange', 'onblur', 'onkeydown']
        # Patrones de datos sensibles
        self.sensitive_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'credit_card': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'api_key': r'(?:api[_-]?key|apikey|token|secret)[\s:=]+[\w-]+',
        }
    
    def sanitize_output(self, text: str, 
                        allow_html: bool = False,
                        detect_sensitive: bool = True) -> Dict:
        """
        Sanitiza la salida del LLM.
        
        Args:
            text: Texto a sanitizar
            allow_html: Si se permite HTML (con sanitización)
            detect_sensitive: Si se debe detectar información sensible
        
        Returns:
            Dict con texto sanitizado y metadatos
        """
        original = text
        sanitized = text
        warnings = []
        
        # 1. Detectar información sensible
        if detect_sensitive:
            sensitive_findings = self._detect_sensitive(sanitized)
            if sensitive_findings:
                warnings.append(f"Se detectó información sensible: {sensitive_findings}")
                # Redactar información sensible
                for pattern_name, matches in sensitive_findings.items():
                    for match in matches:
                        sanitized = sanitized.replace(match, f"[{pattern_name.upper()}_REDACTADO]")
        
        # 2. Sanitizar HTML si se permite
        if allow_html:
            sanitized = self._sanitize_html(sanitized)
        else:
            sanitized = html.escape(sanitized)
        
        # 3. Prevenir inyección de comandos (si se usa en shell)
        # Escapar caracteres peligrosos para shell
        sanitized = re.sub(r'[;&|`$()]', '', sanitized)
        
        return {
            "original": original,
            "sanitized": sanitized,
            "was_modified": original != sanitized,
            "warnings": warnings,
            "has_sensitive_data": len(warnings) > 0
        }
    
    def _detect_sensitive(self, text: str) -> Dict:
        """Detecta información sensible en el texto"""
        findings = {}
        for name, pattern in self.sensitive_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                findings[name] = matches
        return findings
    
    def _sanitize_html(self, html_text: str) -> str:
        """Sanitiza HTML eliminando etiquetas y atributos peligrosos"""
        for tag in self.dangerous_tags:
            # Eliminar etiquetas completas con contenido
            html_text = re.sub(f'<{tag}[^>]*>.*?</{tag}>', '', html_text, 
                               flags=re.IGNORECASE | re.DOTALL)
            # Eliminar etiquetas de apertura sin cierre
            html_text = re.sub(f'<{tag}[^>]*>', '', html_text, flags=re.IGNORECASE)
            # Eliminar etiquetas de cierre
            html_text = re.sub(f'</{tag}>', '', html_text, flags=re.IGNORECASE)
        
        for attr in self.dangerous_attrs:
            html_text = re.sub(f'{attr}\\s*=\\s*["\'][^"\']*["\']', '', html_text, 
                               flags=re.IGNORECASE)
        
        return html_text

# Ejemplo de uso
sanitizer = OutputSanitizer()

# Salida peligrosa de un LLM
llm_output = """
<script>alert('XSS')</script>
<h1>Informe de usuario</h1>
Email: maria@banco.com
Tarjeta: 4111-1111-1111-1111
<img src="x" onerror="steal_cookies()">
"""

result = sanitizer.sanitize_output(llm_output, allow_html=True)
print(f"Texto sanitizado:\n{result['sanitized']}")
print(f"Advertencias: {result['warnings']}")
