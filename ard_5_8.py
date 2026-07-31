from typing import List, Dict, Optional

class ServiceVulnerabilityScanner:
    """
    Simulación de escaneo de vulnerabilidades en servicios de red de pfSense.
    """
    
    def __init__(self):
        self.services = []
        self.vulnerabilities = []
    
    def add_service(self, name: str, port: int, protocol: str, version: str):
        self.services.append({
            "name": name,
            "port": port,
            "protocol": protocol,
            "version": version
        })
    
    def scan_services(self):
        """Escanea servicios en busca de vulnerabilidades conocidas"""
        # Vulnerabilidades simuladas
        vuln_db = {
            "OpenVPN": {
                "versions": ["2.4.0", "2.4.1"],
                "vulnerabilities": ["CVE-2020-15078 (Auth control channel)"],
                "severity": "HIGH"
            },
            "Unbound": {
                "versions": ["1.9.0", "1.9.1"],
                "vulnerabilities": ["CVE-2019-16866 (DoS via malformed packet)"],
                "severity": "MEDIUM"
            },
            "SSH": {
                "versions": ["OpenSSH 7.4"],
                "vulnerabilities": ["CVE-2017-15906 (User enumeration)"],
                "severity": "LOW"
            }
        }
        
        for service in self.services:
            if service["name"] in vuln_db:
                vuln_info = vuln_db[service["name"]]
                if service["version"] in vuln_info["versions"]:
                    self.vulnerabilities.append({
                        "service": service["name"],
                        "version": service["version"],
                        "vulnerabilities": vuln_info["vulnerabilities"],
                        "severity": vuln_info["severity"],
                        "port": service["port"]
                    })
    
    def get_results(self) -> Dict:
        """Obtiene los resultados del escaneo de servicios"""
        return {
            "total_services": len(self.services),
            "vulnerable_services": len(self.vulnerabilities),
            "vulnerabilities": self.vulnerabilities,
            "recommendations": [
                "Actualizar servicios a versiones seguras",
                "Cerrar puertos innecesarios",
                "Aplicar parches de seguridad"
            ]
        }

# Ejemplo de uso
scanner = ServiceVulnerabilityScanner()

# Servicios en pfSense (simulados)
scanner.add_service("OpenVPN", 1194, "UDP", "2.4.0")
scanner.add_service("Unbound", 53, "UDP", "1.9.1")
scanner.add_service("SSH", 22, "TCP", "OpenSSH 7.4")
scanner.add_service("NTP", 123, "UDP", "4.2.8")

scanner.scan_services()
results = scanner.get_results()

print("📊 INFORME DE VULNERABILIDADES EN SERVICIOS")
print(f"Total de servicios: {results['total_services']}")
print(f"Servicios vulnerables: {results['vulnerable_services']}")

print("\n🚨 VULNERABILIDADES ENCONTRADAS:")
for v in results['vulnerabilities']:
    print(f"  {v['service']} (puerto {v['port']}) - {v['version']}")
    print(f"    Severidad: {v['severity']}")
    for vuln in v['vulnerabilities']:
        print(f"      {vuln}")
