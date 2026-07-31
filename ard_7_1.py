from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class IncidentResponseStep:
    """Paso en el plan de respuesta a incidentes de red"""
    order: int
    action: str
    responsible_role: str
    estimated_time: str  # en minutos
    description: str

@dataclass
class IncidentResponsePlan:
    """Plan de respuesta a incidentes para redes con pfSense"""
    plan_name: str
    version: str
    last_review: str
    incident_type: str  # "ddos", "intrusion", "malware", "misconfiguration", "ai_threat"
    severity: str  # "CRITICAL", "HIGH", "MEDIUM", "LOW"
    steps: List[IncidentResponseStep]
    
    def get_timeline(self) -> Dict:
        """Calcula el tiempo total estimado de respuesta"""
        total_minutes = sum(int(step.estimated_time) for step in self.steps)
        return {
            "total_minutes": total_minutes,
            "total_hours": total_minutes / 60,
            "steps": len(self.steps)
        }

# Plan de respuesta para ataque DDoS
ddos_plan = IncidentResponsePlan(
    plan_name="Respuesta a Ataque DDoS en pfSense",
    version="2.0",
    last_review="2026-07-01",
    incident_type="ddos",
    severity="CRITICAL",
    steps=[
        IncidentResponseStep(1, "Activar equipo de respuesta", "CSIRT Lead", "2", "Notificar a todos los miembros del CSIRT"),
        IncidentResponseStep(2, "Identificar IPs de ataque en logs de pfSense", "Network Security", "5", "Analizar logs de firewall para detectar IPs sospechosas"),
        IncidentResponseStep(3, "Bloquear IPs ofensivas en pfSense", "Network Security", "3", "Crear reglas de firewall para bloquear IPs"),
        IncidentResponseStep(4, "Habilitar limitación de conexiones", "Network Security", "5", "Configurar límites de conexiones en pfSense"),
        IncidentResponseStep(5, "Activar protección DDoS en pfSense", "Network Security", "10", "Habilitar módulo de protección DDoS"),
        IncidentResponseStep(6, "Notificar a proveedor de Internet", "Communications Lead", "15", "Contactar a ISP para mitigación adicional"),
        IncidentResponseStep(7, "Analizar logs y determinar alcance", "Forensic Analyst", "30", "Revisar logs de Suricata y pfSense"),
        IncidentResponseStep(8, "Documentar incidente", "CSIRT Lead", "45", "Crear informe detallado del incidente")
    ]
)

print("📋 PLAN DE RESPUESTA A INCIDENTES EN RED")
print(f"Plan: {ddos_plan.plan_name}")
print(f"Versión: {ddos_plan.version}")
print(f"Tipo: {ddos_plan.incident_type}")
print(f"Severidad: {ddos_plan.severity}")

timeline = ddos_plan.get_timeline()
print(f"\n⏱️ TIEMPO ESTIMADO")
print(f"Pasos: {timeline['steps']}")
print(f"Total: {timeline['total_minutes']} min ({timeline['total_hours']:.1f} horas)")

print(f"\n📌 PASOS:")
for step in ddos_plan.steps:
    print(f"  {step.order}. {step.action} ({step.estimated_time} min) - {step.responsible_role}")
