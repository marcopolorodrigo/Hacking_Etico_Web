from enum import Enum
from typing import List, Dict, Optional
from datetime import datetime

class AIActRiskLevel(Enum):
    UNACCEPTABLE = "Riesgo Inaceptable (Prohibido)"
    HIGH = "Alto Riesgo"
    TRANSPARENCY = "Riesgo de Transparencia"
    MINIMAL = "Riesgo Mínimo"

class AIActClassification:
    """
    Clasificador de sistemas de IA según el AI Act.
    """
    
    def __init__(self, system_name: str):
        self.system_name = system_name
        self.risk_level = None
        self.obligations = []
    
    def classify(self, system_type: str, domain: str, 
                 is_interactive: bool = False,
                 generates_content: bool = False,
                 is_high_risk_domain: bool = False) -> Dict:
        """
        Clasifica el sistema según el AI Act.
        """
        # 1. Verificar riesgo inaceptable
        if system_type in ["social_scoring", "manipulative_subliminal", "csam_generation"]:
            self.risk_level = AIActRiskLevel.UNACCEPTABLE
            self.obligations = ["PROHIBIDO: No se puede comercializar o usar"]
            return self._generate_result()
        
        # 2. Verificar alto riesgo (Anexo III)
        high_risk_domains = [
            "employment", "education", "critical_infrastructure", 
            "law_enforcement", "credit_scoring", "healthcare", "justice"
        ]
        if domain in high_risk_domains or is_high_risk_domain:
            self.risk_level = AIActRiskLevel.HIGH
            self.obligations = [
                "Evaluación de conformidad (Anexo VI)",
                "Sistema de gestión de riesgos (Art. 9)",
                "Documentación técnica (Art. 11)",
                "Transparencia y supervisión humana (Art. 13-14)",
                "Registro en la base de datos de la UE (Art. 60)"
            ]
            return self._generate_result()
        
        # 3. Verificar riesgo de transparencia (Art. 50)
        if is_interactive or generates_content:
            self.risk_level = AIActRiskLevel.TRANSPARENCY
            self.obligations = [
                "Informar a los usuarios que interactúan con IA (Art. 50.1)",
                "Marcar contenido generado por IA (Art. 50.2)",
                "Informar sobre reconocimiento de emociones (Art. 50.3)"
            ]
            return self._generate_result()
        
        # 4. Riesgo mínimo
        self.risk_level = AIActRiskLevel.MINIMAL
        self.obligations = [
            "Códigos de conducta voluntarios (Art. 95)"
        ]
        return self._generate_result()
    
    def _generate_result(self) -> Dict:
        """Genera el resultado de la clasificación"""
        return {
            "system": self.system_name,
            "risk_level": self.risk_level.value if self.risk_level else "No clasificado",
            "obligations": self.obligations,
            "compliance_deadlines": self._get_deadlines(),
            "recommendations": self._get_recommendations()
        }
    
    def _get_deadlines(self) -> Dict:
        """Obtiene los plazos de cumplimiento"""
        if self.risk_level == AIActRiskLevel.TRANSPARENCY:
            return {
                "transparency_art50": "2 de agosto de 2026 (vigente)",
                "content_marking_grace": "2 de diciembre de 2026 (para sistemas existentes)"
            }
        elif self.risk_level == AIActRiskLevel.HIGH:
            return {
                "high_risk_annex3": "2 de diciembre de 2027",
                "annex1_products": "2 de agosto de 2028",
                "conformity_assessment": "Obligatorio desde el inicio"
            }
        return {}
    
    def _get_recommendations(self) -> List[str]:
        """Obtiene recomendaciones para el cumplimiento"""
        recs = []
        if self.risk_level == AIActRiskLevel.UNACCEPTABLE:
            recs.append("Suspender inmediatamente el sistema")
        elif self.risk_level == AIActRiskLevel.HIGH:
            recs.append("Iniciar evaluación de conformidad con un organismo notificado")
            recs.append("Implementar sistema de gestión de riesgos")
            recs.append("Documentar toda la arquitectura y datos del sistema")
        elif self.risk_level == AIActRiskLevel.TRANSPARENCY:
            recs.append("Implementar mensaje de interacción con IA en la interfaz de usuario")
            recs.append("Marcar contenido generado con metadatos machine-readable")
        return recs

# Ejemplo de uso
classifier = AIActClassification("Chatbot de Selección de Personal")

result = classifier.classify(
    system_type="chatbot",
    domain="employment",
    is_interactive=True,
    generates_content=True,
    is_high_risk_domain=True
)

print("📋 CLASIFICACIÓN AI ACT")
print(f"Sistema: {result['system']}")
print(f"Nivel de riesgo: {result['risk_level']}")
print(f"\nObligaciones:")
for o in result['obligations']:
    print(f"  - {o}")
print(f"\nPlazos:")
for key, value in result.get('compliance_deadlines', {}).items():
    print(f"  - {key}: {value}")
print(f"\nRecomendaciones:")
for r in result.get('recommendations', []):
    print(f"  - {r}")
