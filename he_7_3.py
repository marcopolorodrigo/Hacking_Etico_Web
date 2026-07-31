from typing import List, Dict

class AutomatedResponse:
    """Sistema de respuesta automatizada para incidentes de IA"""
    
    def __init__(self):
        self.blocked_ips = []
        self.isolated_models = []
        self.response_log = []
    
    def block_ip(self, ip: str) -> Dict:
        if ip not in self.blocked_ips:
            self.blocked_ips.append(ip)
            return {"status": "SUCCESS", "message": f"IP {ip} bloqueada"}
        return {"status": "EXISTS", "message": f"IP {ip} ya está bloqueada"}
    
    def isolate_model(self, model_id: str) -> Dict:
        self.isolated_models.append(model_id)
        return {"status": "SUCCESS", "message": f"Modelo {model_id} aislado"}
    
    def respond_to_prompt_injection(self, model_id: str, suspicious_ips: List[str]) -> List[Dict]:
        responses = []
        responses.append(self.isolate_model(model_id))
        for ip in suspicious_ips:
            responses.append(self.block_ip(ip))
        return responses

# Ejemplo de uso
responder = AutomatedResponse()
responses = responder.respond_to_prompt_injection("chatbot_v2", ["203.0.113.5"])
for r in responses:
    print(f"{r['status']}: {r['message']}")
