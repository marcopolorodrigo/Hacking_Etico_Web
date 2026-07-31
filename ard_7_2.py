import re
from typing import List, Dict
from datetime import datetime

class IncidentDetector:
    """
    Detector de incidentes en logs de pfSense.
    """
    
    def __init__(self):
        self.patterns = {
            "brute_force": re.compile(r"SSH authentication failure from (\d+\.\d+\.\d+\.\d+)"),
            "port_scan": re.compile(r"DENY.*from (\d+\.\d+\.\d+\.\d+) .*port (\d+)"),
            "ddos": re.compile(r"firewall: limit reached"),
            "suricata_alert": re.compile(r"Suricata alert \[(\d+:\d+:\d+)\] (.*?) from (\d+\.\d+\.\d+\.\d+)"),
            "vpn_attempt": re.compile(r"OpenVPN.*auth fail from (\d+\.\d+\.\d+\.\d+)"),
            "admin_access": re.compile(r"webConfigurator authentication success from (\d+\.\d+\.\d+\.\d+)")
        }
        self.incidents = []
    
    def analyze_log(self, log_entry: str) -> List[Dict]:
        """
        Analiza una entrada de log en busca de incidentes.
        """
        incidents = []
        
        for incident_type, pattern in self.patterns.items():
            match = pattern.search(log_entry)
            if match:
                incident = {
                    "type": incident_type,
                    "timestamp": datetime.now().isoformat(),
                    "raw": log_entry[:100],
                    "details": match.groups()
                }
                
                # Asignar severidad según tipo
                if incident_type in ["brute_force", "suricata_alert"]:
                    incident["severity"] = "HIGH"
                elif incident_type in ["ddos", "port_scan"]:
                    incident["severity"] = "MEDIUM"
                else:
                    incident["severity"] = "LOW"
                
                incidents.append(incident)
                self.incidents.append(incident)
        
        return incidents
    
    def get_incidents(self, severity: str = None) -> List[Dict]:
        """Obtiene incidentes filtrados por severidad"""
        if severity:
            return [i for i in self.incidents if i["severity"] == severity]
        return self.incidents
    
    def generate_report(self) -> Dict:
        """Genera un informe de detección de incidentes"""
        return {
            "total_incidents": len(self.incidents),
            "by_type": {
                t: len([i for i in self.incidents if i["type"] == t])
                for t in set(i["type"] for i in self.incidents)
            },
            "by_severity": {
                s: len([i for i in self.incidents if i["severity"] == s])
                for s in set(i["severity"] for i in self.incidents)
            },
            "incidents": self.incidents[-10:],  # Últimos 10
            "timestamp": datetime.now().isoformat()
        }

# Ejemplo de uso
detector = IncidentDetector()

# Simular logs de pfSense
logs = [
    "SSH authentication failure for user admin from 203.0.113.5",
    "DENY TCP from 198.51.100.10 port 54321 to 192.168.1.1 port 22",
    "firewall: limit reached for rule 10 (192.168.1.0/24 -> any)",
    "Suricata alert [1:2000001:1] ET SCAN Portscan Detected from 203.0.113.5",
    "webConfigurator authentication success from 192.168.1.100",
]

for log in logs:
    detector.analyze_log(log)

report = detector.generate_report()

print("📊 INFORME DE DETECCIÓN DE INCIDENTES")
print(f"Total de incidentes: {report['total_incidents']}")
print(f"Por tipo: {report['by_type']}")
print(f"Por severidad: {report['by_severity']}")

print("\n🚨 INCIDENTES RECIENTES:")
for incident in report['incidents']:
    print(f"  [{incident['severity']}] {incident['type']} - {incident['details']}")
