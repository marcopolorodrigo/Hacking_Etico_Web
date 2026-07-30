from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class TestObjective(Enum):
    PROMPT_INJECTION = "Evaluar resistencia a inyección de prompts"
    DATA_POISONING = "Detectar vulnerabilidades a envenenamiento de datos"
    MODEL_STEALING = "Verificar protección contra extracción de modelo"
    OUTPUT_SANITIZATION = "Probar sanitización de salidas del LLM"
    RAG_SECURITY = "Evaluar seguridad del sistema RAG"
    VECTOR_DB_SECURITY = "Probar seguridad de la base de datos vectorial"
    COMPLIANCE = "Verificar cumplimiento con AI Act y GDPR"
    SUPPLY_CHAIN = "Auditar la cadena de suministro de IA"

@dataclass
class PentestPlan:
    """Plan de pruebas de penetración para sistemas con IA"""
    system_name: str
    system_version: str
    objectives: List[TestObjective]
    scope: Dict
    team_members: List[str]
    timeline: str
    rules_of_engagement: str

    def generate_plan_report(self) -> Dict:
        return {
            "system": self.system_name,
            "version": self.system_version,
            "objectives": [obj.value for obj in self.objectives],
            "scope": self.scope,
            "team": self.team_members,
            "timeline": self.timeline,
            "rules": self.rules_of_engagement
        }

# Ejemplo de plan para un chatbot bancario
plan = PentestPlan(
    system_name="Chatbot Atención al Cliente Bancario",
    system_version="3.2.0",
    objectives=[
        TestObjective.PROMPT_INJECTION,
        TestObjective.OUTPUT_SANITIZATION,
        TestObjective.RAG_SECURITY,
        TestObjective.COMPLIANCE
    ],
    scope={
        "in_scope": ["API de chat", "Base de datos vectorial", "Sistema RAG"],
        "out_of_scope": ["Infraestructura de entrenamiento", "Datos históricos"],
        "allowed_techniques": ["Prompt injection", "Model interrogation"]
    },
    team_members=["Lead Pentester", "AI Security Specialist", "Compliance Expert"],
    timeline="2 semanas (10 días hábiles)",
    rules_of_engagement="Pruebas solo en entorno de staging. No afectar datos reales."
)

print("Plan de pentesting generado:")
print(plan.generate_plan_report())
