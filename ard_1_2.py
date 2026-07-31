from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum

class Protocol(Enum):
    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"

@dataclass
class FirewallRule:
    """Regla de firewall para autorización de tráfico"""
    id: str
    source: str  # IP o red
    destination: str  # IP o red
    protocol: Protocol
    port: Optional[int] = None
    action: str = "ALLOW"  # "ALLOW" o "DENY"
    description: str = ""

class FirewallAuthorizer:
    """
    Simulación de autorización de tráfico basada en reglas de firewall.
    """
    
    def __init__(self):
        self.rules: List[FirewallRule] = []
        self.log = []
    
    def add_rule(self, rule: FirewallRule):
        self.rules.append(rule)
    
    def check_traffic(self, source_ip: str, dest_ip: str, 
                      protocol: Protocol, port: int) -> Dict:
        """
        Verifica si el tráfico está autorizado según las reglas.
        """
        # Buscar regla que coincida
        for rule in self.rules:
            if (rule.source == source_ip or rule.source == "ANY") and \
               (rule.destination == dest_ip or rule.destination == "ANY") and \
               rule.protocol == protocol and \
               (rule.port is None or rule.port == port):
                
                self.log.append({
                    "source": source_ip,
                    "destination": dest_ip,
                    "protocol": protocol.value,
                    "port": port,
                    "action": rule.action,
                    "rule": rule.id,
                    "timestamp": datetime.now().isoformat()
                })
                
                return {
                    "allowed": rule.action == "ALLOW",
                    "rule_id": rule.id,
                    "action": rule.action,
                    "description": rule.description
                }
        
        # Si no hay regla, denegar por defecto
        self.log.append({
            "source": source_ip,
            "destination": dest_ip,
            "protocol": protocol.value,
            "port": port,
            "action": "DENY",
            "rule": "DEFAULT_DENY",
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "allowed": False,
            "rule_id": "DEFAULT_DENY",
            "action": "DENY",
            "description": "Denegado por defecto (no hay regla que coincida)"
        }
    
    def get_log(self) -> List[Dict]:
        return self.log

# Ejemplo de uso
authorizer = FirewallAuthorizer()

# Añadir reglas
authorizer.add_rule(FirewallRule(
    id="R-001",
    source="192.168.1.0/24",
    destination="10.0.0.1",
    protocol=Protocol.TCP,
    port=80,
    action="ALLOW",
    description="Permitir HTTP desde LAN a servidor web"
))

authorizer.add_rule(FirewallRule(
    id="R-002",
    source="ANY",
    destination="10.0.0.1",
    protocol=Protocol.TCP,
    port=22,
    action="DENY",
    description="Denegar SSH desde cualquier origen al servidor"
))

# Verificar tráfico
traffic1 = authorizer.check_traffic("192.168.1.10", "10.0.0.1", Protocol.TCP, 80)
traffic2 = authorizer.check_traffic("192.168.2.10", "10.0.0.1", Protocol.TCP, 22)

print("📋 VERIFICACIÓN DE AUTORIZACIÓN")
print(f"Tráfico HTTP: {'✅ PERMITIDO' if traffic1['allowed'] else '❌ DENEGADO'} - {traffic1['description']}")
print(f"Tráfico SSH: {'✅ PERMITIDO' if traffic2['allowed'] else '❌ DENEGADO'} - {traffic2['description']}")
