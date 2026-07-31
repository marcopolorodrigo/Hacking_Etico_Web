from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

@dataclass
class RedTeamFinding:
    """Hallazgo de una sesión de Red Teaming"""
    category: str  # "prompt_injection", "bias", "adversarial", "stealing"
    severity: str
    description: str
    recommendation: str

class AIRedTeam:
    """Simulación de Red Teaming de IA"""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.findings: List[RedTeamFinding] = []
    
    def run_exercise(self) -> List[RedTeamFinding]:
        """Ejecuta una sesión de Red Teaming"""
        self._test_prompt_injection()
        self._test_bias()
        self._test_adversarial()
        self._test_model_stealing()
        return self.findings
    
    def _test_prompt_injection(self):
        self.findings.append(RedTeamFinding(
            category="prompt_injection",
            severity="CRITICAL",
            description="El modelo revela información sensible con prompts específicos.",
            recommendation="Implementar filtros de entrada y sanitización de prompts"
        ))
    
    def _test_bias(self):
        self.findings.append(RedTeamFinding(
            category="bias",
            severity="HIGH",
            description="El modelo muestra sesgo de género en sus predicciones.",
            recommendation="Auditar y reentrenar el modelo con datos más diversos"
        ))
    
    def _test_adversarial(self):
        self.findings.append(RedTeamFinding(
            category="adversarial",
            severity="MEDIUM",
            description="El modelo es vulnerable a ataques adversariales en imágenes.",
            recommendation="Implementar entrenamiento adversarial"
        ))
    
    def _test_model_stealing(self):
        self.findings.append(RedTeamFinding(
            category="stealing",
            severity="HIGH",
            description="El modelo puede ser extraído mediante consultas masivas.",
            recommendation="Implementar rate limiting y detección de patrones"
        ))

# Ejemplo de uso
redteam = AIRedTeam("Chatbot Bancario v2.0")
findings = redteam.run_exercise()
print("📊 INFORME DE RED TEAMING")
for f in findings:
    print(f"  [{f.severity}] {f.category}: {f.description}")
    print(f"    Remedio: {f.recommendation}")
