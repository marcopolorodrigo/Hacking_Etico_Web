from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime
import hashlib

@dataclass
class Connection:
    """Representa una conexión de red stateful"""
    id: str
    protocol: str
    src_ip: str
    src_port: int
    dest_ip: str
    dest_port: int
    state: str  # "NEW", "ESTABLISHED", "CLOSED"
    created: datetime
    bytes_sent: int = 0
    bytes_recv: int = 0

class StatefulFirewall:
    """
    Simulación de un firewall stateful para entender el concepto de seguimiento de estado.
    """
    
    def __init__(self):
        self.connections: Dict[str, Connection] = {}
        self.rules = []
        self.log = []
    
    def add_rule(self, rule: Dict):
        self.rules.append(rule)
    
    def _get_connection_id(self, protocol: str, src_ip: str, src_port: int,
                           dest_ip: str, dest_port: int) -> str:
        """Genera un ID único para una conexión"""
        key = f"{protocol}|{src_ip}|{src_port}|{dest_ip}|{dest_port}"
        return hashlib.md5(key.encode()).hexdigest()[:16]
    
    def process_packet(self, protocol: str, src_ip: str, src_port: int,
                       dest_ip: str, dest_port: int, payload: bytes) -> Dict:
        """
        Procesa un paquete de red con seguimiento de estado.
        """
        conn_id = self._get_connection_id(protocol, src_ip, src_port, dest_ip, dest_port)
        
        # Verificar si es una conexión nueva o existente
        if conn_id not in self.connections:
            # Nueva conexión
            conn = Connection(
                id=conn_id,
                protocol=protocol,
                src_ip=src_ip,
                src_port=src_port,
                dest_ip=dest_ip,
                dest_port=dest_port,
                state="NEW",
                created=datetime.now()
            )
            self.connections[conn_id] = conn
            
            # Verificar reglas para nueva conexión
            allowed = self._check_rules(protocol, src_ip, dest_ip, dest_port)
            if not allowed:
                conn.state = "CLOSED"
                return self._log_packet(protocol, src_ip, dest_ip, dest_port, "DENY")
        else:
            # Conexión existente
            conn = self.connections[conn_id]
            if conn.state == "CLOSED":
                return self._log_packet(protocol, src_ip, dest_ip, dest_port, "DENY")
            
            # Actualizar estado de la conexión
            if conn.state == "NEW":
                conn.state = "ESTABLISHED"
        
        # Procesar paquete
        conn.bytes_sent += len(payload)
        
        return self._log_packet(protocol, src_ip, dest_ip, dest_port, "ALLOW")
    
    def _check_rules(self, protocol: str, src_ip: str, dest_ip: str, dest_port: int) -> bool:
        """Verifica si el tráfico está permitido por las reglas"""
        for rule in self.rules:
            if (rule.get("source") == "ANY" or rule.get("source") == src_ip) and \
               (rule.get("destination") == "ANY" or rule.get("destination") == dest_ip) and \
               rule.get("protocol") == protocol and \
               (rule.get("port") is None or rule.get("port") == dest_port):
                return rule.get("action") == "ALLOW"
        return False
    
    def _log_packet(self, protocol: str, src_ip: str, dest_ip: str,
                    dest_port: int, action: str) -> Dict:
        """Registra el procesamiento del paquete"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "protocol": protocol,
            "source": src_ip,
            "destination": dest_ip,
            "port": dest_port,
            "action": action
        }
        self.log.append(log_entry)
        return log_entry
    
    def get_connections(self) -> List[Dict]:
        """Obtiene el estado de todas las conexiones activas"""
        return [
            {
                "id": c.id,
                "protocol": c.protocol,
                "src": f"{c.src_ip}:{c.src_port}",
                "dest": f"{c.dest_ip}:{c.dest_port}",
                "state": c.state,
                "bytes": c.bytes_sent + c.bytes_recv
            }
            for c in self.connections.values() if c.state != "CLOSED"
        ]

# Ejemplo de uso
fw = StatefulFirewall()

# Añadir reglas
fw.add_rule({"source": "192.168.1.0/24", "destination": "ANY", "protocol": "tcp", "port": 80, "action": "ALLOW"})
fw.add_rule({"source": "ANY", "destination": "10.0.0.1", "protocol": "tcp", "port": 22, "action": "DENY"})

# Procesar paquetes
packets = [
    ("tcp", "192.168.1.10", 12345, "10.0.0.1", 80, b"GET / HTTP/1.1"),
    ("tcp", "192.168.1.10", 12346, "10.0.0.1", 22, b"SSH Connection"),
]

for pkt in packets:
    result = fw.process_packet(*pkt)
    print(f"Paquete {pkt[4]} -> {result['action']}")

print(f"\nConexiones activas: {len(fw.get_connections())}")
