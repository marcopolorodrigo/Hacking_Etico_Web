from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class AIRisk:
    """Representa un riesgo de IA en redes con pfSense"""
    id: str
    threat: str
    vulnerability: str
    impact_on_network: str
    likelihood: str
    severity: str
    mitigation: str

class AIRiskAssessment:
    """
    Evaluación de riesgos de IA para redes con pfSense.
    """
    
    def __init__(self):
        self.risks: List[AIRisk] = []
        self._initialize_risks()
    
    def _initialize_risks(self):
        """Inicializa riesgos de IA comunes en redes con pfSense"""
        self.risks = [
            AIRisk(
                id="AI-R-001",
                threat="Inyección de Prompts",
                vulnerability="Falta de filtros de entrada en el chatbot de IA",
                impact_on_network="Exfiltración de datos de clientes a través del tráfico HTTP",
                likelihood="MEDIUM",
                severity="HIGH",
                mitigation="Implementar reglas de Suricata para detectar inyección de prompts, filtros en Squid"
            ),
            AIRisk(
                id="AI-R-002",
                threat="Envenenamiento de Datos",
                vulnerability="Datos de entrenamiento no validados",
                impact_on_network="Degradación del modelo de IA, afectando la toma de decisiones",
                likelihood="LOW",
                severity="HIGH",
                mitigation="Validar datos en los pipelines de entrenamiento, monitorear deriva de datos"
            ),
            AIRisk(
                id="AI-R-003",
                threat="Extracción de Modelo",
                vulnerability="Falta de rate limiting en las APIs de IA",
                impact_on_network="Pérdida de propiedad intelectual, ataques de denegación de servicio",
                likelihood="MEDIUM",
                severity="MEDIUM",
                mitigation="Implementar rate limiting en pfSense (limitación de conexiones) para las APIs de IA"
            ),
            AIRisk(
                id="AI-R-004",
                threat="Ataques Adversariales",
                vulnerability="Modelo de IA sin pruebas de robustez",
                impact_on_network="Decisiones incorrectas del modelo, afectando la lógica de negocio",
                likelihood="LOW",
                severity="MEDIUM",
                mitigation="Realizar pruebas de red teaming, implementar defensas adversariales"
            )
        ]
    
    def generate_report(self) -> Dict:
        """Genera un informe de riesgos de IA"""
        return {
            "total_risks": len(self.risks),
            "by_severity": {
                s: len([r for r in self.risks if r.severity == s])
                for s in set(r.severity for r in self.risks)
            },
            "risks": [
                {
                    "id": r.id,
                    "threat": r.threat,
                    "vulnerability": r.vulnerability,
                    "severity": r.severity,
                    "mitigation": r.mitigation
                }
                for r in self.risks
            ],
            "recommendations": [
                "Implementar reglas de Suricata para detectar inyección de prompts",
                "Implementar rate limiting para APIs de IA en pfSense",
                "Realizar pruebas de robustez del modelo de IA"
            ]
        }

# Ejemplo de uso
ai_risk = AIRiskAssessment()
report = ai_risk.generate_report()

print("📊 INFORME DE RIESGOS DE IA EN REDES")
print(f"Total de riesgos: {report['total_risks']}")
print(f"Por severidad: {report['by_severity']}")

print("\n📋 RIESGOS DE IA:")
for r in report['risks']:
    print(f"  {r['id']}: {r['threat']} - {r['severity']}")
    print(f"    Mitigación: {r['mitigation']}")
