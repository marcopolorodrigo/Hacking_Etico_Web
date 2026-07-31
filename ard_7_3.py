from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class IncidentNotification:
    """Plantilla de notificación de incidentes de red"""
    incident_id: str
    title: str
    description: str
    incident_type: str
    severity: str
    detection_time: str
    affected_systems: List[str]
    impacted_services: List[str]
    containment: str = ""
    remediation: str = ""
    regulatory_notification: bool = False

class NotificationGenerator:
    """
    Generador de notificaciones de incidentes de red.
    """
    
    def generate_executive_notification(self, incident: IncidentNotification) -> str:
        """Genera una notificación para la alta dirección"""
        return f"""
        ⚠️ NOTIFICACIÓN DE INCIDENTE DE RED - EJECUTIVOS
        =============================================
        ID: {incident.incident_id}
        Título: {incident.title}
        Severidad: {incident.severity}
        Fecha: {incident.detection_time}
        
        Impacto en el Negocio:
        {incident.description}
        
        Sistemas Afectados:
        {', '.join(incident.affected_systems)}
        
        Servicios Afectados:
        {', '.join(incident.impacted_services)}
        
        Medidas Tomadas:
        {incident.containment}
        
        Próximos Pasos:
        - Investigación en curso
        - Implementación de medidas correctivas
        - Informe final en 48h
        """
    
    def generate_technical_notification(self, incident: IncidentNotification) -> str:
        """Genera una notificación para equipos técnicos"""
        return f"""
        🔧 NOTIFICACIÓN TÉCNICA - INCIDENTE DE RED
        =========================================
        ID: {incident.incident_id}
        Tipo: {incident.incident_type}
        Severidad: {incident.severity}
        
        Sistemas Afectados:
        {', '.join(incident.affected_systems)}
        
        Servicios Afectados:
        {', '.join(incident.impacted_services)}
        
        Acciones Requeridas:
        1. Verificar logs de pfSense y Suricata
        2. Aislar sistemas afectados
        3. Implementar reglas de bloqueo en pfSense
        4. Verificar integridad de las configuraciones
        5. Actualizar documentación
        
        Responsables: Equipo CSIRT
        """

# Ejemplo de uso
notification = IncidentNotification(
    incident_id="IR-2026-001",
    title="Ataque DDoS a pfSense",
    description="Se detectó un ataque DDoS dirigido al firewall pfSense, afectando la disponibilidad de los servicios web.",
    incident_type="ddos",
    severity="CRITICAL",
    detection_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    affected_systems=["pfSense Firewall", "Servidor Web"],
    impacted_services=["HTTP", "HTTPS", "VPN"],
    containment="Se bloquearon las IPs ofensivas y se habilitó la protección DDoS en pfSense",
    remediation="Pendiente de análisis"
)

generator = NotificationGenerator()

print(generator.generate_executive_notification(notification))
print("\n" + "="*60 + "\n")
print(generator.generate_technical_notification(notification))
