from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class EthicalImpact:
    """Impacto ético de un sistema de IA"""
    category: str  # "sesgo", "privacidad", "transparencia", "seguridad", "discriminacion"
    description: str
    affected_groups: List[str]
    severity: str  # "CRITICAL", "HIGH", "MEDIUM", "LOW"
    mitigation: str

class EthicalImpactAssessment:
    """
    Evaluación de impacto ético para sistemas de IA.
    """
    
    def __init__(self, system_name: str):
        self.system_name = system_name
        self.impacts: List[EthicalImpact] = []
    
    def assess(self, domain: str, data_sources: List[str],
               expected_users: List[str]) -> Dict:
        """
        Evalúa los impactos éticos del sistema.
        """
        # 1. Evaluar sesgos potenciales
        if any("redes sociales" in d or "web scraping" in d for d in data_sources):
            self.impacts.append(EthicalImpact(
                category="sesgo",
                description="Datos de entrenamiento pueden contener sesgos de redes sociales",
                affected_groups=["Minorías étnicas", "Género", "Edad"],
                severity="HIGH",
                mitigation="Auditar y equilibrar los datos de entrenamiento"
            ))
        
        # 2. Evaluar privacidad
        if "datos personales" in str(data_sources).lower():
            self.impacts.append(EthicalImpact(
                category="privacidad",
                description="El sistema procesa datos personales sensibles",
                affected_groups=["Todos los usuarios"],
                severity="CRITICAL",
                mitigation="Implementar anonimización y cifrado de datos"
            ))
        
        # 3. Evaluar transparencia
        if "black box" in domain.lower() or "deep learning" in domain.lower():
            self.impacts.append(EthicalImpact(
                category="transparencia",
                description="El modelo es una caja negra, difícil de explicar",
                affected_groups=["Todos los usuarios"],
                severity="MEDIUM",
                mitigation="Implementar técnicas de explicabilidad (SHAP, LIME)"
            ))
        
        # 4. Evaluar discriminación
        if domain in ["employment", "credit", "healthcare"]:
            self.impacts.append(EthicalImpact(
                category="discriminacion",
                description="El sistema puede discriminar en decisiones críticas",
                affected_groups=["Grupos vulnerables"],
                severity="CRITICAL",
                mitigation="Realizar pruebas de equidad y monitoreo continuo"
            ))
        
        return self._generate_report()
    
    def _generate_report(self) -> Dict:
        critical = [i for i in self.impacts if i.severity == "CRITICAL"]
        high = [i for i in self.impacts if i.severity == "HIGH"]
        
        return {
            "system": self.system_name,
            "total_impacts": len(self.impacts),
            "critical": len(critical),
            "high": len(high),
            "medium": len([i for i in self.impacts if i.severity == "MEDIUM"]),
            "low": len([i for i in self.impacts if i.severity == "LOW"]),
            "details": [
                {
                    "category": i.category,
                    "description": i.description,
                    "affected_groups": i.affected_groups,
                    "severity": i.severity,
                    "mitigation": i.mitigation
                }
                for i in self.impacts
            ],
            "status": "CRITICAL" if critical else "ATENCION" if high else "ACEPTABLE"
        }

# Ejemplo de uso
assessment = EthicalImpactAssessment("Sistema de Selección de Personal IA")
report = assessment.assess(
    domain="employment (black box model)",
    data_sources=["redes sociales", "datos personales de empleados", "entrevistas grabadas"],
    expected_users=["candidatos", "departamento de RRHH"]
)

print("📋 EVALUACIÓN DE IMPACTO ÉTICO")
print(f"Sistema: {report['system']}")
print(f"Estado: {report['status']}")
print(f"  Total de impactos: {report['total_impacts']}")
print(f"  Críticos: {report['critical']}")
print(f"  Altos: {report['high']}")

print("\n📌 DETALLE DE IMPACTOS:")
for i in report['details']:
    print(f"  [{i['severity']}] {i['category']}: {i['description']}")
    print(f"    Grupos afectados: {', '.join(i['affected_groups'])}")
    print(f"    Mitigación: {i['mitigation']}")
