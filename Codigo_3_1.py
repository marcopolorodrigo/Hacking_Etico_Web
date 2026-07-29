# Simulación de verificación de cumplimiento de Artículo 50
from datetime import datetime
import json

class AIActTransparencyChecker:
    def __init__(self):
        self.deadlines = {
            "transparency_art50": datetime(2026, 8, 2),
            "high_risk_annex3": datetime(2027, 12, 2),
            "annex1_products": datetime(2028, 8, 2),
            "csam_prohibition": datetime(2026, 12, 2)
        }
        self.requirements = {
            "interactive_ai": "Informar que se interactúa con IA en primera interacción",
            "generated_content": "Marcar contenido generado por IA (machine-readable)",
            "emotion_recognition": "Informar sobre uso de reconocimiento de emociones",
            "biometric_categorization": "Informar sobre categorización biométrica"
        }
    
    def check_system_compliance(self, system_type: str, market_date: datetime, 
                               is_interactive: bool = False, generates_content: bool = False):
        """Verifica si un sistema cumple con los plazos del AI Act"""
        today = datetime.now()
        results = {
            "system_type": system_type,
            "market_date": market_date.strftime("%Y-%m-%d"),
            "deadlines": {},
            "actions_required": []
        }
        
        # Verificar obligaciones de transparencia (Art. 50) - aplican desde 2/8/2026
        if today >= self.deadlines["transparency_art50"]:
            if is_interactive:
                results["actions_required"].append({
                    "requirement": "transparency_interactive",
                    "description": self.requirements["interactive_ai"],
                    "status": "REQUIRED"
                })
            if generates_content:
                # Si el sistema se colocó antes del 2/8/2026, tiene gracia hasta 2/12/2026
                grace_deadline = self.deadlines["csam_prohibition"]  # 2/12/2026
                if market_date < self.deadlines["transparency_art50"]:
                    deadline = grace_deadline
                    status = "GRACE_PERIOD"
                else:
                    deadline = self.deadlines["transparency_art50"]
                    status = "REQUIRED"
                results["actions_required"].append({
                    "requirement": "content_marking",
                    "description": self.requirements["generated_content"],
                    "deadline": deadline.strftime("%Y-%m-%d"),
                    "status": status
                })
        
        # Verificar si es sistema de alto riesgo (Anexo III)
        # (Plazo extendido a 2/12/2027)
        high_risk_systems = ["employment", "education", "credit_scoring", 
                            "critical_infrastructure", "law_enforcement"]
        if system_type in high_risk_systems:
            results["deadlines"]["high_risk"] = self.deadlines["high_risk_annex3"].strftime("%Y-%m-%d")
            results["actions_required"].append({
                "requirement": "high_risk_conformity",
                "description": "Evaluación de conformidad y gestión de riesgos para sistemas de alto riesgo",
                "deadline": self.deadlines["high_risk_annex3"].strftime("%Y-%m-%d"),
                "status": "PENDING"
            })
        
        return results

# Ejemplo: Verificar un chatbot lanzado en enero 2026
checker = AIActTransparencyChecker()
chatbot = checker.check_system_compliance(
    system_type="chatbot",
    market_date=datetime(2026, 1, 15),
    is_interactive=True,
    generates_content=True
)
print(json.dumps(chatbot, indent=2, default=str))
