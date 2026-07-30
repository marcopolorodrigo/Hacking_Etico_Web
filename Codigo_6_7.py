import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class VulnerabilitySeverity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

@dataclass
class Finding:
    line: int
    code: str
    vulnerability: str
    severity: VulnerabilitySeverity
    description: str
    suggestion: str

class HybridSAST:
    """
    Analizador SAST híbrido que combina reglas tradicionales con razonamiento LLM.
    """
    
    def __init__(self):
        # Reglas tradicionales (patrones)
        self.syntactic_rules = [
            {
                "pattern": r"eval\s*\(",
                "vulnerability": "Uso de eval()",
                "severity": VulnerabilitySeverity.CRITICAL,
                "description": "eval() puede ejecutar código arbitrario",
                "suggestion": "Usar ast.literal_eval() o funciones seguras"
            },
            {
                "pattern": r"exec\s*\(",
                "vulnerability": "Uso de exec()",
                "severity": VulnerabilitySeverity.CRITICAL,
                "description": "exec() puede ejecutar código arbitrario",
                "suggestion": "Evitar exec() o usar con restricciones"
            },
            {
                "pattern": r"cursor\.execute\s*\(\s*f['\"]",
                "vulnerability": "SQL Injection potencial",
                "severity": VulnerabilitySeverity.HIGH,
                "description": "Concatenación directa en SQL query",
                "suggestion": "Usar consultas parametrizadas"
            },
            {
                "pattern": r"<script>|javascript:",
                "vulnerability": "XSS potencial",
                "severity": VulnerabilitySeverity.HIGH,
                "description": "Contenido no sanitizado en salida HTML",
                "suggestion": "Sanitizar salidas con html.escape()"
            }
        ]
    
    def analyze(self, code: str, filename: str) -> List[Finding]:
        """
        Analiza el código combinando reglas sintácticas y razonamiento LLM.
        """
        findings = []
        lines = code.split('\n')
        
        # 1. Análisis sintáctico (reglas tradicionales)
        for i, line in enumerate(lines, 1):
            for rule in self.syntactic_rules:
                if re.search(rule["pattern"], line, re.IGNORECASE):
                    findings.append(Finding(
                        line=i,
                        code=line.strip(),
                        vulnerability=rule["vulnerability"],
                        severity=rule["severity"],
                        description=rule["description"],
                        suggestion=rule["suggestion"]
                    ))
        
        # 2. Simulación de análisis semántico (LLM)
        # En producción, aquí se llamaría a un LLM para analizar el código
        semantic_findings = self._semantic_analysis(code)
        findings.extend(semantic_findings)
        
        return findings
    
    def _semantic_analysis(self, code: str) -> List[Finding]:
        """
        Simula el análisis semántico con LLM.
        En producción, se usaría un modelo como CodeQL o un LLM especializado.
        """
        findings = []
        
        # Detectar patrones de inyección de prompts (contexto LLM)
        if 'prompt' in code.lower() and '+' in code:
            findings.append(Finding(
                line=0,  # Línea no específica en simulación
                code="...",
                vulnerability="Posible concatenación insegura de prompts",
                severity=VulnerabilitySeverity.HIGH,
                description="La concatenación de cadenas en prompts puede permitir inyección",
                suggestion="Usar plantillas de prompts estructuradas"
            ))
        
        # Detectar manejo inseguro de salidas de LLM
        if 'llm' in code.lower() and 'response' in code.lower():
            if 'html' in code.lower() or 'render' in code.lower():
                findings.append(Finding(
                    line=0,
                    code="...",
                    vulnerability="Salida de LLM no sanitizada",
                    severity=VulnerabilitySeverity.HIGH,
                    description="La salida del LLM se usa en contexto HTML sin sanitización",
                    suggestion="Sanitizar la salida con html.escape() o un sanitizador HTML"
                ))
        
        return findings

# Ejemplo de uso
sast = HybridSAST()

code = """
def process_user_input(user_input):
    # PELIGROSO: eval de entrada de usuario
    result = eval(user_input)
    
    # PELIGROSO: SQL injection
    cursor.execute(f"SELECT * FROM users WHERE id = {user_input}")
    
    # PELIGROSO: Prompt concatenation
    prompt = "Eres un asistente. Usuario: " + user_input
    
    return result
"""

findings = sast.analyze(code, "app.py")
print(f"Análisis de {len(findings)} hallazgos:")
for f in findings:
    print(f"  [{f.severity.value}] {f.vulnerability} (Línea {f.line})")
    print(f"    {f.description}")
    print(f"    Sugerencia: {f.suggestion}")
