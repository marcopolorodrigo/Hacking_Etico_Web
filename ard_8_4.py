from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class ISO42001Requirement:
    """Requisito de la norma ISO/IEC 42001"""
    id: str
    category: str  # "policy", "risk_assessment", "controls", "monitoring", "improvement"
    description: str
    status: str  # "CUMPLE", "PARCIAL", "INCUMPLE"
    evidence: str

class ISO42001ComplianceChecker:
    """
    Verificador de cumplimiento ISO 42001 para sistemas de IA.
    """
    
    def __init__(self, system_name: str):
        self.system_name = system_name
        self.requirements: List[ISO42001Requirement] = []
        self._initialize_requirements()
    
    def _initialize_requirements(self):
        self.requirements = [
            ISO42001Requirement(
                id="ISO42001-001",
                category="policy",
                description="Política de IA: principios y objetivos definidos",
                status="PARCIAL",
                evidence="Política de IA en desarrollo, no aprobada formalmente"
            ),
            ISO42001Requirement(
                id="ISO42001-002",
                category="risk_assessment",
                description="Evaluación de riesgos de IA (sesgo, inyección de prompts, etc.)",
                status="INCUMPLE",
                evidence="No se ha realizado una evaluación de riesgos específica para IA"
            ),
            ISO42001Requirement(
                id="ISO42001-003",
                category="controls",
                description="Controles de IA (filtros de prompts, sanitización de salidas, etc.)",
                status="PARCIAL",
                evidence="Algunos controles implementados, pero no documentados formalmente"
            ),
            ISO42001Requirement(
                id="ISO42001-004",
                category="monitoring",
                description="Monitoreo de rendimiento y conformidad de sistemas de IA",
                status="PARCIAL",
                evidence="Monitoreo básico implementado, sin alertas automatizadas"
            ),
            ISO42001Requirement(
                id="ISO42001-005",
                category="improvement",
                description="Procesos de mejora continua para sistemas de IA",
                status="INCUMPLE",
                evidence="No hay procesos formales de mejora continua"
            )
        ]
    
    def check_compliance(self) -> Dict:
        total = len(self.requirements)
        cumplen = len([r for r in self.requirements if r.status == "CUMPLE"])
        parcial = len([r for r in self.requirements if r.status == "PARCIAL"])
        incumplen = len([r for r in self.requirements if r.status == "INCUMPLE"])
        
        score = (cumplen / total) * 100
        
        return {
            "system": self.system_name,
            "standard": "ISO/IEC 42001",
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
                "Desarrollar y aprobar formalmente una política de IA",
                "Realizar una evaluación de riesgos específica para IA",
                "Documentar formalmente los controles de IA implementados",
                "Implementar monitoreo automatizado con alertas",
                "Establecer procesos formales de mejora continua"
            ]
        }

# Ejemplo de uso
checker = ISO42001ComplianceChecker("Sistema de Recomendación IA")
report = checker.check_compliance()

print("📋 INFORME DE CUMPLIMIENTO ISO 42001")
print(f"Sistema: {report['system']}")
print(f"Puntuación: {report['compliance_score']}% ({report['status']})")
print(f"  Cumple: {report['compliant']}/{report['total_requirements']}")
print(f"  Parcial: {report['partial']}")
print(f"  Incumple: {report['non_compliant']}")

if report['critical_issues']:
    print("\n⚠️ INCUMPLIMIENTOS CRÍTICOS:")
    for issue in report['critical_issues']:
        print(f"  - {issue}")
