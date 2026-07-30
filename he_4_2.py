from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class IncidentSeverity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class IncidentType(Enum):
    PROMPT_INJECTION = "prompt_injection"
    DATA_POISONING = "data_poisoning"
    MODEL_STEALING = "model_stealing"
    OUTPUT_LEAKAGE = "output_leakage"
    BIAS_DISCRIMINATION = "bias_discrimination"
    SUPPLY_CHAIN = "supply_chain"

@dataclass
class IncidentResponseStep:
    """Paso en el plan de respuesta a incidentes"""
    order: int
    action: str
    responsible_role: str
    estimated_time: str  # en minutos
    description: str

@dataclass
class IncidentResponsePlan:
    """Plan de respuesta a incidentes de IA"""
    plan_name: str
    version: str
    last_review: str
    incident_type: IncidentType
    severity: IncidentSeverity
    steps: List[IncidentResponseStep]
    
    def get_timeline(self) -> Dict:
        """Calcula el tiempo total estimado de respuesta"""
        total_minutes = sum(int(step.estimated_time) for step in self.steps)
        return {
            "total_minutes": total_minutes,
            "total_hours": total_minutes / 60,
            "steps": len(self.steps)
        }

# Ejemplo: Plan de respuesta para inyección de prompts (CRITICAL)
plan = IncidentResponsePlan(
    plan_name="Respuesta a Inyección de Prompts - Nivel Crítico",
    version="2.0",
    last_review="2026-07-01",
    incident_type=IncidentType.PROMPT_INJECTION,
    severity=IncidentSeverity.CRITICAL,
    steps=[
        IncidentResponseStep(1, "Activar equipo de respuesta", "CSIRT Lead", "2", "Notificar a todos los miembros del CSIRT"),
        IncidentResponseStep(2, "Aislar el modelo comprometido", "AI Security Specialist", "5", "Desconectar el modelo afectado de producción"),
        IncidentResponseStep(3, "Bloquear tráfico sospechoso", "Network Security", "3", "Bloquear IPs y patrones de ataque"),
        IncidentResponseStep(4, "Activar filtros de entrada adicionales", "AI Security Specialist", "10", "Implementar reglas de detección de inyección"),
        IncidentResponseStep(5, "Analizar logs y determinar alcance", "Forensic Analyst", "30", "Revisar interacciones recientes"),
        IncidentResponseStep(6, "Notificar a partes interesadas", "Communications Lead", "15", "Informar a dirección y reguladores"),
        IncidentResponseStep(7, "Implementar medidas correctivas", "AI Security Specialist", "60", "Aplicar parches y actualizaciones"),
        IncidentResponseStep(8, "Restaurar servicio", "DevOps Engineer", "30", "Desplegar modelo parcheado"),
        IncidentResponseStep(9, "Documentar y revisar", "CSIRT Lead", "45", "Crear informe y lecciones aprendidas")
    ]
)

print(f"📋 PLAN DE RESPUESTA A INCIDENTES DE IA")
print(f"Plan: {plan.plan_name}")
print(f"Versión: {plan.version}")
print(f"Tipo: {plan.incident_type.value}")
print(f"Severidad: {plan.severity.value}")

timeline = plan.get_timeline()
print(f"\n⏱️ TIEMPO ESTIMADO")
print(f"Pasos: {timeline['steps']}")
print(f"Total: {timeline['total_minutes']} min ({timeline['total_hours']:.1f} horas)")

print(f"\n📌 PASOS:")
for step in plan.steps:
    print(f"  {step.order}. {step.action} ({step.estimated_time} min) - {step.responsible_role}")
