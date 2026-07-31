from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Vulnerability:
    """Representa una vulnerabilidad en la red"""
    id: str
    name: str
    category: str  # "configuration", "software", "authentication", "network", "physical", "policy", "ai_specific"
    description: str
    severity: str  # "CRITICAL", "HIGH", "MEDIUM", "LOW"
    cvss_score: float
    affected_asset: str
    remediation: str

class VulnerabilityIdentification:
    """
    Identificación de vulnerabilidades en redes con pfSense.
    """
    
    def __init__(self):
        self.vulnerabilities: List[Vulnerability] = []
        self._initialize_vulnerabilities()
    
    def _initialize_vulnerabilities(self):
        """Inicializa una lista de vulnerabilidades comunes en redes con pfSense"""
        self.vulnerabilities = [
            Vulnerability(
                id="V-001",
                name="Puertos SSH expuestos a Internet",
                category="configuration",
                description="El puerto SSH (22) está abierto a Internet, permitiendo ataques de fuerza bruta",
                severity="HIGH",
                cvss_score=7.5,
                affected_asset="pfSense Firewall",
                remediation="Cerrar puerto SSH o limitar acceso a IPs autorizadas, usar autenticación de clave pública"
            ),
            Vulnerability(
                id="V-002",
                name="pfSense sin actualizar",
                category="software",
                description="El firewall pfSense está ejecutando una versión obsoleta con vulnerabilidades conocidas",
                severity="CRITICAL",
                cvss_score=9.0,
                affected_asset="pfSense Firewall",
                remediation="Actualizar pfSense a la última versión estable"
            ),
            Vulnerability(
                id="V-003",
                name="Contraseña por defecto en admin",
                category="authentication",
                description="El usuario admin de pfSense tiene una contraseña débil o por defecto",
                severity="CRITICAL",
                cvss_score=9.8,
                affected_asset="pfSense Firewall",
                remediation="Cambiar la contraseña de admin, habilitar MFA y deshabilitar usuarios innecesarios"
            ),
            Vulnerability(
                id="V-004",
                name="Suricata con firmas obsoletas",
                category="software",
                description="Suricata tiene reglas de detección de amenazas desactualizadas",
                severity="HIGH",
                cvss_score=7.0,
                affected_asset="Suricata IDS/IPS",
                remediation="Configurar actualización automática de reglas de Suricata"
            ),
            Vulnerability(
                id="V-005",
                name="Falta de filtros de prompts en chatbot IA",
                category="ai_specific",
                description="El chatbot de IA no tiene filtros de entrada para prevenir inyección de prompts",
                severity="HIGH",
                cvss_score=8.5,
                affected_asset="Chatbot IA",
                remediation="Implementar filtros de prompts y sanitización de entradas"
            ),
            Vulnerability(
                id="V-006",
                name="Falta de políticas de seguridad documentadas",
                category="policy",
                description="No existen políticas de seguridad formalizadas para la gestión del firewall",
                severity="MEDIUM",
                cvss_score=5.0,
                affected_asset="Documentación",
                remediation="Desarrollar e implementar políticas de seguridad para pfSense"
            )
        ]
    
    def add_vulnerability(self, vulnerability: Vulnerability):
        self.vulnerabilities.append(vulnerability)
    
    def get_vulnerabilities_by_severity(self, severity: str) -> List[Vulnerability]:
        return [v for v in self.vulnerabilities if v.severity == severity]
    
    def get_critical_vulnerabilities(self) -> List[Vulnerability]:
        return [v for v in self.vulnerabilities if v.severity == "CRITICAL"]
    
    def generate_report(self) -> Dict:
        """Genera un informe de vulnerabilidades"""
        return {
            "total_vulnerabilities": len(self.vulnerabilities),
            "by_severity": {
                s: len([v for v in self.vulnerabilities if v.severity == s])
                for s in set(v.severity for v in self.vulnerabilities)
            },
            "by_category": {
                c: len([v for v in self.vulnerabilities if v.category == c])
                for c in set(v.category for v in self.vulnerabilities)
            },
            "critical_vulnerabilities": [
                {"id": v.id, "name": v.name, "cvss_score": v.cvss_score, "remediation": v.remediation}
                for v in self.vulnerabilities if v.severity == "CRITICAL"
            ],
            "vulnerabilities": [
                {"id": v.id, "name": v.name, "severity": v.severity, "cvss_score": v.cvss_score}
                for v in self.vulnerabilities
            ]
        }

# Ejemplo de uso
vulns = VulnerabilityIdentification()
report = vulns.generate_report()

print("📊 INFORME DE VULNERABILIDADES")
print(f"Total de vulnerabilidades: {report['total_vulnerabilities']}")
print(f"Por severidad: {report['by_severity']}")
print(f"Por categoría: {report['by_category']}")

print("\n🚨 VULNERABILIDADES CRÍTICAS:")
for v in report['critical_vulnerabilities']:
    print(f"  {v['id']}: {v['name']} (CVSS: {v['cvss_score']})")
    print(f"    Remedio: {v['remediation']}")
