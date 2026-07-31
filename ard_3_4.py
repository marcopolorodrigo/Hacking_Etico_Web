class NATSimulator:
    """
    Simulación de NAT (SNAT y DNAT) para entender el concepto.
    """
    
    def __init__(self, public_ip: str):
        self.public_ip = public_ip
        self.nat_table = {}  # mapping: (src_ip, src_port) -> (internal_ip, internal_port)
        self.port_forwarding_rules = []
    
    def add_port_forwarding(self, external_port: int, internal_ip: str, internal_port: int):
        """Añade una regla de port forwarding (DNAT)"""
        self.port_forwarding_rules.append({
            "external_port": external_port,
            "internal_ip": internal_ip,
            "internal_port": internal_port
        })
    
    def translate_egress(self, src_ip: str, src_port: int, dest_ip: str, dest_port: int) -> Dict:
        """
        Traduce un paquete saliente (SNAT).
        """
        # Simular asignación de puerto NAT
        nat_port = src_port  # En la práctica, se asignaría un puerto aleatorio
        self.nat_table[(src_ip, src_port)] = (self.public_ip, nat_port)
        
        return {
            "original": {"src": f"{src_ip}:{src_port}", "dest": f"{dest_ip}:{dest_port}"},
            "translated": {"src": f"{self.public_ip}:{nat_port}", "dest": f"{dest_ip}:{dest_port}"}
        }
    
    def translate_ingress(self, src_ip: str, src_port: int, dest_ip: str, dest_port: int) -> Dict:
        """
        Traduce un paquete entrante (DNAT / Port Forwarding).
        """
        for rule in self.port_forwarding_rules:
            if rule["external_port"] == dest_port:
                internal_ip = rule["internal_ip"]
                internal_port = rule["internal_port"]
                return {
                    "original": {"src": f"{src_ip}:{src_port}", "dest": f"{dest_ip}:{dest_port}"},
                    "translated": {"src": f"{src_ip}:{src_port}", "dest": f"{internal_ip}:{internal_port}"}
                }
        
        # Si no hay regla, no traducir
        return {
            "original": {"src": f"{src_ip}:{src_port}", "dest": f"{dest_ip}:{dest_port}"},
            "translated": {"src": f"{src_ip}:{src_port}", "dest": f"{dest_ip}:{dest_port}"}
        }

# Ejemplo de uso
nat = NATSimulator(public_ip="203.0.113.10")

# Añadir port forwarding
nat.add_port_forwarding(80, "192.168.1.10", 80)   # HTTP
nat.add_port_forwarding(443, "192.168.1.10", 443) # HTTPS

# Simular tráfico saliente desde LAN a Internet
egress = nat.translate_egress("192.168.1.20", 12345, "8.8.8.8", 53)
print(f"📤 Egress (SNAT): {egress['original']['src']} -> {egress['translated']['src']}")

# Simular tráfico entrante a puerto 80 (port forwarding)
ingress = nat.translate_ingress("203.0.113.20", 54321, "203.0.113.10", 80)
print(f"📥 Ingress (DNAT): {ingress['original']['dest']} -> {ingress['translated']['dest']}")
