from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class FirewallRule:
    """Representa una regla de firewall en pfSense"""
    id: int
    action: str  # "pass", "block", "reject"
    protocol: str  # "tcp", "udp", "icmp", "any"
    source: str  # "any", "IP", "network", "alias"
    destination: str  # "any", "IP", "network", "alias"
    dest_port: Optional[int] = None
    log: bool = False
    description: str = ""

class RuleProcessor:
    """
    Simulación de procesamiento de reglas de firewall en pfSense.
    """
    
    def __init__(self, default_action: str = "deny"):
        self.rules: List[FirewallRule] = []
        self.default_action = default_action
        self.log = []
    
    def add_rule(self, rule: FirewallRule):
        self.rules.append(rule)
    
    def match(self, rule: FirewallRule, protocol: str, src_ip: str, dest_ip: str, dest_port: int) -> bool:
        """Verifica si una regla coincide con un paquete"""
        if rule.protocol != "any" and rule.protocol != protocol:
            return False
        
        if rule.source != "any" and rule.source != src_ip:
            return False
        
        if rule.destination != "any" and rule.destination != dest_ip:
            return False
        
        if rule.dest_port is not None and rule.dest_port != dest_port:
            return False
        
        return True
    
    def process_packet(self, protocol: str, src_ip: str, dest_ip: str, dest_port: int) -> Dict:
        """
        Procesa un paquete evaluando las reglas en orden.
        """
        action = None
        matched_rule = None
        
        for rule in self.rules:
            if self.match(rule, protocol, src_ip, dest_ip, dest_port):
                action = rule.action
                matched_rule = rule
                break
        
        if action is None:
            action = self.default_action
        
        # Registrar el procesamiento
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "protocol": protocol,
            "source": src_ip,
            "destination": dest_ip,
            "port": dest_port,
            "action": action,
            "rule": matched_rule.description if matched_rule else "default"
        }
        self.log.append(log_entry)
        
        return {
            "action": action,
            "rule": matched_rule.description if matched_rule else "default",
            "allowed": action in ["pass", "allow"]
        }

# Ejemplo de uso
processor = RuleProcessor(default_action="deny")

# Añadir reglas
processor.add_rule(FirewallRule(id=1, action="pass", protocol="tcp", source="192.168.1.0/24", destination="any", dest_port=80, log=True, description="HTTP desde LAN"))
processor.add_rule(FirewallRule(id=2, action="block", protocol="tcp", source="any", destination="10.0.0.1", dest_port=22, log=True, description="Bloquear SSH al servidor"))

# Procesar paquetes
packets = [
    ("tcp", "192.168.1.10", "10.0.0.1", 80),
    ("tcp", "192.168.1.10", "10.0.0.1", 22),
    ("udp", "192.168.1.10", "10.0.0.1", 53),
]

for proto, src, dest, port in packets:
    result = processor.process_packet(proto, src, dest, port)
    print(f"{proto} {src} -> {dest}:{port} -> {result['action']} (Regla: {result['rule']})")
