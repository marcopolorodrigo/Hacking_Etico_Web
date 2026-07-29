import json
from datetime import datetime
from typing import List, Dict

class AIRegister:
    def __init__(self):
        self.systems: List[Dict] = []
    
    def register_system(self, name: str, description: str, 
                        system_type: str, risk_level: str,
                        provider: str, deployer: str,
                        compliance_status: Dict) -> str:
        """Registra un sistema de IA en el registro"""
        system_id = f"AI-{datetime.now().strftime('%Y%m%d')}-{len(self.systems)+1:04d}"
        
        entry = {
            "id": system_id,
            "name": name,
            "description": description,
            "system_type": system_type,
            "risk_level": risk_level,
            "provider": provider,
            "deployer": deployer,
            "registration_date": datetime.now().isoformat(),
            "compliance_status": compliance_status,
            "documentation": {
                "technical_documentation": None,
                "conformity_assessment": None,
                "post_market_monitoring": None
            },
            "updates": []
        }
        
        self.systems.append(entry)
        return system_id
    
    def update_compliance(self, system_id: str, status_update: Dict):
        """Actualiza el estado de cumplimiento de un sistema"""
        for system in self.systems:
            if system["id"] == system_id:
                system["compliance_status"].update(status_update)
                system["updates"].append({
                    "date": datetime.now().isoformat(),
                    "update": status_update
                })
                return True
        return False
    
    def get_high_risk_systems(self) -> List[Dict]:
        """Obtiene todos los sistemas de alto riesgo"""
        return [s for s in self.systems if "ALTO" in s["risk_level"]]
    
    def export_register(self) -> str:
        """Exporta el registro como JSON para auditorías"""
        return json.dumps(self.systems, indent=2, default=str)

# Ejemplo: Registrar sistemas de IA
register = AIRegister()

# Registrar un chatbot
chatbot_id = register.register_system(
    name="Chatbot Atención al Cliente",
    description="Chatbot basado en LLM para atención al cliente en el sector bancario",
    system_type="CHATBOT",
    risk_level="RIESGO_DE_TRANSPARENCIA (Art. 50)",
    provider="TechSolutions S.A.",
    deployer="Banco Nacional",
    compliance_status={
        "transparency": "PENDIENTE",
        "data_protection": "CUMPLE",
        "ai_act_art50": "EN_PROGRESO"
    }
)

# Registrar un sistema de alto riesgo
screening_id = register.register_system(
    name="Sistema de Selección de Personal",
    description="Sistema de IA para preselección de candidatos en procesos de contratación",
    system_type="HR_AI",
    risk_level="ALTO_RIESGO (Anexo III)",
    provider="HR-Tech",
    deployer="Corporación Global",
    compliance_status={
        "conformity_assessment": "PENDIENTE",
        "risk_management": "EN_PROGRESO",
        "documentation": "PENDIENTE"
    }
)

# Actualizar estado de cumplimiento
register.update_compliance(chatbot_id, {"transparency": "CUMPLE", "ai_act_art50": "CUMPLE"})

# Exportar registro para auditoría
print(register.export_register())
