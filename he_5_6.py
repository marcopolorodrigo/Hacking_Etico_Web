from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class TrainingModule:
    """Módulo de formación en cumplimiento de IA"""
    id: str
    title: str
    description: str
    duration_minutes: int
    mandatory: bool
    completed: bool = False

class ComplianceTrainingProgram:
    """
    Programa de formación en cumplimiento para IA.
    """
    
    def __init__(self, organization: str):
        self.organization = organization
        self.modules: List[TrainingModule] = []
        self._initialize_modules()
    
    def _initialize_modules(self):
        self.modules = [
            TrainingModule(
                id="T-001",
                title="GDPR y Protección de Datos",
                description="Principios del GDPR y su aplicación en IA",
                duration_minutes=60,
                mandatory=True
            ),
            TrainingModule(
                id="T-002",
                title="AI Act y Cumplimiento Normativo",
                description="Clasificación de riesgos y obligaciones del AI Act",
                duration_minutes=90,
                mandatory=True
            ),
            TrainingModule(
                id="T-003",
                title="Ética en IA y Sesgos",
                description="Identificación y mitigación de sesgos en sistemas de IA",
                duration_minutes=60,
                mandatory=True
            ),
            TrainingModule(
                id="T-004",
                title="LFPDPPP y Protección de Datos en México",
                description="Requisitos de la LFPDPPP para sistemas de IA",
                duration_minutes=45,
                mandatory=False
            ),
            TrainingModule(
                id="T-005",
                title="Seguridad en IA y Prácticas de Hacking Ético",
                description="Riesgos de seguridad en IA y prácticas éticas",
                duration_minutes=90,
                mandatory=True
            )
        ]
    
    def complete_module(self, module_id: str, user_id: str) -> bool:
        """Marca un módulo como completado por un usuario"""
        for module in self.modules:
            if module.id == module_id:
                module.completed = True
                return True
        return False
    
    def get_user_progress(self, user_id: str) -> Dict:
        """Obtiene el progreso de un usuario"""
        total = len(self.modules)
        completed = len([m for m in self.modules if m.completed])
        mandatory = [m for m in self.modules if m.mandatory]
        mandatory_completed = len([m for m in mandatory if m.completed])
        mandatory_total = len(mandatory)
        
        return {
            "user_id": user_id,
            "total_modules": total,
            "completed_modules": completed,
            "progress": round((completed / total) * 100, 1),
            "mandatory_progress": round((mandatory_completed / mandatory_total) * 100, 1) if mandatory_total > 0 else 0,
            "modules": [
                {
                    "id": m.id,
                    "title": m.title,
                    "duration": m.duration_minutes,
                    "mandatory": m.mandatory,
                    "status": "COMPLETED" if m.completed else "PENDING"
                }
                for m in self.modules
            ]
        }
    
    def generate_certificate(self, user_id: str) -> str:
        """Genera un certificado de cumplimiento"""
        progress = self.get_user_progress(user_id)
        if progress['mandatory_progress'] < 100:
            return "Certificado NO disponible - módulos obligatorios incompletos"
        
        return f"""
        CERTIFICADO DE CUMPLIMIENTO
        ============================
        Organización: {self.organization}
        Usuario: {user_id}
        Fecha: {datetime.now().strftime('%Y-%m-%d')}
        
        Módulos completados: {progress['completed_modules']}/{progress['total_modules']}
        Módulos obligatorios: {int(progress['mandatory_progress'])}%
        
        Certificado de cumplimiento en regulaciones y ética de IA.
        """

# Ejemplo de uso
training = ComplianceTrainingProgram("Banco Nacional S.A.")

# Simular completar módulos
training.complete_module("T-001", "juan.perez")
training.complete_module("T-002", "juan.perez")
training.complete_module("T-003", "juan.perez")

progress = training.get_user_progress("juan.perez")
print(f"📚 PROGRESO DE FORMACIÓN EN CUMPLIMIENTO")
print(f"Usuario: {progress['user_id']}")
print(f"Progreso total: {progress['progress']}%")
print(f"Progreso obligatorio: {progress['mandatory_progress']}%")

print(f"\n📋 MÓDULOS:")
for m in progress['modules']:
    status = "✅" if m['status'] == "COMPLETED" else "⬜"
    mandatory = " (Obligatorio)" if m['mandatory'] else ""
    print(f"  {status} {m['title']}{mandatory}")

print("\n" + training.generate_certificate("juan.perez"))
