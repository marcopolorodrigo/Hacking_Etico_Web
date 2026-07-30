from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class ResponseAction:
    """Acción de respuesta a un incidente de IA"""
    action_id: str
    description: str
    status: str  # "PENDING", "IN_PROGRESS", "COMPLETED", "FAILED"
    timestamp: datetime
    result: Optional[str] = None

class AutomatedResponseSystem:
    """
    Sistema de respuesta automatizada para incidentes de IA.
    """
    
    def __init__(self):
        self.actions: List[ResponseAction] = []
        self.isolated_models = []
        self.blocked_ips = []
    
    def respond_to_prompt_injection(self, incident_id: str, 
                                    model_id: str, 
                                    suspicious_ips: List[str]) -> List[ResponseAction]:
        """
        Responde automáticamente a un incidente de inyección de prompts.
        """
        actions = []
        
        # Acción 1: Aislar modelo
        action1 = ResponseAction(
            action_id=f"{incident_id}_001",
            description=f"Aislando modelo {model_id}",
            status="IN_PROGRESS",
            timestamp=datetime.now()
        )
        self.isolated_models.append(model_id)
        action1.status = "COMPLETED"
        action1.result = "Modelo aislado correctamente"
        actions.append(action1)
        
        # Acción 2: Bloquear IPs
        for ip in suspicious_ips:
            action = ResponseAction(
                action_id=f"{incident_id}_002_{ip}",
                description=f"Bloqueando IP {ip}",
                status="PENDING",
                timestamp=datetime.now()
            )
            if ip not in self.blocked_ips:
                self.blocked_ips.append(ip)
                action.status = "COMPLETED"
                action.result = f"IP {ip} bloqueada"
            else:
                action.status = "COMPLETED"
                action.result = f"IP {ip} ya estaba bloqueada"
            actions.append(action)
        
        # Acción 3: Activar filtros adicionales
        action3 = ResponseAction(
            action_id=f"{incident_id}_003",
            description="Activando filtros de entrada adicionales",
            status="IN_PROGRESS",
            timestamp=datetime.now()
        )
        # Simulación de activación
        action3.status = "COMPLETED"
        action3.result = "Filtros adicionales activados (reglas 1001-1005)"
        actions.append(action3)
        
        self.actions.extend(actions)
        return actions
    
    def get_response_summary(self) -> Dict:
        """Obtiene un resumen de las respuestas ejecutadas"""
        return {
            "total_actions": len(self.actions),
            "completed": len([a for a in self.actions if a.status == "COMPLETED"]),
            "in_progress": len([a for a in self.actions if a.status == "IN_PROGRESS"]),
            "failed": len([a for a in self.actions if a.status == "FAILED"]),
            "isolated_models": self.isolated_models,
            "blocked_ips": self.blocked_ips
        }

# Ejemplo de uso
responder = AutomatedResponseSystem()

# Responder a un incidente
response = responder.respond_to_prompt_injection(
    incident_id="AI-2026-001",
    model_id="chatbot_v2",
    suspicious_ips=["203.0.113.5", "198.51.100.10"]
)

print("🚨 RESPUESTA AUTOMATIZADA")
print(f"Acciones ejecutadas: {len(response)}")
for action in response:
    print(f"  [{action.status}] {action.description}")
    if action.result:
        print(f"    Resultado: {action.result}")

summary = responder.get_response_summary()
print(f"\n📊 RESUMEN DE RESPUESTA")
print(f"  Modelos aislados: {summary['isolated_models']}")
print(f"  IPs bloqueadas: {summary['blocked_ips']}")
