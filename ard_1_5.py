from typing import List, Dict, Optional
import re
from datetime import datetime

class Signature:
    """Firma de ataque para IDS"""
    def __init__(self, id: str, name: str, pattern: str, severity: str, action: str = "ALERT"):
        self.id = id
        self.name = name
        self.pattern = re.compile(pattern, re.IGNORECASE)
        self.severity = severity
        self.action = action  # "ALERT", "BLOCK"

class SignatureBasedIDS:
    """
    Simulación de un IDS basado en firmas para entender el concepto.
    """
    
    def __init__(self):
        self.signatures: List[Signature] = []
        self.alerts = []
        self.blocked = []
    
    def add_signature(self, signature: Signature):
        self.signatures.append(signature)
    
    def analyze_packet(self, packet_data: str, src_ip: str, dest_ip: str) -> Dict:
        """
        Analiza un paquete en busca de firmas de ataque.
        """
        for sig in self.signatures:
            if sig.pattern.search(packet_data):
                alert = {
                    "timestamp": datetime.now().isoformat(),
                    "signature_id": sig.id,
                    "signature_name": sig.name,
                    "severity": sig.severity,
                    "source": src_ip,
                    "destination": dest_ip,
                    "action": sig.action,
                    "data_preview": packet_data[:100]
                }
                
                if sig.action == "BLOCK":
                    self.blocked.append(alert)
                else:
                    self.alerts.append(alert)
                
                return alert
        
        return {"status": "CLEAN"}
    
    def get_alerts(self) -> List[Dict]:
        return self.alerts
    
    def get_blocked(self) -> List[Dict]:
        return self.blocked
    
    def generate_report(self) -> Dict:
        return {
            "timestamp": datetime.now().isoformat(),
            "total_alerts": len(self.alerts),
            "total_blocked": len(self.blocked),
            "alerts": self.alerts,
            "blocked": self.blocked
        }

# Ejemplo de uso
ids = SignatureBasedIDS()

# Añadir firmas de ataque
ids.add_signature(Signature(
    id="S-001",
    name="SQL Injection Attempt",
    pattern=r"(\bSELECT\b.*\bFROM\b|\bUNION\b.*\bSELECT\b|'\s*OR\s*'1'\s*=\s*'1)",
    severity="HIGH",
    action="BLOCK"
))

ids.add_signature(Signature(
    id="S-002",
    name="XSS Attempt",
    pattern=r"<script.*?>|javascript:|onerror=|onload=",
    severity="MEDIUM",
    action="ALERT"
))

ids.add_signature(Signature(
    id="S-003",
    name="Command Injection",
    pattern=r";\s*(?:ls|cat|id|whoami|rm|echo)|`.*?`|\$\{.*?\}",
    severity="CRITICAL",
    action="BLOCK"
))

# Simular análisis de paquetes
packets = [
    ("GET /index.php?id=1' OR '1'='1 HTTP/1.1", "203.0.113.5", "192.168.1.10"),
    ("<script>alert('XSS')</script>", "203.0.113.6", "192.168.1.10"),
    ("normal traffic", "192.168.1.20", "10.0.0.1"),
]

for data, src, dest in packets:
    result = ids.analyze_packet(data, src, dest)
    if result.get("status") != "CLEAN":
        print(f"🚨 {result['signature_name']} - {result['action']} (desde {src})")

report = ids.generate_report()
print(f"\n📊 RESUMEN IDS")
print(f"Alertas: {report['total_alerts']}")
print(f"Bloqueados: {report['total_blocked']}")
