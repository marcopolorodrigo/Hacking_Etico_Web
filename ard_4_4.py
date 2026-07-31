import random
from typing import List, Dict, Optional
from datetime import datetime

class LoadBalancer:
    """
    Simulación de balanceo de carga (como HAProxy) en Python.
    """
    
    def __init__(self, algorithm: str = "round_robin"):
        self.servers: List[Dict] = []
        self.algorithm = algorithm
        self.current_index = 0
        self.stats = {"requests": 0, "servers": {}}
    
    def add_server(self, name: str, ip: str, port: int, weight: int = 1):
        self.servers.append({
            "name": name,
            "ip": ip,
            "port": port,
            "weight": weight,
            "connections": 0,
            "active": True
        })
        self.stats["servers"][name] = {"requests": 0}
    
    def get_next_server(self) -> Optional[Dict]:
        """Obtiene el siguiente servidor según el algoritmo de balanceo"""
        active_servers = [s for s in self.servers if s["active"]]
        if not active_servers:
            return None
        
        if self.algorithm == "round_robin":
            server = active_servers[self.current_index % len(active_servers)]
            self.current_index += 1
            return server
        
        elif self.algorithm == "least_connections":
            return min(active_servers, key=lambda s: s["connections"])
        
        elif self.algorithm == "random":
            return random.choice(active_servers)
        
        return active_servers[0]
    
    def route_request(self, request: Dict) -> Dict:
        """Enruta una solicitud a un servidor según el balanceo"""
        server = self.get_next_server()
        if not server:
            return {"error": "No hay servidores disponibles"}
        
        server["connections"] += 1
        self.stats["requests"] += 1
        self.stats["servers"][server["name"]]["requests"] += 1
        
        return {
            "server": server["name"],
            "ip": server["ip"],
            "port": server["port"],
            "timestamp": datetime.now().isoformat(),
            "algorithm": self.algorithm
        }
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas del balanceador"""
        return {
            "algorithm": self.algorithm,
            "total_requests": self.stats["requests"],
            "active_servers": len([s for s in self.servers if s["active"]]),
            "servers": [
                {
                    "name": s["name"],
                    "connections": s["connections"],
                    "active": s["active"],
                    "requests": self.stats["servers"].get(s["name"], {}).get("requests", 0)
                }
                for s in self.servers
            ]
        }

# Ejemplo de uso
lb = LoadBalancer(algorithm="round_robin")

# Añadir servidores
lb.add_server("web01", "10.0.0.1", 80, weight=1)
lb.add_server("web02", "10.0.0.2", 80, weight=1)
lb.add_server("web03", "10.0.0.3", 80, weight=2)

# Simular solicitudes
requests = [
    {"client": "192.168.1.10", "url": "/index.html"},
    {"client": "192.168.1.20", "url": "/about.html"},
    {"client": "192.168.1.30", "url": "/contact.html"},
    {"client": "192.168.1.40", "url": "/products.html"},
    {"client": "192.168.1.50", "url": "/index.html"},
]

print("⚖️ BALANCEO DE CARGA")
for req in requests:
    result = lb.route_request(req)
    print(f"Cliente {req['client']} -> {result['server']} ({result['ip']}:{result['port']})")

stats = lb.get_stats()
print(f"\n📊 ESTADÍSTICAS DEL BALANCEADOR")
print(f"  Total de solicitudes: {stats['total_requests']}")
print(f"  Servidores activos: {stats['active_servers']}")
for server in stats['servers']:
    print(f"  {server['name']}: {server['requests']} solicitudes, {server['connections']} conexiones activas")
