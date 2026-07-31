from typing import Dict, List
from enum import Enum


class Likelihood(Enum):
    """Escala de probabilidad según NIST SP 800-30 (valores 1-5)."""
    VERY_LOW = 1
    LOW = 2
    MODERATE = 3
    HIGH = 4
    VERY_HIGH = 5


class Impact(Enum):
    """Escala de impacto según NIST SP 800-30 (valores 1-5)."""
    VERY_LOW = 1
    LOW = 2
    MODERATE = 3
    HIGH = 4
    VERY_HIGH = 5


class RiskAssessment:
    """
    Evaluación de riesgos basada en la metodología de NIST SP 800-30.
    Cada riesgo se define por una amenaza (threat) que explota una
    vulnerabilidad (vulnerability), con una probabilidad e impacto
    asociados, de los cuales se deriva el nivel de riesgo.
    """

    def __init__(self):
        self.risks: List[Dict] = []
        self._next_id = 1

    def add_risk(
        self,
        threat: str,
        vulnerability: str,
        likelihood: Likelihood,
        impact: Impact,
        mitigation: str,
    ) -> Dict:
        """
        Registra un riesgo identificado, calculando su puntaje y nivel
        (Bajo / Medio / Alto / Crítico) según la matriz NIST 5x5.
        """
        score = likelihood.value * impact.value
        level = self._calculate_level(score)

        risk = {
            "id": f"R-{self._next_id:03d}",
            "threat": threat,
            "vulnerability": vulnerability,
            "likelihood": likelihood.name,
            "impact": impact.name,
            "score": score,
            "level": level,
            "mitigation": mitigation,
        }

        self.risks.append(risk)
        self._next_id += 1
        return risk

    @staticmethod
    def _calculate_level(score: int) -> str:
        """
        Convierte el puntaje (probabilidad x impacto, rango 1-25)
        en un nivel cualitativo de riesgo según NIST SP 800-30.
        """
        if score >= 20:
            return "CRITICAL"
        elif score >= 12:
            return "HIGH"
        elif score >= 6:
            return "MEDIUM"
        else:
            return "LOW"

    def generate_report(self) -> Dict:
        """
        Genera el informe consolidado de riesgos: totales, distribución
        por nivel y el detalle de los riesgos críticos.
        """
        by_level: Dict[str, int] = {}
        for r in self.risks:
            by_level[r["level"]] = by_level.get(r["level"], 0) + 1

        critical_risks = [r for r in self.risks if r["level"] == "CRITICAL"]

        return {
            "total_risks": len(self.risks),
            "by_level": by_level,
            "critical_risks": critical_risks,
            "all_risks": self.risks,
        }


# ----------------------------------------------------------------------
# Ejemplo de uso: registro de riesgos y generación del informe
# ----------------------------------------------------------------------

assessment = RiskAssessment()

assessment.add_risk(
    threat="Actor externo con acceso a credenciales robadas",
    vulnerability="Falta de autenticación multifactor (MFA)",
    likelihood=Likelihood.HIGH,
    impact=Impact.VERY_HIGH,
    mitigation="Implementar MFA en todos los accesos administrativos",
)

assessment.add_risk(
    threat="Malware tipo ransomware distribuido por phishing",
    vulnerability="Personal sin capacitación en seguridad",
    likelihood=Likelihood.MODERATE,
    impact=Impact.HIGH,
    mitigation="Programa de concientización y filtrado de correo avanzado",
)

assessment.add_risk(
    threat="Explotación de vulnerabilidad conocida sin parchar",
    vulnerability="Servidores sin política de gestión de parches",
    likelihood=Likelihood.HIGH,
    impact=Impact.HIGH,
    mitigation="Establecer ciclo formal de gestión de parches (patch management)",
)

assessment.add_risk(
    threat="Empleado interno con privilegios excesivos",
    vulnerability="Falta de control de acceso basado en el principio de menor privilegio",
    likelihood=Likelihood.LOW,
    impact=Impact.MODERATE,
    mitigation="Revisión periódica de permisos y modelo RBAC",
)

report = assessment.generate_report()

print("📊 INFORME DE RIESGOS (NIST SP 800-30)")
print(f"Total de riesgos: {report['total_risks']}")
print(f"Por nivel: {report['by_level']}")

print("\n🚨 RIESGOS CRÍTICOS:")
for r in report['critical_risks']:
    print(f"  {r['id']}: {r['threat']} -> {r['vulnerability']}")
    print(f"    Remedio: {r['mitigation']}")
