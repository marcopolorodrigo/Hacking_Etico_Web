from typing import List, Dict
from datetime import datetime

class AutomatedResponse:
    """
    Automatización de respuesta a incidentes en pfSense (simulación).
    """
    
    def __init__(self):
        self.blocked_ips = []
        self.response_log = []
    
    def block_ip(self, ip: str) -> Dict:
        """
        Simula el bloqueo de una IP en pfSense.
        """
        if ip not in self.blocked_ips:
            self.blocked_ips.append(ip)
            self.response_log.append({
                "action": "BLOCK_IP",
                "ip": ip,
                "timestamp": datetime.now().isoformat(),
                "status": "SUCCESS"
            })
            return {"status": "SUCCESS", "message": f"IP {ip} bloqueada"}
        else:
            return {"status": "EXISTS", "message": f"IP {ip} ya está bloqueada"}
    
    def isolate_vlan(self, vlan_id: str) -> Dict:
        """
        Simula el aislamiento de una VLAN en pfSense.
        """
        self.response_log.append({
            "action": "ISOLATE_VLAN",
            "vlan": vlan_id,
            "timestamp": datetime.now().isoformat(),
            "status": "SUCCESS"
        })
        return {"status": "SUCCESS", "message": f"VLAN {vlan_id} aislada"}
    
    def enable_ddos_protection(self) -> Dict:
        """
        Simula la activación de protección DDoS en pfSense.
        """
        self.response_log.append({
            "action": "ENABLE_DDOS_PROTECTION",
            "timestamp": datetime.now().isoformat(),
            "status": "SUCCESS"
        })
        return {"status": "SUCCESS", "message": "Protección DDoS activada"}
    
    def update_firewall_rules(self, rules: List[str]) -> Dict:
        """
        Simula la actualización de reglas de firewall en pfSense.
        """
        self.response_log.append({
            "action": "UPDATE_RULES",
            "rules": rules,
            "timestamp": datetime.now().isoformat(),
            "status": "SUCCESS"
        })
        return {"status": "SUCCESS", "message": f"Reglas actualizadas: {len(rules)}"}
    
    def respond_to_incident(self, incident_type: str, details: Dict) -> List[Dict]:
        """
        Responde automáticamente a un incidente según su tipo.
        """
        responses = []
        
        if incident_type == "ddos":
            # Bloquear IPs ofensivas
            for ip in details.get("ips", []):
                responses.append(self.block_ip(ip))
            # Activar protección DDoS
            responses.append(self.enable_ddos_protection())
        
        elif incident_type == "intrusion":
            # Bloquear IPs ofensivas
            for ip in details.get("ips", []):
                responses.append(self.block_ip(ip))
            # Aislar VLAN (si se especifica)
            if "vlan" in details:
                responses.append(self.isolate_vlan(details["vlan"]))
        
        elif incident_type == "misconfiguration":
            # Restaurar configuración previa
            responses.append(self.update_firewall_rules(details.get("previous_rules", [])))
        
        return responses
    
    def get_response_log(self) -> List[Dict]:
        return self.response_log

# Ejemplo de uso
responder = AutomatedResponse()

# Simular respuesta a un ataque DDoS
response = responder.respond_to_incident("ddos", {
    "ips": ["203.0.113.5", "198.51.100.10"]
})

print("🚨 RESPUESTA AUTOMATIZADA A INCIDENTE DDoS")
for r in response:
    print(f"  {r['status']}: {r['message']}")

# Ver logs de respuesta
print(f"\n📊 LOG DE RESPUESTA: {len(responder.get_response_log())} acciones")
