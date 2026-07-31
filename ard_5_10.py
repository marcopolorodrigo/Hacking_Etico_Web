from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime, timedelta

@dataclass
class RiskMitigationPlan:
    """Plan de mitigación para riesgos identificados"""
    risk_id: str
    risk_description: str
    mitigation_action: str
    responsible: str
    deadline: str
    status: str  # "PENDING", "IN_PROGRESS", "COMPLETED"
    notes: str = ""

class MitigationPlanGenerator:
    """
    Generador de planes de mitigación para riesgos en pfSense.
    """
    
    def __init__(self):
        self.plans: List[RiskMitigationPlan] = []
    
    def add_plan(self, plan: RiskMitigationPlan):
        self.plans.append(plan)
    
    def get_plans_by_status(self, status: str) -> List[RiskMitigationPlan]:
        return [p for p in self.plans if p.status == status]
    
    def generate_report(self) -> Dict:
        """Genera un informe del plan de mitigación"""
        return {
            "total_plans": len(self.plans),
            "by_status": {
                s: len([p for p in self.plans if p.status == s])
                for s in set(p.status for p in self.plans)
            },
            "plans": [
                {
                    "risk_id": p.risk_id,
                    "risk_description": p.risk_description,
                    "action": p.mitigation_action,
                    "responsible": p.responsible,
                    "deadline": p.deadline,
                    "status": p.status
                }
                for p in self.plans
            ],
            "recommendations": [
                "Revisar planes pendientes y asignar prioridades",
                "Verificar la efectividad de las mitigaciones implementadas",
                "Actualizar el plan de respuesta a incidentes"
            ]
        }

# Ejemplo de uso
plan_gen = MitigationPlanGenerator()

# Añadir planes de mitigación
plan_gen.add_plan(RiskMitigationPlan(
    risk_id="R-001",
    risk_description="Ataque DDoS a pfSense",
    mitigation_action="Implementar limitación de conexiones y protección DDoS",
    responsible="Equipo de Redes",
    deadline=(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
    status="IN_PROGRESS"
))

plan_gen.add_plan(RiskMitigationPlan(
    risk_id="R-002",
    risk_description="Fuerza Bruta SSH",
    mitigation_action="Cerrar puerto SSH y usar autenticación de clave pública",
    responsible="Equipo de Seguridad",
    deadline=(datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
    status="PENDING"
))

plan_gen.add_plan(RiskMitigationPlan(
    risk_id="R-004",
    risk_description="Inyección de Prompts en Chatbot IA",
    mitigation_action="Implementar reglas de Suricata para detección de inyección de prompts",
    responsible="Equipo de IA",
    deadline=(datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
    status="PENDING"
))

plan_gen.add_plan(RiskMitigationPlan(
    risk_id="R-003",
    risk_description="pfSense desactualizado",
    mitigation_action="Actualizar pfSense a la última versión",
    responsible="Equipo de Redes",
    deadline=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
    status="COMPLETED"
))

report = plan_gen.generate_report()

print("📊 INFORME DE PLAN DE MITIGACIÓN DE RIESGOS")
print(f"Total de planes: {report['total_plans']}")
print(f"Por estado: {report['by_status']}")

print("\n📋 PLANES DE MITIGACIÓN:")
for p in report['plans']:
    print(f"  {p['risk_id']}: {p['risk_description']}")
    print(f"    Acción: {p['action']}")
    print(f"    Responsable: {p['responsible']}")
    print(f"    Plazo: {p['deadline']}")
    print(f"    Estado: {p['status']}")
