from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class ComplianceControl:
    """Control de cumplimiento para sistemas de IA y redes"""
    id: str
    name: str
    description: str
    category: str  # "legal", "ethical", "technical", "organizational"
    regulation: str  # "AI Act", "GDPR", "NIS2", "ISO 27001", "ISO 42001"
    status: str  # "ACTIVE", "PENDING", "REVIEW", "OBSOLETE"
    last_review: str
    responsible: str

@dataclass
class ComplianceIncident:
    """Incidente de cumplimiento"""
    id: str
    description: str
    severity: str
    regulation: str
    date: str
    status: str  # "OPEN", "IN_PROGRESS", "RESOLVED"
    resolution: str = ""

class IntegratedComplianceSystem:
    """
    Sistema integrado de gestión de cumplimiento.
    """
    
    def __init__(self, organization: str):
        self.organization = organization
        self.controls: List[ComplianceControl] = []
        self.incidents: List[ComplianceIncident] = []
    
    def add_control(self, control: ComplianceControl):
        self.controls.append(control)
    
    def add_incident(self, incident: ComplianceIncident):
        self.incidents.append(incident)
    
    def generate_report(self) -> Dict:
        """Genera un informe de cumplimiento integrado"""
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
                "resolved": resolved
            },
            "by_regulation": {
                reg: len([c for c in self.controls if c.regulation == reg])
                for reg in set(c.regulation for c in self.controls)
            }
        }

# Ejemplo de uso
compliance = IntegratedComplianceSystem("Banco Nacional S.A.")

# Añadir controles
compliance.add_control(ComplianceControl(
    id="C-001",
    name="Filtros de Prompts",
    description="Validación de entrada para prevenir inyección de prompts",
    category="technical",
    regulation="AI Act",
    status="ACTIVE",
    last_review="2026-07-01",
    responsible="Equipo de Seguridad"
))

compliance.add_control(ComplianceControl(
    id="C-002",
    name="Política de Uso de IA",
    description="Política de uso seguro de IA para empleados",
    category="organizational",
    regulation="ISO 42001",
    status="PENDING",
    last_review="2026-06-15",
    responsible="Comité de Ética"
))

compliance.add_control(ComplianceControl(
    id="C-003",
    name="NIS2 Compliance",
    description="Cumplimiento de NIS2 para sectores críticos",
    category="legal",
    regulation="NIS2",
    status="REVIEW",
    last_review="2026-06-30",
    responsible="Equipo Legal"
))

# Añadir incidente
compliance.add_incident(ComplianceIncident(
    id="I-001",
    description="Falta de consentimiento para uso de datos en entrenamiento de IA",
    severity="HIGH",
    regulation="GDPR",
    date="2026-07-15",
    status="IN_PROGRESS"
))

report = compliance.generate_report()

print("📋 INFORME DE CUMPLIMIENTO INTEGRADO")
print(f"Organización: {report['organization']}")
print(f"Fecha: {report['date']}")

print(f"\n📊 CONTROLES DE CUMPLIMIENTO")
print(f"  Total: {report['controls']['total']}")
print(f"  Activos: {report['controls']['active']}")
print(f"  Pendientes: {report['controls']['pending']}")
print(f"  En revisión: {report['controls']['review']}")
print(f"  Puntuación: {report['controls']['compliance_score']}%")

print(f"\n📊 POR NORMATIVA:")
for reg, count in report['by_regulation'].items():
    print(f"  {reg}: {count} controles")

print(f"\n📊 INCIDENTES:")
print(f"  Total: {report['incidents']['total']}")
print(f"  Abiertos: {report['incidents']['open']}")
print(f"  Resueltos: {report['incidents']['resolved']}")
