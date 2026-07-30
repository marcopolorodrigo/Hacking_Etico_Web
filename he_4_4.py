from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class IncidentNotification:
    """Plantilla de notificación de incidentes de IA"""
    incident_id: str
    title: str
    description: str
    incident_type: str
    severity: str
    detection_time: str
    affected_systems: List[str]
    affected_users: Optional[int] = None
    impact: str = ""
    remediation: str = ""
    status: str = "EN_PROCESO"
    regulatory_notification: bool = False

class NotificationGenerator:
    """
    Generador de notificaciones de incidentes de IA para diferentes audiencias.
    """
    
    def generate_executive_notification(self, incident: IncidentNotification) -> str:
        """Genera una notificación para la alta dirección"""
        return f"""
        ⚠️ NOTIFICACIÓN DE INCIDENTE DE IA - EJECUTIVOS
        =============================================
        ID: {incident.incident_id}
        Título: {incident.title}
        Severidad: {incident.severity}
        Fecha: {incident.detection_time}
        
        Impacto en el Negocio:
        {incident.impact}
        
        Medidas Tomadas:
        {incident.remediation}
        
        Próximos Pasos:
        - Investigación en curso
        - Implementación de medidas correctivas
        - Informe final en 48h
        """
    
    def generate_technical_notification(self, incident: IncidentNotification) -> str:
        """Genera una notificación para equipos técnicos"""
        return f"""
        🔧 NOTIFICACIÓN TÉCNICA - INCIDENTE DE IA
        =========================================
        ID: {incident.incident_id}
        Tipo: {incident.incident_type}
        Severidad: {incident.severity}
        
        Sistemas Afectados:
        {', '.join(incident.affected_systems)}
        
        Impacto Técnico:
        {incident.impact}
        
        Acciones Requeridas:
        1. Aislar sistemas afectados
        2. Analizar logs del modelo
        3. Implementar parches de seguridad
        4. Verificar integridad del modelo
        5. Actualizar documentación
        
        Responsables: Equipo CSIRT
        """
    
    def generate_regulatory_notification(self, incident: IncidentNotification) -> str:
        """Genera una notificación para autoridades reguladoras"""
        return f"""
        📜 NOTIFICACIÓN REGULATORIA - INCIDENTE DE IA
        =============================================
        Incidente: {incident.incident_id}
        Organización: [Nombre de la organización]
        Fecha de notificación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        Naturaleza del Incidente:
        {incident.description}
        
        Datos Afectados:
        Usuarios afectados: {incident.affected_users or 'No determinado'}
        Sistemas afectados: {', '.join(incident.affected_systems)}
        
        Medidas de Mitigación:
        {incident.remediation}
        
        Cumplimiento Normativo:
        - GDPR Art. 33: Notificación en 72h
        - AI Act Art. 62: Notificación de incidentes graves
        - NIS2: Notificación en 24h para sectores críticos
        
        Contacto: [Nombre del CISO] | [Correo electrónico] | [Teléfono]
        """

# Ejemplo de uso
notification = IncidentNotification(
    incident_id="AI-2026-001",
    title="Inyección de Prompts en Chatbot Bancario",
    description="Se detectaron múltiples intentos de inyección de prompts en el chatbot de atención al cliente, con un intento exitoso que expuso información de un cliente.",
    incident_type="prompt_injection",
    severity="CRITICAL",
    detection_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    affected_systems=["Chatbot API", "Modelo LLM", "Base de datos de clientes"],
    affected_users=1,
    impact="Exposición de datos de un cliente, posible violación de GDPR",
    remediation="Aislamiento del modelo afectado, implementación de filtros de entrada",
    status="CONTENIDO"
)

generator = NotificationGenerator()

print(generator.generate_executive_notification(notification))
print("\n" + "="*60 + "\n")
print(generator.generate_technical_notification(notification))
print("\n" + "="*60 + "\n")
print(generator.generate_regulatory_notification(notification))
