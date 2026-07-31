from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class NIS2Requirement:
    """Requisito de la Directiva NIS2"""
    id: str
    category: str  # "risk_assessment", "security_measures", "incident_reporting", "business_continuity"
    description: str
    status: str  # "CUMPLE", "PARCIAL", "INCUMPLE"
    evidence: str

class NIS2ComplianceChecker:
    """
    Verificador de cumplimiento NIS2 para organizaciones.
    """
    
    def __init__(self, organization_name: str, sector: str):
        self.organization_name = organization_name
        self.sector = sector
        self.requirements: List[NIS2Requirement] = []
        self._initialize_requirements()
    
    def _initialize_requirements(self):
        self.requirements = [
            NIS2Requirement(
                id="NIS2-001",
                category="risk_assessment",
                description="Evaluación de riesgos de ciberseguridad",
                status="PARCIAL",
                evidence="Evaluación realizada en 2025, pendiente de actualización"
            ),
            NIS2Requirement(
                id="NIS2-002",
                category="security_measures",
                description="Implementación de controles técnicos (firewall, IDS/IPS, cifrado)",
                status="CUMPLE",
                evidence="pfSense con Suricata, cifrado TLS 1.3 implementado"
            ),
            NIS2Requirement(
                id="NIS2-003",
                category="security_measures",
                description="Implementación de controles organizativos (políticas, formación)",
                status="PARCIAL",
                evidence="Políticas de seguridad existentes, formación pendiente de actualización"
            ),
            NIS2Requirement(
                id="NIS2-004",
                category="incident_reporting",
                description="Procedimientos de notificación de incidentes (24h)",
                status="INCUMPLE",
                evidence="Procedimientos no documentados formalmente"
            ),
            NIS2Requirement(
                id="NIS2-005",
                category="business_continuity",
                description="Plan de continuidad del negocio y recuperación ante desastres",
                status="PARCIAL",
                evidence="Plan básico existente, no probado en simulacros"
            )
        ]
    
    def check_compliance(self) -> Dict:
        total = len(self.requirements)
        cumplen = len([r for r in self.requirements if r.status == "CUMPLE"])
        parcial = len([r for r in self.requirements if r.status == "PARCIAL"])
        incumplen = len([r for r in self.requirements if r.status == "INCUMPLE"])
        
        score = (cumplen / total) * 100
        
        return {
            "organization": self.organization_name,
            "sector": self.sector,
            "total_requirements": total,
            "compliant": cumplen,
            "partial": parcial,
            "non_compliant": incumplen,
            "compliance_score": round(score, 1),
            "status": "CUMPLE" if score >= 80 else "PARCIAL" if score >= 50 else "INCUMPLE",
            "details": [
                {
                    "id": r.id,
                    "category": r.category,
                    "description": r.description,
                    "status": r.status,
                    "evidence": r.evidence
                }
                for r in self.requirements
            ],
            "critical_issues": [
                r.id for r in self.requirements if r.status == "INCUMPLE"
            ],
            "recommendations": [
                "Documentar formalmente los procedimientos de notificación de incidentes",
                "Actualizar la evaluación de riesgos de ciberseguridad",
                "Realizar simulacros del plan de continuidad del negocio"
            ]
        }

# Ejemplo de uso
checker = NIS2ComplianceChecker(
    organization_name="Banco Nacional S.A.",
    sector="Finanzas"
)
report = checker.check_compliance()

print("📋 INFORME DE CUMPLIMIENTO NIS2")
print(f"Organización: {report['organization']}")
print(f"Sector: {report['sector']}")
print(f"Puntuación: {report['compliance_score']}% ({report['status']})")
print(f"  Cumple: {report['compliant']}/{report['total_requirements']}")
print(f"  Parcial: {report['partial']}")
print(f"  Incumple: {report['non_compliant']}")

if report['critical_issues']:
    print("\n⚠️ INCUMPLIMIENTOS CRÍTICOS:")
    for issue in report['critical_issues']:
        print(f"  - {issue}")
