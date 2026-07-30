from datetime import datetime
from typing import Dict, Optional
import random

class AdaptiveAuth:
    """
    Autenticación adaptativa basada en riesgo para APIs de IA.
    """
    
    def __init__(self):
        self.user_profiles = {}
        self.failed_attempts = {}
    
    def register_user(self, user_id: str, trusted_ips: list, 
                      avg_typing_speed: int = 50):
        self.user_profiles[user_id] = {
            "trusted_ips": trusted_ips,
            "avg_typing_speed": avg_typing_speed
        }
        self.failed_attempts[user_id] = 0
    
    def calculate_risk(self, user_id: str, ip: str, 
                       typing_speed: Optional[int] = None,
                       resource: str = "default") -> int:
        """
        Calcula una puntuación de riesgo (0-100).
        """
        score = 0
        profile = self.user_profiles.get(user_id)
        if not profile:
            return 100  # Usuario desconocido
        
        # Factor 1: IP no confiable
        if ip not in profile["trusted_ips"]:
            score += 40
        
        # Factor 2: Hora de acceso (fuera de horario)
        hour = datetime.now().hour
        if hour < 8 or hour > 18:
            score += 20
        
        # Factor 3: Patrón de tecleo anómalo
        if typing_speed and abs(typing_speed - profile["avg_typing_speed"]) > 30:
            score += 20
        
        # Factor 4: Recurso sensible
        sensitive_resources = ["/admin", "/model/weights", "/database"]
        if resource in sensitive_resources:
            score += 20
        
        # Factor 5: Intentos fallidos previos
        score += min(self.failed_attempts.get(user_id, 0) * 10, 30)
        
        return min(score, 100)
    
    def authenticate(self, user_id: str, ip: str, 
                     typing_speed: Optional[int] = None,
                     resource: str = "default") -> Dict:
        """
        Evalúa la autenticación basada en riesgo.
        """
        risk = self.calculate_risk(user_id, ip, typing_speed, resource)
        
        if risk > 70:
            return {
                "status": "REQUIRE_MFA",
                "risk_score": risk,
                "message": "Riesgo alto - Se requiere autenticación multifactor"
            }
        elif risk > 40:
            return {
                "status": "REQUIRE_OTP",
                "risk_score": risk,
                "message": "Riesgo medio - Se requiere OTP adicional"
            }
        else:
            return {
                "status": "APPROVED",
                "risk_score": risk,
                "message": "Autenticación aprobada"
            }
    
    def record_failure(self, user_id: str):
        self.failed_attempts[user_id] = self.failed_attempts.get(user_id, 0) + 1
    
    def reset_failures(self, user_id: str):
        self.failed_attempts[user_id] = 0

# Ejemplo de uso
auth = AdaptiveAuth()
auth.register_user("alice", ["192.168.1.100", "10.0.0.5"], avg_typing_speed=60)

# Solicitud desde IP confiable, horario normal, velocidad normal
result = auth.authenticate("alice", "192.168.1.100", typing_speed=58, resource="/chat")
print(f"Alice (normal): {result['status']} - Riesgo: {result['risk_score']}")

# Solicitud desde IP desconocida, madrugada, velocidad anómala
result = auth.authenticate("alice", "203.0.113.5", typing_speed=100, resource="/admin")
print(f"Alice (sospechosa): {result['status']} - Riesgo: {result['risk_score']}")
