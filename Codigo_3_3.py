from dataclasses import dataclass, field
from typing import List, Dict
import json

@dataclass
class AIRMFAssessment:
    system_name: str
    governance: Dict = field(default_factory=dict)
    mapping: Dict = field(default_factory=dict)
    measurement: Dict = field(default_factory=dict)
    management: Dict = field(default_factory=dict)
    
    def assess_trustworthiness(self) -> Dict:
        """Evalúa las características de IA Confiable del NIST"""
        results = {
            "system": self.system_name,
            "valid_reliable": self._check_valid_reliable(),
            "safe": self._check_safe(),
            "secure_resilient": self._check_secure_resilient(),
            "explainable": self._check_explainable(),
            "private": self._check_private(),
            "fair": self._check_fair(),
            "overall_score": 0.0
        }
        
        # Calcular puntuación global (0-100)
        scores = [
            results["valid_reliable"]["score"],
            results["safe"]["score"],
            results["secure_resilient"]["score"],
            results["explainable"]["score"],
            results["private"]["score"],
            results["fair"]["score"]
        ]
        results["overall_score"] = sum(scores) / len(scores)
        
        return results
    
    def _check_valid_reliable(self) -> Dict:
        # Simulación: verificar precisión del modelo, deriva de datos
        return {"score": 85, "status": "GOOD", 
                "notes": "Precisión del 92% en validación cruzada. Deriva de datos detectada: 5%"}
    
    def _check_safe(self) -> Dict:
        # Simulación: verificar seguridad física y lógica
        return {"score": 70, "status": "NEEDS_IMPROVEMENT",
                "notes": "No se realizaron pruebas de adversarios. Recomendar pruebas de robustez."}
    
    def _check_secure_resilient(self) -> Dict:
        # Simulación: verificar protección contra ataques
        return {"score": 60, "status": "NEEDS_IMPROVEMENT",
                "notes": "Vulnerable a ataques de adversarial patch. Implementar defensas."}
    
    def _check_explainable(self) -> Dict:
        # Simulación: verificar explicabilidad (SHAP, LIME)
        return {"score": 75, "status": "GOOD",
                "notes": "SHAP implementado para explicaciones locales. Global explainability pendiente."}
    
    def _check_private(self) -> Dict:
        # Simulación: verificar protección de datos
        return {"score": 80, "status": "GOOD",
                "notes": "Datos anonimizados. Differential Privacy implementada en entrenamiento."}
    
    def _check_fair(self) -> Dict:
        # Simulación: verificar sesgos y equidad
        return {"score": 55, "status": "CRITICAL",
                "notes": "Sesgo detectado en predicciones para grupos minoritarios. Acción correctiva urgente."}

# Ejemplo: Evaluar un sistema de selección de personal basado en IA
assessment = AIRMFAssessment(
    system_name="Sistema de Selección de Personal IA v2.0",
    governance={"policy": "Ética IA aprobada 2025", "committee": "Comité de Ética activo"},
    mapping={"assets": ["CVs", "entrevistas"], "threats": ["sesgo", "discriminación"]},
    measurement={"tests": ["pruebas de sesgo", "pruebas de robustez"]},
    management={"controls": ["monitoreo continuo", "auditoría anual"]}
)

results = assessment.assess_trustworthiness()
print(json.dumps(results, indent=2, default=str))
