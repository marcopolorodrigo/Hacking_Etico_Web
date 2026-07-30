from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class GDPRRequirement:
    """Requisito del GDPR para sistemas de IA"""
    article: str
    description: str
    status: str  # "CUMPLE", "PARCIAL", "INCUMPLE"
    evidence: str
    due_date: Optional[str] = None

class GDPRComplianceChecker:
    """
    Verificador de cumplimiento GDPR para sistemas de IA.
    """
    
    def __init__(self, system_name: str):
        self.system_name = system_name
        self.requirements: List[GDPRRequirement] = []
        self._initialize_requirements()
    
    def _initialize_requirements(self):
        """Inicializa los requisitos del GDPR para IA"""
        self.requirements = [
            GDPRRequirement(
                article="Art. 6 (Legalidad)",
                description="Base legal para el procesamiento de datos personales",
                status="PARCIAL",
                evidence="Consentimiento obtenido para datos de entrenamiento, no para inferencia"
            ),
            GDPRRequirement(
                article="Art. 13 (Transparencia)",
                description="Información a los usuarios sobre el procesamiento de datos",
                status="PARCIAL",
                evidence="Aviso de privacidad actualizado, pero no específico para IA"
            ),
            GDPRRequirement(
                article="Art. 22 (Decisiones automatizadas)",
                description="Derecho a no ser sujeto a decisiones automatizadas",
                status="INCUMPLE",
                evidence="No se ofrece opción de revisión humana para decisiones automatizadas"
            ),
            GDPRRequirement(
                article="Art. 32 (Seguridad)",
                description="Medidas de seguridad técnicas y organizativas",
                status="CUMPLE",
                evidence="Cifrado en reposo y en tránsito, control de acceso"
            ),
            GDPRRequirement(
                article="Art. 33 (Notificación de brechas)",
                description="Notificación en 72 horas de brechas de datos",
                status="CUMPLE",
                evidence="Plan de respuesta a incidentes implementado"
            ),
            GDPRRequirement(
                article="Art. 35 (DPIA)",
                description="Evaluación de impacto sobre la protección de datos",
                status="INCUMPLE",
                evidence="No se realizó DPIA para el sistema de IA"
            ),
            GDPRRequirement(
                article="Art. 17 (Derecho al olvido)",
                description="Eliminación de datos personales",
                status="PARCIAL",
                evidence="Eliminación implementada para datos estructurados, no para modelos de IA"
            )
        ]
    
    def check_compliance(self) -> Dict:
        """Evalúa el cumplimiento GDPR del sistema"""
        total = len(self.requirements)
        cumplen = len([r for r in self.requirements if r.status == "CUMPLE"])
        parcial = len([r for r in self.requirements if r.status == "PARCIAL"])
        incumplen = len([r for r in self.requirements if r.status == "INCUMPLE"])
        
        score = (cumplen / total) * 100
        
        return {
            "system": self.system_name,
            "total_requirements": total,
            "compliant": cumplen,
            "partial": parcial,
            "non_compliant": incumplen,
            "compliance_score": round(score, 1),
            "status": "CUMPLE" if score >= 80 else "PARCIAL" if score >= 50 else "INCUMPLE",
            "details": [
                {
                    "article": r.article,
                    "description": r.description,
                    "status": r.status,
                    "evidence": r.evidence
                }
                for r in self.requirements
            ],
            "critical_issues": [
                r.article for r in self.requirements if r.status == "INCUMPLE"
            ]
        }
    
    def generate_remediation_plan(self) -> List[str]:
        """Genera un plan de remediación para incumplimientos"""
        plan = []
        for r in self.requirements:
            if r.status == "INCUMPLE":
                if "Art. 22" in r.article:
                    plan.append("Implementar opción de revisión humana para decisiones automatizadas")
                elif "Art. 35" in r.article:
                    plan.append("Realizar DPIA para el sistema de IA antes del próximo despliegue")
                elif "Art. 17" in r.article:
                    plan.append("Implementar eliminación de datos de modelos de IA (machine unlearning)")
            elif r.status == "PARCIAL":
                if "Art. 13" in r.article:
                    plan.append("Actualizar aviso de privacidad para incluir información específica sobre IA")
                elif "Art. 6" in r.article:
                    plan.append("Obtener consentimiento específico para el uso de datos en inferencia")
        return plan

# Ejemplo de uso
checker = GDPRComplianceChecker("Chatbot de Atención al Cliente")
report = checker.check_compliance()

print("📋 INFORME DE CUMPLIMIENTO GDPR")
print(f"Sistema: {report['system']}")
print(f"Puntuación: {report['compliance_score']}% ({report['status']})")
print(f"  Cumple: {report['compliant']}/{report['total_requirements']}")
print(f"  Parcial: {report['partial']}")
print(f"  Incumple: {report['non_compliant']}")

if report['critical_issues']:
    print("\n⚠️ INCUMPLIMIENTOS CRÍTICOS:")
    for issue in report['critical_issues']:
        print(f"  - {issue}")

print("\n📌 PLAN DE REMEDIACIÓN:")
plan = checker.generate_remediation_plan()
for item in plan:
    print(f"  - {item}")
