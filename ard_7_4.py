import re
from typing import List, Dict
from datetime import datetime

class PFLogForensics:
    """
    Análisis forense de logs de pfSense.
    """
    
    def __init__(self):
        self.logs = []
        self.findings = []
    
    def load_logs(self, log_entries: List[str]):
        self.logs = log_entries
    
    def analyze(self) -> List[Dict]:
        """
        Analiza los logs en busca de evidencia forense.
        """
        findings = []
        
        for log in self.logs:
            finding = self._analyze_entry(log)
            if finding:
                findings.append(finding)
        
        self.findings = findings
        return findings
    
    def _analyze_entry(self, log_entry: str) -> Dict:
        """
        Analiza una entrada de log para extraer evidencia.
        """
        # Buscar eventos de autenticación
        if "authentication" in log_entry:
            return {
                "type": "AUTHENTICATION",
                "timestamp": self._extract_timestamp(log_entry),
                "user": self._extract_user(log_entry),
                "source_ip": self._extract_ip(log_entry),
                "details": log_entry[:100]
            }
        
        # Buscar eventos de firewall
        if "DENY" in log_entry or "PASS" in log_entry:
            return {
                "type": "FIREWALL",
                "timestamp": self._extract_timestamp(log_entry),
                "action": "DENY" if "DENY" in log_entry else "PASS",
                "source_ip": self._extract_ip(log_entry),
                "destination_ip": self._extract_dest_ip(log_entry),
                "details": log_entry[:100]
            }
        
        # Buscar eventos de Suricata
        if "Suricata" in log_entry:
            return {
                "type": "IDS_ALERT",
                "timestamp": self._extract_timestamp(log_entry),
                "signature": self._extract_signature(log_entry),
                "source_ip": self._extract_ip(log_entry),
                "details": log_entry[:100]
            }
        
        return None
    
    def _extract_timestamp(self, log: str) -> str:
        # Simulación de extracción de timestamp
        return datetime.now().isoformat()
    
    def _extract_ip(self, log: str) -> str:
        ip_pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+)')
        match = ip_pattern.search(log)
        return match.group(1) if match else "Unknown"
    
    def _extract_dest_ip(self, log: str) -> str:
        # Simulación
        return "192.168.1.1"
    
    def _extract_user(self, log: str) -> str:
        user_pattern = re.compile(r'user (\w+)')
        match = user_pattern.search(log)
        return match.group(1) if match else "Unknown"
    
    def _extract_signature(self, log: str) -> str:
        sig_pattern = re.compile(r'\[.*?\] (.*?) from')
        match = sig_pattern.search(log)
        return match.group(1) if match else "Unknown"
    
    def generate_timeline(self) -> List[Dict]:
        """
        Genera una línea de tiempo de eventos.
        """
        timeline = sorted(self.findings, key=lambda x: x["timestamp"])
        return timeline

# Ejemplo de uso
forensics = PFLogForensics()

# Simular logs
logs = [
    "2026-07-21 14:30:00 SSH authentication failure for user admin from 203.0.113.5",
    "2026-07-21 14:31:00 DENY TCP from 203.0.113.5 port 54321 to 192.168.1.1 port 22",
    "2026-07-21 14:32:00 Suricata alert [1:2000001:1] ET SCAN Portscan Detected from 203.0.113.5",
    "2026-07-21 14:35:00 webConfigurator authentication success from 192.168.1.100",
]

forensics.load_logs(logs)
findings = forensics.analyze()
timeline = forensics.generate_timeline()

print("🔍 ANÁLISIS FORENSE DE LOGS")
print(f"Hallazgos: {len(findings)}")
print("\n📅 LÍNEA DE TIEMPO:")
for event in timeline:
    print(f"  [{event['timestamp']}] {event['type']} - {event.get('details', '')[:50]}")
