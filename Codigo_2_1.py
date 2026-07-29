import random
import time
from datetime import datetime
import numpy as np

class AdaptiveAuthEngine:
    def __init__(self, user_profile):
        """
        user_profile: dict con patrones de comportamiento históricos
        """
        self.profile = user_profile
        # Simular un modelo de ML (en producción usar XGBoost o TensorFlow)
        self.weights = {
            'hour': 0.3,
            'ip_trust': 0.4,
            'typing_deviation': 0.2,
            'resource_sensitivity': 0.3
        }

    def _calculate_hour_risk(self):
        current_hour = datetime.now().hour
        if 8 <= current_hour <= 18:
            return 0
        elif 19 <= current_hour <= 23:
            return 30
        else:  # 0-7
            return 50

    def _calculate_ip_risk(self, ip):
        if ip in self.profile.get('trusted_ips', []):
            return 0
        # Simular geolocalización (en realidad usar API de MaxMind)
        return 60

    def _calculate_typing_risk(self, current_speed):
        avg = self.profile.get('avg_typing_speed', 50)
        deviation = abs(current_speed - avg)
        if deviation < 10:
            return 0
        elif deviation < 30:
            return 25
        else:
            return 50

    def _calculate_resource_risk(self, resource):
        sensitive = ['/admin', '/database', '/financial', '/hr', '/ai_model']
        for sens in sensitive:
            if sens in resource:
                return 40
        return 0

    def calculate_risk_score(self, request):
        risk = 0
        risk += self._calculate_hour_risk()
        risk += self._calculate_ip_risk(request.get('ip', ''))
        risk += self._calculate_typing_risk(request.get('typing_speed', 50))
        risk += self._calculate_resource_risk(request.get('resource', ''))
        return min(risk, 100)

    def authenticate(self, request):
        risk = self.calculate_risk_score(request)
        if risk > 70:
            return "REQUIRE_BIOMETRIC", risk
        elif risk > 40:
            return "REQUIRE_OTP", risk
        else:
            return "APPROVED", risk

# Simulación de perfil y solicitud
user_profile = {
    'trusted_ips': ['192.168.1.10', '10.0.0.5'],
    'avg_typing_speed': 65
}

# Solicitud sospechosa (3 AM, IP externa, velocidad atípica, acceso a admin)
request = {
    'ip': '203.0.113.5',
    'typing_speed': 100,
    'resource': '/admin/settings'
}

engine = AdaptiveAuthEngine(user_profile)
decision, score = engine.authenticate(request)
print(f"Puntuación de riesgo: {score} -> Decisión: {decision}")
# Salida esperada: Puntuación de riesgo: 80 -> Decisión: REQUIRE_BIOMETRIC
