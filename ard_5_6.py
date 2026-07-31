from datetime import datetime
import random

class VulnerabilityScan:
    """
    Simulación de un escaneo de vulnerabilidades con OpenVAS para redes con pfSense.
    """
    
    def __init__(self, target: str):
        self.target = target
        self.results = []
        self._simulate_scan()
    
    def _simulate_scan(self):
        """Simula los resultados de un escaneo de vulnerabilidades"""
        # Vulnerabilidades simuladas en una red con pfSense
        vulnerabilities = [
            {"name": "pfSense vulnerable a CVE-2026-1234", "severity": "CRITICAL", "cvss": 9.8, "port": 443},
            {"name": "Puerto SSH expuesto a Internet", "severity": "HIGH", "cvss": 7.5, "port": 22},
            {"name": "TLS 1.0 habilitado en HTTPS", "severity": "MEDIUM", "cvss": 5.0, "port": 443},
            {"name": "Suricata con firmas obsoletas", "severity": "HIGH", "cvss": 7.0, "port": None},
            {"name": "Falta de MFA en usuario admin", "severity": "HIGH", "cvss": 8.0, "port": 443},
            {"name": "Puerto 21 (FTP) abierto innecesariamente", "severity": "MEDIUM", "cvss": 5.5, "port": 21},
        ]
        
        # Simular aleatoriedad en los resultados
        for vuln in vulnerabilities:
            if random.random() < 0.8:  # 80% de probabilidad de encontrar cada vulnerabilidad
                self.results.append({
                    "name": vuln["name"],
                    "severity": vuln["severity"],
                    "cvss_score": vuln["cvss"],
                    "port": vuln["port"],
                    "description": f"{vuln['name']} detectada en el escaneo de {self.target}",
                    "remediation": self._get_remediation(vuln["name"])
                })
    
    def _get_remediation(self, vuln_name: str) -> str:
        """Obtiene la recomendación de remediación para una vulnerabilidad"""
        remediations = {
            "pfSense vulnerable a CVE-2026-1234": "Actualizar pfSense a la última versión estable que incluya el parche",
            "Puerto SSH expuesto a Internet": "Cerrar el puerto SSH o limitar el acceso a IPs autorizadas",
            "TLS 1.0 habilitado en HTTPS": "Configurar pfSense para usar TLS 1.2 o TLS 1.3 exclusivamente",
            "Suricata con firmas obsoletas": "Configurar actualización automática de reglas de Suricata",
            "Falta de MFA en usuario admin": "Habilitar MFA para el usuario admin de pfSense",
            "Puerto 21 (FTP) abierto innecesariamente": "Cerrar el puerto FTP si no es necesario, o migrar a SFTP"
        }
        return remediations.get(vuln_name, "Consultar documentación de pfSense para la mitigación")
    
    def get_results(self) -> List[Dict]:
        return self.results
    
    def get_summary(self) -> Dict:
        """Obtiene un resumen del escaneo de vulnerabilidades"""
        severity_counts = {}
        for result in self.results:
            severity_counts[result["severity"]] = severity_counts.get(result["severity"], 0) + 1
        
        return {
            "target": self.target,
            "total_vulnerabilities": len(self.results),
            "by_severity": severity_counts,
            "results": self.results,
            "scan_date": datetime.now().isoformat()
        }

# Ejemplo de uso
scan = VulnerabilityScan("192.168.1.1 (pfSense)")
summary = scan.get_summary()

print("📊 INFORME DE ESCANEO DE VULNERABILIDADES")
print(f"Objetivo: {summary['target']}")
print(f"Total de vulnerabilidades: {summary['total_vulnerabilities']}")
print(f"Por severidad: {summary['by_severity']}")

print("\n📋 VULNERABILIDADES DETECTADAS:")
for v in summary['results']:
    print(f"  [{v['severity']}] {v['name']} (CVSS: {v['cvss_score']})")
    if v['port']:
        print(f"    Puerto: {v['port']}")
    print(f"    Remedio: {v['remediation']}")
