import re
from typing import List, Dict
from datetime import datetime

class LogAnalyzer:
    """
    Analizador de logs de pfSense para detección de vulnerabilidades y ataques.
    """
    
    def __init__(self):
        self.logs = []
        self.alerts = []
    
    def add_log_entry(self, entry: str):
        """Añade una entrada de log y la analiza"""
        self.logs.append(entry)
        self._analyze_entry(entry)
    
    def _analyze_entry(self, entry: str):
        """Analiza una entrada de log en busca de patrones sospechosos"""
        # Detectar intentos de autenticación fallidos (fuerza bruta)
        if "SSH" in entry and "authentication failure" in entry:
            ip = re.search(r'from (\d+\.\d+\.\d+\.\d+)', entry)
            if ip:
                self.alerts.append({
                    "type": "BRUTE_FORCE_ATTEMPT",
                    "ip": ip.group(1),
                    "timestamp": datetime.now().isoformat(),
                    "severity": "HIGH"
                })
        
        # Detectar escaneos de puertos (tráfico bloqueado)
        if "DENY" in entry and "TCP" in entry:
            port = re.search(r'port (\d+)', entry)
            source = re.search(r'source (\d+\.\d+\.\d+\.\d+)', entry)
            if port and source:
                self.alerts.append({
                    "type": "PORT_SCAN",
                    "source": source.group(1),
                    "port": int(port.group(1)),
                    "timestamp": datetime.now().isoformat(),
                    "severity": "MEDIUM"
                })
        
        # Detectar alertas de Suricata (IDS/IPS)
        if "Suricata" in entry and "alert" in entry:
            signature = re.search(r'\[(\d+):\d+:\d+\] (.*?)\s', entry)
            if signature:
                self.alerts.append({
                    "type": "IDS_ALERT",
                    "signature_id": signature.group(1),
                    "signature": signature.group(2),
                    "timestamp": datetime.now().isoformat(),
                    "severity": "HIGH"
                })
    
    def get_alerts(self) -> List[Dict]:
        return self.alerts
    
    def get_summary(self) -> Dict:
        """Obtiene un resumen de las alertas"""
        severity_counts = {}
        for alert in self.alerts:
            severity_counts[alert["severity"]] = severity_counts.get(alert["severity"], 0) + 1
        
        return {
            "total_logs": len(self.logs),
            "total_alerts": len(self.alerts),
            "by_severity": severity_counts,
            "alerts": self.alerts
        }

# Ejemplo de uso
analyzer = LogAnalyzer()

# Simular logs de pfSense
logs = [
    "SSH authentication failure for user admin from 203.0.113.5",
    "SSH authentication failure for user root from 203.0.113.5",
    "DENY TCP from 198.51.100.10 port 54321 to 192.168.1.1 port 22",
    "Suricata alert [2000001:1] ET SCAN Portscan Detected from 203.0.113.5",
    "SSH authentication failure for user admin from 203.0.113.5",
]

for log in logs:
    analyzer.add_log_entry(log)

summary = analyzer.get_summary()

print("📊 INFORME DE ANÁLISIS DE LOGS")
print(f"Total de logs: {summary['total_logs']}")
print(f"Alertas generadas: {summary['total_alerts']}")
print(f"Por severidad: {summary['by_severity']}")

print("\n🚨 ALERTAS DETECTADAS:")
for alert in summary['alerts']:
    print(f"  [{alert['severity']}] {alert['type']} - {alert.get('ip') or alert.get('source') or alert.get('signature')}")
