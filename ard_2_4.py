import re
from typing import Dict, List


class HTTPInspector:
    """
    Simulación de inspección HTTP para IDS/IPS.
    """

    def __init__(self):
        self.patterns = {
            "sql_injection": re.compile(
                r"(\bSELECT\b.*\bFROM\b|\bUNION\b.*\bSELECT\b|'\s*OR\s*'1'\s*=\s*'1)",
                re.IGNORECASE,
            ),
            "xss": re.compile(
                r"<script.*?>|javascript:|onerror=|onload=",
                re.IGNORECASE,
            ),
            "path_traversal": re.compile(
                r"\.\./|\.\.\\",
                re.IGNORECASE,
            ),
            "command_injection": re.compile(
                r";\s*(?:ls|cat|id|whoami|rm|echo)|`.*?`",
                re.IGNORECASE,
            ),
        }
        self.alerts = []

    def inspect_request(self, method: str, uri: str, body: str = "") -> Dict:
        """
        Inspecciona una solicitud HTTP en busca de ataques.
        """
        alerts = []
        full_request = f"{method} {uri} {body}"

        for attack_type, pattern in self.patterns.items():
            if pattern.search(full_request):
                alerts.append({
                    "attack_type": attack_type,
                    "pattern": pattern.pattern,
                    "severity": "HIGH" if attack_type in ["sql_injection", "command_injection"] else "MEDIUM",
                    "method": method,
                    "uri": uri[:50],
                })

        self.alerts.extend(alerts)

        return {
            "status": "CLEAN" if not alerts else "ATTACK_DETECTED",
            "alerts": alerts,
            "method": method,
            "uri": uri[:50],
        }

    def get_alerts(self) -> List[Dict]:
        return self.alerts


# Ejemplo de uso
inspector = HTTPInspector()

requests = [
    ("GET", "/index.php?id=1", ""),
    ("GET", "/search?q=' OR '1'='1", ""),
    ("GET", "/page.html", ""),
    ("POST", "/login", "username=admin'--"),
    ("GET", "<script>alert('XSS')</script>", ""),
]

for method, uri, body in requests:
    result = inspector.inspect_request(method, uri, body)
    if result["status"] == "ATTACK_DETECTED":
        print(f"🚨 ATAQUE DETECTADO en {result['method']} {result['uri']}")
        for alert in result["alerts"]:
            print(f"  [{alert['severity']}] {alert['attack_type']}")

print(f"\n📊 Alertas totales: {len(inspector.get_alerts())}")