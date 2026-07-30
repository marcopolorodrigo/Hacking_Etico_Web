from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json

@dataclass
class AIIncident:
    """Representa un incidente en un sistema de IA"""
    id: str
    title: str
    description: str
    incident_type: str  # "prompt_injection", "data_poisoning", "model_stealing", etc.
    severity: str  # "CRITICAL", "HIGH", "MEDIUM", "LOW"
    detection_time: datetime
    affected_systems: List[str]
    affected_users: Optional[int] = None
    status: str = "DETECTED"
    impact: str = ""
    remediation: str = ""
    reported_to_regulator: bool = False

class AIIncidentNotification:
    """
    Sistema de notificación de incidentes para sistemas de IA.
    """
    
    def __init__(self, organization: str, regulatory_authority: str):
        self.organization = organization
        self.regulatory_authority = regulatory_authority
        self.incidents: List[AIIncident] = []
    
    def register_incident(self, incident: AIIncident):
        self.incidents.append(incident)
        self._check_notification_requirements(incident)
    
    def _check_notification_requirements(self, incident: AIIncident):
        """Verifica si se requiere notificación regulatoria"""
        # GDPR: 72 horas para datos personales
        if incident.affected_users and incident.affected_users > 0:
            deadline_gdpr = incident.detection_time + timedelta(hours=72)
            print(f"⚠️ GDPR: Notificar en 72h (plazo: {deadline_gdpr})")
        
        # AI Act: 15 días para sistemas de alto riesgo
        if incident.severity in ["CRITICAL", "HIGH"]:
            deadline_aiact = incident.detection_time + timedelta(days=15)
            print(f"⚠️ AI Act: Notificar en 15 días (plazo: {deadline_aiact})")
            
            # Notificar automáticamente si es crítico
            if incident.severity == "CRITICAL":
                self._notify_regulator(incident)
    
    def _notify_regulator(self, incident: AIIncident):
        """Simula la notificación a la autoridad reguladora"""
        print(f"📢 NOTIFICANDO A AUTORIDAD REGULADORA")
        print(f"  Organización: {self.organization}")
        print(f"  Autoridad: {self.regulatory_authority}")
        print(f"  Incidente: {incident.title}")
        print(f"  Severidad: {incident.severity}")
        print(f"  Fecha: {incident.detection_time}")
        incident.reported_to_regulator = True
    
    def generate_report(self, incident_id: str) -> Dict:
        """Genera un informe de incidente para auditoría"""
        incident = next((i for i in self.incidents if i.id == incident_id), None)
        if not incident:
            return {"error": "Incidente no encontrado"}
        
        return {
            "incident_id": incident.id,
            "organization": self.organization,
            "title": incident.title,
            "type": incident.incident_type,
            "severity": incident.severity,
            "detection_time": incident.detection_time.isoformat(),
            "affected_systems": incident.affected_systems,
            "affected_users": incident.affected_users,
            "status": incident.status,
            "impact": incident.impact,
            "remediation": incident.remediation,
            "reported_to_regulator": incident.reported_to_regulator,
            "regulatory_authority": self.regulatory_authority
        }

# Ejemplo de uso
notification = AIIncidentNotification("Banco Nacional S.A.", "CNIL")

# Registrar un incidente crítico
incident = AIIncident(
    id="AI-2026-001",
    title="Inyección de Prompts en Chatbot Bancario",
    description="Se detectaron múltiples intentos de inyección de prompts en el chatbot de atención al cliente.",
    incident_type="prompt_injection",
    severity="CRITICAL",
    detection_time=datetime.now(),
    affected_systems=["Chatbot API", "Modelo LLM", "Base de datos de clientes"],
    affected_users=500,
    impact="Exposición de datos de clientes, violación de GDPR y AI Act",
    remediation="Implementación de filtros de entrada y sanitización de salidas"
)

notification.register_incident(incident)

# Generar informe
report = notification.generate_report("AI-2026-001")
print("\n📄 INFORME DE INCIDENTE")
print(json.dumps(report, indent=2, default=str))
