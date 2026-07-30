from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class Vulnerability:
    """Representa una vulnerabilidad encontrada durante un pentesting"""
    id: str
    title: str
    description: str
    severity: str  # "CRITICAL", "HIGH", "MEDIUM", "LOW"
    affected_service: str
    cvss_score: float
    poc: Optional[str] = None
    mitigation: Optional[str] = None

class EthicalHacker:
    """
    Simulación de un flujo de trabajo de hacking ético.
    """
    
    def __init__(self, name: str, certification: str, tools: List[str]):
        self.name = name
        self.certification = certification
        self.tools = tools
        self.authorizations = []
        self.findings: List[Vulnerability] = []
    
    def authorize_test(self, target: str, scope: str, 
                       signed_consent: bool) -> bool:
        """Obtiene autorización para realizar pruebas de penetración"""
        if not signed_consent:
            print(f"⚠️ {self.name}: No se puede proceder sin consentimiento firmado.")
            return False
        
        authorization = {
            "target": target,
            "scope": scope,
            "date": datetime.now().isoformat(),
            "status": "AUTHORIZED"
        }
        self.authorizations.append(authorization)
        print(f"✅ {self.name}: Autorización concedida para {target}")
        return True
    
    def recon(self, target: str) -> Dict:
        """Fase de reconocimiento (simulación)"""
        print(f"🔍 {self.name}: Realizando reconocimiento en {target}...")
        return {
            "open_ports": [22, 80, 443, 3306, 8080],
            "services": {"22": "SSH", "80": "HTTP", "443": "HTTPS", 
                        "3306": "MySQL", "8080": "Tomcat"},
            "os": "Ubuntu 22.04",
            "domain": "example.com"
        }
    
    def scan(self, target: str, services: Dict) -> List[Vulnerability]:
        """Fase de escaneo de vulnerabilidades (simulación)"""
        print(f"🔎 {self.name}: Escaneando vulnerabilidades...")
        vulnerabilities = [
            Vulnerability(
                id="VULN-001",
                title="SQL Injection en formulario de login",
                description="El formulario de login es vulnerable a SQL injection.",
                severity="HIGH",
                affected_service="HTTP",
                cvss_score=7.5,
                poc="' OR '1'='1 --",
                mitigation="Usar consultas parametrizadas con ORM."
            ),
            Vulnerability(
                id="VULN-002",
                title="SSH vulnerabilidad de credenciales débiles",
                description="El servidor SSH permite autenticación por contraseña débil.",
                severity="MEDIUM",
                affected_service="SSH",
                cvss_score=5.0,
                poc="hydra -l root -P rockyou.txt ssh://target",
                mitigation="Implementar autenticación por clave pública."
            )
        ]
        self.findings.extend(vulnerabilities)
        return vulnerabilities
    
    def exploit(self, vulnerability: Vulnerability) -> bool:
        """Fase de explotación (simulación)"""
        print(f"💥 {self.name}: Intentando explotar {vulnerability.title}...")
        if vulnerability.severity in ["CRITICAL", "HIGH"]:
            print(f"✅ Explotación exitosa en {vulnerability.affected_service}")
            return True
        else:
            print(f"⚠️ Explotación no viable o de bajo riesgo")
            return False
    
    def report(self) -> Dict:
        """Genera un informe de hallazgos"""
        return {
            "hacker": self.name,
            "certification": self.certification,
            "tools": self.tools,
            "authorizations": self.authorizations,
            "findings": [{"id": f.id, "title": f.title, 
                         "severity": f.severity, 
                         "cvss": f.cvss_score} for f in self.findings],
            "summary": {
                "total_findings": len(self.findings),
                "critical": len([f for f in self.findings if f.severity == "CRITICAL"]),
                "high": len([f for f in self.findings if f.severity == "HIGH"]),
                "medium": len([f for f in self.findings if f.severity == "MEDIUM"]),
                "low": len([f for f in self.findings if f.severity == "LOW"])
            }
        }

# Ejemplo de uso
hacker = EthicalHacker(
    name="María Gómez",
    certification="OSCP",
    tools=["Nmap", "Metasploit", "Burp Suite", "Garak"]
)

# Obtener autorización
consent = hacker.authorize_test(
    target="192.168.1.100",
    scope="Red interna y aplicaciones web",
    signed_consent=True
)

# Realizar pentesting
if consent:
    recon = hacker.recon("192.168.1.100")
    vulns = hacker.scan("192.168.1.100", recon["services"])
    for v in vulns:
        hacker.exploit(v)
    
    # Generar informe
    report = hacker.report()
    print("\n📄 INFORME DE PENTESTING")
    print(f"Hallazgos totales: {report['summary']['total_findings']}")
    print(f"Críticos: {report['summary']['critical']}")
    print(f"Altos: {report['summary']['high']}")
