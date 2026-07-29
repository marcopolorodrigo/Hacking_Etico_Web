from dataclasses import dataclass, field
from typing import List, Dict
import json
from datetime import datetime

@dataclass
class AlgorithmicImpactAssessment:
    system_name: str
    system_description: str
    system_purpose: str
    stakeholders: List[str]
    risk_level: str = "NO_CLASIFICADO"
    impacts: List[Dict] = field(default_factory=list)
    mitigations: List[Dict] = field(default_factory=list)
    
    def classify_risk(self) -> str:
        """Clasifica el riesgo según AI Act"""
        high_risk_domains = [
            "empleo", "educación", "infraestructura_crítica", 
            "aplicación_ley", "calificación_crediticia", "salud", "justicia"
        ]
        
        # Simulación: verificar si el sistema opera en dominios de alto riesgo
        for domain in high_risk_domains:
            if domain in self.system_description.lower():
                self.risk_level = "ALTO_RIESGO (Anexo III)"
                return self.risk_level
        
        # Verificar si es sistema interactivo o generativo (transparencia)
        if "chatbot" in self.system_description.lower() or "generativo" in self.system_description.lower():
            self.risk_level = "RIESGO_DE_TRANSPARENCIA (Art. 50)"
            return self.risk_level
        
        self.risk_level = "RIESGO_MÍNIMO"
        return self.risk_level
    
    def add_impact(self, impact_type: str, description: str, 
                   affected_groups: List[str], severity: str):
        self.impacts.append({
            "type": impact_type,
            "description": description,
            "affected_groups": affected_groups,
            "severity": severity,
            "date_identified": datetime.now().isoformat()
        })
    
    def add_mitigation(self, impact_ref: str, measure: str, 
                       responsible: str, deadline: str):
        self.mitigations.append({
            "impact": impact_ref,
            "measure": measure,
            "responsible": responsible,
            "deadline": deadline,
            "status": "PENDIENTE"
        })
    
    def generate_report(self) -> Dict:
        """Genera un informe completo de la EIA"""
        return {
            "system": {
                "name": self.system_name,
                "description": self.system_description,
                "purpose": self.system_purpose,
                "stakeholders": self.stakeholders,
                "risk_level": self.risk_level,
                "assessment_date": datetime.now().isoformat()
            },
            "impacts": self.impacts,
            "mitigations": self.mitigations,
            "summary": {
                "total_impacts": len(self.impacts),
                "total_mitigations": len(self.mitigations),
                "critical_impacts": len([i for i in self.impacts if i["severity"] == "CRÍTICO"]),
                "status": "EN_REVISIÓN" if self.mitigations else "PENDIENTE"
            }
        }

# Ejemplo: Evaluación de un chatbot de selección de personal
eia = AlgorithmicImpactAssessment(
    system_name="Chatbot de Selección de Personal IA",
    system_description="Sistema de chatbot que realiza entrevistas iniciales y selecciona candidatos para puestos de trabajo, utilizando procesamiento de lenguaje natural y análisis de sentimiento.",
    system_purpose="Automatizar la preselección de candidatos para reducir el tiempo de contratación.",
    stakeholders=["Candidatos", "Departamento de RRHH", "Equipo de IA", "Comité de Ética", "Reguladores"]
)

eia.classify_risk()
print(f"Clasificación de riesgo: {eia.risk_level}")

# Añadir impactos identificados
eia.add_impact(
    impact_type="SESGO",
    description="El modelo podría discriminar a candidatos por género o origen étnico debido a sesgos en los datos de entrenamiento.",
    affected_groups=["Mujeres", "Minorías étnicas", "Candidatos de mayor edad"],
    severity="CRÍTICO"
)
eia.add_impact(
    impact_type="PRIVACIDAD",
    description="El chatbot recopila información personal sensible durante las entrevistas (origen, estado civil, etc.) sin consentimiento explícito.",
    affected_groups=["Todos los candidatos"],
    severity="ALTO"
)
eia.add_impact(
    impact_type="TRANSPARENCIA",
    description="Los candidatos no son informados de que están interactuando con un sistema de IA.",
    affected_groups=["Todos los candidatos"],
    severity="MEDIO"
)

# Añadir medidas de mitigación
eia.add_mitigation(
    impact_ref="SESGO",
    measure="Auditar el modelo para detectar y corregir sesgos. Implementar técnicas de fairness (reweighting, adversarial debiasing).",
    responsible="Equipo de Ética de IA",
    deadline="2026-12-31"
)
eia.add_mitigation(
    impact_ref="PRIVACIDAD",
    measure="Implementar consentimiento explícito para la recopilación de datos sensibles. Anonimizar datos no esenciales.",
    responsible="Equipo de Privacidad",
    deadline="2026-10-15"
)
eia.add_mitigation(
    impact_ref="TRANSPARENCIA",
    measure="Informar a los candidatos en la primera interacción que están hablando con un sistema de IA. Cumplir con Art. 50 del AI Act.",
    responsible="Equipo de Desarrollo",
    deadline="2026-08-02"
)

# Generar informe
report = eia.generate_report()
print(json.dumps(report, indent=2, default=str))
