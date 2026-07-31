from dataclasses import dataclass
from datetime import datetime

@dataclass
class IncidentNotification:
    incident_id: str
    title: str
    description: str
    incident_type: str
    severity: str
    detection_time: str
    affected_systems: List[str]
    impact: str
    remediation: str

class NotificationGenerator:
    """Generador de notificaciones de incidentes de IA"""
    
    def generate_executive_notification(self, incident: IncidentNotification) -> str:
        return f"""
        ⚠️ NOTIFICACIÓN DE INCIDENTE DE IA - EJECUTIVOS
        =============================================
        ID: {incident.incident_id}
        Título: {incident.title}
        Severidad: {incident.severity}
        Impacto: {incident.impact}
        Medidas: {incident.remediation}
        """
    
    def generate_regulatory_notification(self, incident: IncidentNotification) -> str:
        return f"""
        📜 NOTIFICACIÓN REGULATORIA - INCIDENTE DE IA
        =============================================
        Incidente: {incident.incident_id}
        Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Naturaleza: {incident.description}
        Datos Afectados: {', '.join(incident.affected_systems)}
        Medidas: {incident.remediation}
        """

# Ejemplo de uso
notification = IncidentNotification(
    incident_id="AI-2026-001",
    title="Inyección de Prompts en Chatbot",
    description="Se detectaron múltiples intentos de inyección de prompts.",
    incident_type="prompt_injection",
    severity="CRITICAL",
    detection_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    affected_systems=["Chatbot API", "Modelo LLM"],
    impact="Exposición de datos de clientes",
    remediation="Aislamiento del modelo, implementación de filtros"
)

generator = NotificationGenerator()
print(generator.generate_executive_notification(notification))
