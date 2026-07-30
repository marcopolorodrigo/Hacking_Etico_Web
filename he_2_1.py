from dataclasses import dataclass
from typing import List, Dict
from enum import Enum

class DefenseLayer(Enum):
    PHYSICAL = "Seguridad Física"
    NETWORK = "Seguridad de Red"
    HOST = "Seguridad de Host"
    APPLICATION = "Seguridad de Aplicación"
    DATA = "Seguridad de Datos"
    COGNITIVE = "Seguridad Cognitiva (IA)"

@dataclass
class DefenseControl:
    layer: DefenseLayer
    control_name: str
    description: str
    implemented: bool
    effectiveness: int  # 0-100

class DefenseInDepthAssessment:
    """
    Evaluación de la defensa en profundidad en un sistema con IA.
    """
    
    def __init__(self, system_name: str):
        self.system_name = system_name
        self.controls: List[DefenseControl] = []
    
    def add_control(self, control: DefenseControl):
        self.controls.append(control)
    
    def assess_layers(self) -> Dict:
        """Evalúa la cobertura de cada capa de defensa"""
        layers = {}
        for control in self.controls:
            if control.layer not in layers:
                layers[control.layer] = {"count": 0, "implemented": 0, "effectiveness": []}
            layers[control.layer]["count"] += 1
            if control.implemented:
                layers[control.layer]["implemented"] += 1
                layers[control.layer]["effectiveness"].append(control.effectiveness)
        
        # Calcular puntuación por capa
        for layer, data in layers.items():
            if data["implemented"] > 0:
                data["score"] = sum(data["effectiveness"]) / len(data["effectiveness"])
            else:
                data["score"] = 0
            data["coverage"] = (data["implemented"] / data["count"]) * 100 if data["count"] > 0 else 0
        
        return layers
    
    def generate_report(self) -> Dict:
        """Genera un informe de la evaluación"""
        layers = self.assess_layers()
        
        # Identificar capas débiles
        weak_layers = [layer.value for layer, data in layers.items() if data["score"] < 60]
        
        return {
            "system": self.system_name,
            "total_controls": len(self.controls),
            "implemented_controls": len([c for c in self.controls if c.implemented]),
            "layers": layers,
            "weak_layers": weak_layers,
            "overall_score": sum([data["score"] for data in layers.values()]) / len(layers) if layers else 0,
            "recommendations": self._generate_recommendations(weak_layers)
        }
    
    def _generate_recommendations(self, weak_layers: List[str]) -> List[str]:
        """Genera recomendaciones para capas débiles"""
        recommendations = []
        for layer in weak_layers:
            if "Física" in layer:
                recommendations.append("Implementar control de acceso físico y vigilancia")
            elif "Red" in layer:
                recommendations.append("Implementar firewalls de próxima generación y segmentación")
            elif "Host" in layer:
                recommendations.append("Implementar antivirus, parches y hardening")
            elif "Aplicación" in layer:
                recommendations.append("Implementar WAF, SAST y DAST")
            elif "Datos" in layer:
                recommendations.append("Implementar cifrado en reposo y en tránsito")
            elif "Cognitiva" in layer:
                recommendations.append("Implementar filtros de prompts, monitoreo de deriva y pruebas de robustez")
        return recommendations

# Ejemplo de uso
assessment = DefenseInDepthAssessment("Sistema de Asistente Virtual Bancario")

# Añadir controles
assessment.add_control(DefenseControl(
    layer=DefenseLayer.PHYSICAL,
    control_name="Control de acceso a servidores",
    description="Acceso restringido a salas de servidores con tarjeta RFID",
    implemented=True,
    effectiveness=85
))

assessment.add_control(DefenseControl(
    layer=DefenseLayer.NETWORK,
    control_name="Firewall perimetral",
    description="Firewall de próxima generación con IPS",
    implemented=True,
    effectiveness=80
))

assessment.add_control(DefenseControl(
    layer=DefenseLayer.APPLICATION,
    control_name="Filtros de prompts",
    description="Validación de entrada para prevenir inyección de prompts",
    implemented=False,
    effectiveness=0
))

assessment.add_control(DefenseControl(
    layer=DefenseLayer.COGNITIVE,
    control_name="Monitoreo de deriva de datos",
    description="Detección de cambios en la distribución de datos de entrada",
    implemented=False,
    effectiveness=0
))

# Generar informe
report = assessment.generate_report()
print("📊 INFORME DE DEFENSA EN PROFUNDIDAD")
print(f"Sistema: {report['system']}")
print(f"Controles implementados: {report['implemented_controls']}/{report['total_controls']}")
print("\nCapas evaluadas:")
for layer, data in report['layers'].items():
    status = "✅" if data["score"] >= 70 else "⚠️" if data["score"] >= 50 else "❌"
    print(f"  {status} {layer}: {data['score']:.1f}% (Cobertura: {data['coverage']:.1f}%)")

if report["weak_layers"]:
    print("\n⚠️ CAPAS DÉBILES IDENTIFICADAS:")
    for layer in report["weak_layers"]:
        print(f"  - {layer}")

print("\n📋 RECOMENDACIONES:")
for rec in report["recommendations"]:
    print(f"  - {rec}")
