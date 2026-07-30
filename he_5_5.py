from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class ComplianceControl:
    """Control de cumplimiento para sistemas de IA"""
    id: str
    name: str
    description: str
    category: str  # "legal", "ethical", "technical", "organizational"
    status: str  # "ACTIVE", "PENDING", "REVIEW", "OBSOLETE"
    last_review: str
    responsible: str

@dataclass
class ComplianceIncident:
    """Incidente de cumplimiento"""
    id: str
    description: str
    severity: str
    date: str
    status: str  # "OPEN", "IN_PROGRESS", "RESOLVED"
    resolution: str = ""

class ComplianceManagementSystem:
    """
    Sistema de gestión de cumplimiento para IA.
    """
    
    def __init__(self, organization: str):
        self.organization = organization
        self.controls: List[ComplianceControl] = []
        self.incidents: List[ComplianceIncident] = []
    
    def add_control(self, control: ComplianceControl):
        self.controls.append(control)
    
    def add_incident(self, incident: ComplianceIncident):
        self.incidents.append(incident)
    
    def resolve_incident(self, incident_id: str, resolution: str):
        for incident in self.incidents:
            if incident.id == incident_id:
                incident.status = "RESOLVED"
                incident.resolution = resolution
                return True
        return False
    
    def generate_report(self) -> Dict:
        """Genera un informe de cumplimiento"""
        total_controls = len(self.controls)
        active = len([c for c in self.controls if c.status == "ACTIVE"])
        pending = len([c for c in self.controls if c.status == "PENDING"])
        review = len([c for c in self.controls if c.status == "REVIEW"])
        
        open_incidents = len([i for i in self.incidents if i.status in ["OPEN", "IN_PROGRESS"]])
        resolved = len([i for i in self.incidents if i.status == "RESOLVED"])
        
        return {
            "organization": self.organization,
            "date": datetime.now().isoformat(),
            "controls": {
                "total": total_controls,
                "active": active,
                "pending": pending,
                "review": review,
                "compliance_score": round((active / total_controls) * 100, 1) if total_controls > 0 else 0
            },
            "incidents": {
                "total": len(self.incidents),
                "open": open_incidents,
                "resolved": resolved,
                "resolution_rate": round((resolved / len(self.incidents)) * 100, 1) if len(self.incidents) > 0 else 0
            },
            "details": {
                "controls": [
                    {
                        "id": c.id,
                        "name": c.name,
                        "status": c.status,
                        "responsible": c.responsible
                    }
                    for c in self.controls
                ],
                "open_incidents": [
                    {
                        "id": i.id,
                        "description": i.description,
                        "severity": i.severity,
                        "date": i.date
                    }
                    for i in self.incidents if i.status in ["OPEN", "IN_PROGRESS"]
                ]
            }
        }

# Ejemplo de uso
cms = ComplianceManagementSystem("Banco Nacional S.A.")

# Añadir controles
cms.add_control(ComplianceControl(
    id="C-001",
    name="Filtros de Prompts",
    description="Validación de entrada para prevenir inyección de prompts",
    category="technical",
    status="ACTIVE",
    last_review="2026-07-01",
    responsible="Equipo de Seguridad"
))

cms.add_control(ComplianceControl(
    id="C-002",
    name="Política de Uso de IA",
    description="Política de uso seguro de IA para empleados",
    category="organizational",
    status="PENDING",
    last_review="2026-06-15",
    responsible="Comité de Ética"
))

cms.add_control(ComplianceControl(
    id="C-003",
    name="AI Act Compliance",
    description="Cumplimiento de AI Act para sistemas de alto riesgo",
    category="legal",
    status="REVIEW",
    last_review="2026-06-30",
    responsible="Equipo Legal"
))

# Añadir incidentes
cms.add_incident(ComplianceIncident(
    id="I-001",
    description="Falta de consentimiento para uso de datos en entrenamiento de IA",
    severity="HIGH",
    date="2026-07-15",
    status="IN_PROGRESS"
))

report = cms.generate_report()

print("📋 INFORME DE CUMPLIMIENTO")
print(f"Organización: {report['organization']}")
print(f"Fecha: {report['date']}")

print(f"\n📊 CONTROLES DE CUMPLIMIENTO")
print(f"  Total: {report['controls']['total']}")
print(f"  Activos: {report['controls']['active']}")
print(f"  Pendientes: {report['controls']['pending']}")
print(f"  En revisión: {report['controls']['review']}")
print(f"  Puntuación: {report['controls']['compliance_score']}%")

print(f"\n📊 INCIDENTES")
print(f"  Total: {report['incidents']['total']}")
print(f"  Abiertos: {report['incidents']['open']}")
print(f"  Resueltos: {report['incidents']['resolved']}")
print(f"  Tasa de resolución: {report['incidents']['resolution_rate']}%")

if report['details']['open_incidents']:
    print("\n⚠️ INCIDENTES ABIERTOS:")
    for i in report['details']['open_incidents']:
        print(f"  [{i['severity']}] {i['id']}: {i['description']}")
