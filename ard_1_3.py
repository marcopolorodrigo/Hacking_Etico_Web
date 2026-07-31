import re
from typing import List, Dict
from datetime import datetime

class FirewallLogAnalyzer:
    """
    Analizador de logs de firewall para detección de actividades sospechosas.
    """
    
    def __init__(self):
        self.logs = []
        self.alerts = []
    
    def add_log_entry(self, entry: Dict):
        """Añade una entrada de log"""
        self.logs.append(entry)
        self._analyze_entry(entry)
    
    def _analyze_entry(self, entry: Dict):
        """Analiza una entrada de log en busca de patrones sospechosos"""
        # Detectar múltiples intentos fallidos desde la misma IP
        if entry.get("action") == "DENY":
            self._check_brute_force(entry.get("source_ip", ""))
        
        # Detectar escaneo de puertos (múltiples puertos desde misma IP)
        if entry.get("action") == "DENY" and entry.get("protocol") in ["tcp", "udp"]:
            self._check_port_scan(entry.get("source_ip", ""))
    
    def _check_brute_force(self, source_ip: str):
        """Detecta posibles ataques de fuerza bruta"""
        attempts = [l for l in self.logs if l.get("source_ip") == source_ip and l.get("action") == "DENY"]
        if len(attempts) > 10:
            self.alerts.append({
                "type": "BRUTE_FORCE",
                "source_ip": source_ip,
                "attempts": len(attempts),
                "timestamp": datetime.now().isoformat(),
                "severity": "HIGH"
            })
    
    def _check_port_scan(self, source_ip: str):
        """Detecta posibles escaneos de puertos"""
        ports = set()
        for log in self.logs:
            if log.get("source_ip") == source_ip and log.get("action") == "DENY":
                ports.add(log.get("port"))
        if len(ports) > 20:
            self.alerts.append({
                "type": "PORT_SCAN",
                "source_ip": source_ip,
                "ports_scanned": len(ports),
                "timestamp": datetime.now().isoformat(),
                "severity": "MEDIUM"
            })
    
    def get_alerts(self) -> List[Dict]:
        return self.alerts
    
    def generate_report(self) -> Dict:
        return {
            "total_logs": len(self.logs),
            "alerts": len(self.alerts),
            "alert_details": self.alerts,
            "timestamp": datetime.now().isoformat()
        }

# Ejemplo de uso
analyzer = FirewallLogAnalyzer()

# Simular logs
logs = [
    {"source_ip": "203.0.113.5", "dest_ip": "192.168.1.10", "protocol": "tcp", "port": 22, "action": "DENY"},
    {"source_ip": "203.0.113.5", "dest_ip": "192.168.1.10", "protocol": "tcp", "port": 22, "action": "DENY"},
    {"source_ip": "203.0.113.5", "dest_ip": "192.168.1.10", "protocol": "tcp", "port": 22, "action": "DENY"},
    {"source_ip": "203.0.113.5", "dest_ip": "192.168.1.10", "protocol": "tcp", "port": 80, "action": "DENY"},
    {"source_ip": "203.0.113.5", "dest_ip": "192.168.1.10", "protocol": "tcp", "port": 443, "action": "DENY"},
]

for log in logs:
    analyzer.add_log_entry(log)

report = analyzer.generate_report()
print("📊 INFORME DE ANÁLISIS DE LOGS")
print(f"Total de logs: {report['total_logs']}")
print(f"Alertas: {report['alerts']}")

for alert in report['alert_details']:
    print(f"\n🚨 ALERTA: {alert['type']}")
    print(f"  IP origen: {alert['source_ip']}")
    print(f"  Severidad: {alert['severity']}")
