from typing import List, Dict, Optional
from datetime import datetime
import time

class FirewallNode:
    """Representa un nodo de firewall en un clúster HA"""
    def __init__(self, name: str, ip: str, priority: int):
        self.name = name
        self.ip = ip
        self.priority = priority
        self.status = "BACKUP"  # "MASTER" o "BACKUP"
        self.last_heartbeat = datetime.now()
        self.connections = []
    
    def send_heartbeat(self) -> bool:
        """Simula el envío de latido"""
        self.last_heartbeat = datetime.now()
        return True
    
    def is_alive(self) -> bool:
        """Verifica si el nodo está vivo"""
        return (datetime.now() - self.last_heartbeat).seconds < 5

class CARPCluster:
    """
    Simulación de un clúster HA con CARP en pfSense.
    """
    
    def __init__(self, vip: str):
        self.vip = vip
        self.nodes: List[FirewallNode] = []
        self.master = None
        self.events = []
    
    def add_node(self, node: FirewallNode):
        self.nodes.append(node)
    
    def _elect_master(self):
        """Elige el nodo maestro basado en prioridad"""
        alive_nodes = [n for n in self.nodes if n.is_alive()]
        if not alive_nodes:
            return
        
        # Elegir el nodo con mayor prioridad
        self.master = max(alive_nodes, key=lambda n: n.priority)
        self.master.status = "MASTER"
        for n in alive_nodes:
            if n != self.master:
                n.status = "BACKUP"
        
        self.events.append({
            "timestamp": datetime.now().isoformat(),
            "event": "MASTER_ELECTION",
            "master": self.master.name,
            "vip": self.vip
        })
    
    def handle_node_failure(self, node_name: str):
        """Maneja la falla de un nodo"""
        node = next((n for n in self.nodes if n.name == node_name), None)
        if node:
            node.status = "FAILED"
            self.events.append({
                "timestamp": datetime.now().isoformat(),
                "event": "NODE_FAILURE",
                "node": node_name
            })
            self._elect_master()
    
    def get_status(self) -> Dict:
        """Obtiene el estado del clúster"""
        return {
            "vip": self.vip,
            "master": self.master.name if self.master else None,
            "nodes": [
                {
                    "name": n.name,
                    "ip": n.ip,
                    "status": n.status,
                    "priority": n.priority,
                    "alive": n.is_alive()
                }
                for n in self.nodes
            ],
            "events": self.events[-5:]  # Últimos 5 eventos
        }

# Ejemplo de uso
cluster = CARPCluster("192.168.1.1")

# Añadir nodos
cluster.add_node(FirewallNode("fw01", "192.168.1.11", 100))
cluster.add_node(FirewallNode("fw02", "192.168.1.12", 90))
cluster.add_node(FirewallNode("fw03", "192.168.1.13", 80))

# Elegir maestro inicial
cluster._elect_master()

# Simular falla del nodo maestro
print("✅ Clúster HA inicializado")
status = cluster.get_status()
print(f"VIP: {status['vip']}")
print(f"Maestro: {status['master']}")

print("\n⚠️ Simulando falla del nodo maestro...")
cluster.handle_node_failure("fw01")

status = cluster.get_status()
print(f"Nuevo maestro: {status['master']}")
print(f"Eventos: {len(status['events'])}")
