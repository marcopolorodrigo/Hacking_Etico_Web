from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class LFPDPPPRequirement:
    """Requisito de la LFPDPPP para sistemas de IA"""
    article: str
    description: str
    status: str  # "CUMPLE", "PARCIAL", "INCUMPLE"
    evidence: str

class LFPDPPPComplianceChecker:
    """
    Verificador de cumplimiento LFPDPPP para sistemas de IA en México.
    """
    
    def __init__(self, system_name: str):
        self.system_name = system_name
        self.requirements: List[LFPDPPPRequirement] = []
        self._initialize_requirements()
    
    def _initialize_requirements(self):
        self.requirements = [
            LFPDPPPRequirement(
                article="Art. 6 (Consentimiento)",
                description="Consentimiento explícito para el tratamiento de datos personales",
                status="PARCIAL",
                evidence="Consentimiento obtenido para recolección, no para procesamiento por IA"
            ),
            LFPDPPPRequirement(
                article="Art. 7 (Aviso de privacidad)",
                description="Aviso de privacidad actualizado con información sobre IA",
                status="INCUMPLE",
                evidence="Aviso de privacidad no menciona el uso de IA"
            ),
            LFPDPPPRequirement(
                article="Art. 8 (Derechos ARCO)",
                description="Derechos de Acceso, Rectificación, Cancelación y Oposición",
                status="PARCIAL",
                evidence="Derechos ARCO implementados para datos estructurados, no para modelos de IA"
            ),
            LFPDPPPRequirement(
                article="Art. 19 (Medidas de seguridad)",
                description="Medidas técnicas y organizativas para proteger datos",
                status="CUMPLE",
                evidence="Cifrado, control de acceso y monitoreo implementados"
            ),
            LFPDPPPRequirement(
                article="Art. 22 (Inventario de datos)",
                description="Mantener inventario actualizado de datos personales",
                status="PARCIAL",
                evidence="Inventario de datos existente, pero no cubre datos procesados por IA"
            )
        ]
    
    def check_compliance(self) -> Dict:
        """Evalúa el cumplimiento LFPDPPP del sistema"""
        total = len(self.requirements)
        cumplen = len([r for r in self.requirements if r.status == "CUMPLE"])
        parcial = len([r for r in self.requirements if r.status == "PARCIAL"])
        incumplen = len([r for r in self.requirements if r.status == "INCUMPLE"])
        
        score = (cumplen / total) * 100
        
        return {
            "system": self.system_name,
            "regulation": "LFPDPPP (México)",
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

# Ejemplo de uso
checker = LFPDPPPComplianceChecker("Chatbot de Atención al Cliente")
report = checker.check_compliance()

print("📋 INFORME DE CUMPLIMIENTO LFPDPPP")
print(f"Sistema: {report['system']}")
print(f"Puntuación: {report['compliance_score']}% ({report['status']})")
print(f"  Cumple: {report['compliant']}/{report['total_requirements']}")
print(f"  Parcial: {report['partial']}")
print(f"  Incumple: {report['non_compliant']}")

if report['critical_issues']:
    print("\n⚠️ INCUMPLIMIENTOS CRÍTICOS:")
    for issue in report['critical_issues']:
        print(f"  - {issue}")
