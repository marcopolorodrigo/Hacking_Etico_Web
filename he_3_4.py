from typing import List, Dict
from dataclasses import dataclass

@dataclass
class TrainingModule:
    name: str
    description: str
    duration_minutes: int
    completed: bool = False

class SecurityAwarenessTraining:
    """
    Programa de concienciación en seguridad de IA.
    """
    
    def __init__(self, user_role: str):
        self.user_role = user_role
        self.modules = self._generate_modules()
    
    def _generate_modules(self) -> List[TrainingModule]:
        modules = [
            TrainingModule(
                "Fundamentos de IA",
                "Introducción a los riesgos de seguridad en IA",
                30
            ),
            TrainingModule(
                "Inyección de Prompts",
                "Cómo identificar y prevenir ataques de inyección de prompts",
                45
            ),
            TrainingModule(
                "Seguridad de Datos en IA",
                "Protección de datos sensibles en sistemas de IA",
                30
            ),
            TrainingModule(
                "Cumplimiento Normativo en IA",
                "AI Act, GDPR y otras regulaciones",
                30
            )
        ]
        
        # Módulos adicionales según rol
        if self.user_role in ["developer", "data_scientist"]:
            modules.append(TrainingModule(
                "Desarrollo Seguro con IA",
                "Prácticas de codificación segura para sistemas de IA",
                60
            ))
        
        if self.user_role in ["security", "admin"]:
            modules.append(TrainingModule(
                "Red Teaming de IA",
                "Pruebas de robustez y ataques adversariales",
                90
            ))
        
        return modules
    
    def complete_module(self, module_name: str):
        for module in self.modules:
            if module.name == module_name:
                module.completed = True
                return True
        return False
    
    def get_progress(self) -> Dict:
        total = len(self.modules)
        completed = len([m for m in self.modules if m.completed])
        
        return {
            "total_modules": total,
            "completed_modules": completed,
            "progress": (completed / total) * 100 if total > 0 else 0,
            "modules": [
                {
                    "name": m.name,
                    "description": m.description,
                    "duration": m.duration_minutes,
                    "status": "✅" if m.completed else "⬜"
                }
                for m in self.modules
            ]
        }

# Ejemplo de uso
training = SecurityAwarenessTraining("developer")
training.complete_module("Fundamentos de IA")
training.complete_module("Seguridad de Datos en IA")

progress = training.get_progress()
print(f"📚 PROGRESO DE CONCIENCIACIÓN EN IA")
print(f"Completado: {progress['completed_modules']}/{progress['total_modules']}")
print(f"Progreso: {progress['progress']:.1f}%")
print("\nMódulos:")
for m in progress['modules']:
    print(f"  {m['status']} {m['name']} ({m['duration']} min) - {m['description']}")
