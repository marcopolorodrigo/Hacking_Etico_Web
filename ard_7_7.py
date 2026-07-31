import json
from typing import List, Dict
from datetime import datetime

class SIEMIntegration:
    """
    Simulación de integración de pfSense con SIEM.
    """
    
    def __init__(self, siem_url: str):
        self.siem_url = siem_url
        self.logs = []
    
    def send_log(self, log_entry: Dict) -> Dict:
        """
        Simula el envío de un log de pfSense al SIEM.
        """
        log_entry["timestamp"] = datetime.now().isoformat()
        self.logs.append(log_entry)
        
        # Simulación de análisis SIEM
        if log_entry.get("severity") in ["CRITICAL", "HIGH"]:
            return {
                "status": "ALERT",
                "message": f"Incidente crítico detectado en log: {log_entry.get('type')}",
                "alert_id": f"ALT-{len(self.logs)}"
            }
        else:
            return {
                "status": "OK",
                "message": "Log procesado correctamente"
            }
    
    def get_alerts(self) -> List[Dict]:
        """Obtiene las alertas generadas por el SIEM"""
        return [l for l in self.logs if l.get("severity") in ["CRITICAL", "HIGH"]]

# Ejemplo de uso
siem = SIEMIntegration("http://siem.empresa.com:9200")

# Simular logs de pfSense
logs = [
    {"type": "firewall", "severity": "HIGH", "message": "DENY TCP from 203.0.113.5 to 192.168.1.1:22"},
    {"type": "firewall", "severity": "LOW", "message": "PASS TCP from 192.168.1.100 to 8.8.8.8:53"},
    {"type": "ids", "severity": "CRITICAL", "message": "Suricata alert: ET SCAN Portscan Detected from 203.0.113.5"},
]

for log in logs:
    result = siem.send_log(log)
    print(f"Log: {log['type']} - {result['status']}: {result['message']}")

alerts = siem.get_alerts()
print(f"\n🚨 Alertas generadas: {len(alerts)}")
