from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class GDPRRequirement:
    article: str
    description: str
    status: str  # "CUMPLE", "PARCIAL", "INCUMPLE"
    evidence: str

class GDPRComplianceChecker:
    """
    Verificador de cumplimiento GDPR para sistemas de IA y web scraping.
    """
    
    def __init__(self, system_name: str):
        self.system_name = system_name
        self.requirements: List[GDPRRequirement] = []
        self._initialize_requirements()
    
    def _initialize_requirements(self):
        self.requirements = [
            GDPRRequirement(
                article="Art. 6 (Legalidad)",
                description="Base legal para el procesamiento de datos personales (scraping)",
                status="PARCIAL",
                evidence="Interés legítimo evaluado, pero no documentado formalmente"
            ),
            GDPRRequirement(
                article="Art. 13 (Transparencia)",
                description="Información a los usuarios sobre el procesamiento de datos",
                status="INCUMPLE",
                evidence="No se informa a los usuarios sobre el scraping de sus datos"
            ),
            GDPRRequirement(
                article="Art. 22 (Decisiones automatizadas)",
                description="Derecho a no ser sujeto a decisiones automatizadas",
                status="INCUMPLE",
                evidence="No se ofrece opción de revisión humana para decisiones automatizadas"
            ),
            GDPRRequirement(
                article="Art. 25 (Privacy by Design)",
                description="Protección de datos desde el diseño",
                status="PARCIAL",
                evidence="Algunas medidas de privacidad implementadas, pero no desde el inicio"
            ),
            GDPRRequirement(
                article="Art. 32 (Seguridad)",
                description="Medidas de seguridad técnicas y organizativas",
                status="CUMPLE",
                evidence="Cifrado en reposo y en tránsito, control de acceso"
            ),
            GDPRRequirement(
                article="Art. 33 (Notificación de brechas)",
                description="Notificación en 72 horas de brechas de datos",
                status="CUMPLE",
                evidence="Plan de respuesta a incidentes implementado"
            ),
            GDPRRequirement(
                article="Art. 35 (DPIA)",
                description="Evaluación de impacto sobre la protección de datos",
                status="INCUMPLE",
                evidence="No se realizó DPIA para el sistema de IA"
            )
        ]
    
    def assess_web_scraping(self, data_source: str, is_sensitive: bool = False) -> Dict:
        """
        Evalúa el cumplimiento GDPR para actividades de web scraping en IA.
        """
        result = {
            "system": self.system_name,
            "data_source": data_source,
            "is_sensitive": is_sensitive,
            "compliance_status": "PENDIENTE",
            "issues": [],
            "recommendations": []
        }
        
        # Verificar base legal
        for req in self.requirements:
            if req.article == "Art. 6 (Legalidad)":
                if req.status == "PARCIAL":
                    result["issues"].append("Base legal no documentada adecuadamente")
                    result["recommendations"].append("Documentar formalmente la base legal (interés legítimo)")
        
        # Verificar transparencia
        for req in self.requirements:
            if req.article == "Art. 13 (Transparencia)":
                if req.status == "INCUMPLE":
                    result["issues"].append("Falta de transparencia sobre el scraping")
                    result["recommendations"].append("Actualizar el aviso de privacidad para incluir scraping")
        
        # Verificar datos sensibles
        if is_sensitive:
            result["issues"].append("Procesamiento de datos sensibles (Art. 9 GDPR)")
            result["recommendations"].append("Implementar medidas específicas para datos sensibles")
        
        # Determinar estado general
        if len(result["issues"]) == 0:
            result["compliance_status"] = "CUMPLE"
        elif len(result["issues"]) <= 2:
            result["compliance_status"] = "PARCIAL"
        else:
            result["compliance_status"] = "INCUMPLE"
        
        return result

# Ejemplo de uso
checker = GDPRComplianceChecker("Sistema de Entrenamiento de IA")
result = checker.assess_web_scraping(
    data_source="Redes Sociales (públicas)",
    is_sensitive=False
)

print("📋 EVALUACIÓN GDPR PARA WEB SCRAPING")
print(f"Sistema: {result['system']}")
print(f"Fuente de datos: {result['data_source']}")
print(f"Estado de cumplimiento: {result['compliance_status']}")

print("\n⚠️ PROBLEMAS IDENTIFICADOS:")
for issue in result['issues']:
    print(f"  - {issue}")

print("\n✅ RECOMENDACIONES:")
for rec in result['recommendations']:
    print(f"  - {rec}")
