from typing import List, Dict
from datetime import datetime

class AutomatedResponse:
    """Sistema de respuesta automatizada para incidentes de IA"""
    
    def __init__(self):
        self.blocked_ips = []
        self.isolated_models = []
        self.response_log = []
    
    def block_ip(self, ip: str) -> Dict:
        if ip not in self.blocked_ips:
            self.blocked_ips.append(ip)
            self.response_log.append({"action": "BLOCK_IP", "ip": ip, "status": "SUCCESS"})
            return {"status": "SUCCESS", "message": f"IP {ip} bloqueada"}
        return {"status": "EXISTS", "message": f"IP {ip} ya está bloqueada"}
    
    def isolate_model(self, model_id: str) -> Dict:
        self.isolated_models.append(model_id)
        self.response_log.append({"action": "ISOLATE_MODEL", "model": model_id, "status": "SUCCESS"})
        return {"status": "SUCCESS", "message": f"Modelo {model_id} aislado"}
    
    def respond_to_prompt_injection(self, incident_id: str, model_id: str, suspicious_ips: List[str]) -> List[Dict]:
        responses = []
        # Aislar modelo
        responses.append(self.isolate_model(model_id))
        # Bloquear IPs
        for ip in suspicious_ips:
            responses.append(self.block_ip(ip))
        return responses

# Ejemplo de uso
responder = AutomatedResponse()
responses = responder.respond_to_prompt_injection("AI-2026-001", "chatbot_v2", ["203.0.113.5", "198.51.100.10"])
for r in responses:
    print(f"{r['status']}: {r['message']}")
