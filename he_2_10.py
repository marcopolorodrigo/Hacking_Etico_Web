from dataclasses import dataclass
from typing import List, Dict

@dataclass
class AIDefenseControl:
    layer: str
    control_name: str
    description: str
    ai_enhanced: bool
    ai_component: str
    effectiveness: int

class AIIntegratedDefense:
    """
    Sistema de defensa en profundidad integrado con IA.
    """
    
    def __init__(self):
        self.controls: List[AIDefenseControl] = []
        self._initialize_controls()
    
    def _initialize_controls(self):
        """Inicializa los controles de defensa con integración de IA"""
        self.controls = [
            # Capa de red
            AIDefenseControl("Red", "Firewall NGFW", "Firewall con detección de amenazas", True, "ML detection", 85),
            AIDefenseControl("Red", "WAF", "Web Application Firewall", True, "Prompt detection", 80),
            
            # Capa de aplicación
            AIDefenseControl("Aplicación", "Filtro de Prompts", "Detección de inyección de prompts", True, "Zero-shot classification", 90),
            AIDefenseControl("Aplicación", "Sanitización de Salidas", "Filtrado de respuestas del LLM", True, "NER + regex", 75),
            
            # Capa de datos
            AIDefenseControl("Datos", "Cifrado de Modelos", "Cifrado de pesos del modelo", False, "None", 95),
            AIDefenseControl("Datos", "Monitoreo de Deriva", "Detección de cambios en datos", True, "KS Drift detection", 70),
            
            # Capa cognitiva
            AIDefenseControl("Cognitiva", "Pruebas de Robustez", "Red teaming automatizado", True, "Garak", 65),
            AIDefenseControl("Cognitiva", "Auditoría de Sesgos", "Detección de discriminación", True, "Fairness metrics", 60),
            AIDefenseControl("Cognitiva", "Control de Agentes", "Permisos de agentes de IA", True, "RBAC + ABAC", 80)
        ]
    
    def assess(self) -> Dict:
        """Evalúa la efectividad de la defensa integrada"""
        return {
            "total_controls": len(self.controls),
            "ai_enhanced": len([c for c in self.controls if c.ai_enhanced]),
            "average_effectiveness": sum(c.effectiveness for c in self.controls) / len(self.controls),
            "by_layer": self._assess_by_layer()
        }
    
    def _assess_by_layer(self) -> Dict:
        """Evalúa la efectividad por capa"""
        layers = {}
        for control in self.controls:
            if control.layer not in layers:
                layers[control.layer] = {"count": 0, "effectiveness": []}
            layers[control.layer]["count"] += 1
            layers[control.layer]["effectiveness"].append(control.effectiveness)
        
        for layer, data in layers.items():
            data["avg"] = sum(data["effectiveness"]) / len(data["effectiveness"])
        
        return layers

# Ejemplo de uso
defense = AIIntegratedDefense()
assessment = defense.assess()

print("🔒 EVALUACIÓN DE DEFENSA EN PROFUNDIDAD CON IA")
print(f"Total de controles: {assessment['total_controls']}")
print(f"Controles con IA: {assessment['ai_enhanced']}")
print(f"Efectividad promedio: {assessment['average_effectiveness']:.1f}%")

print("\n📊 POR CAPAS:")
for layer, data in assessment['by_layer'].items():
    print(f"  {layer}: {data['avg']:.1f}% ({data['count']} controles)")
