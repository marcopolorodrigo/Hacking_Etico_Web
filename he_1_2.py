from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class Jurisdiction(Enum):
    UE = "Unión Europea"
    USA = "Estados Unidos"
    MEXICO = "México"
    BRASIL = "Brasil"
    ECUADOR = "Ecuador"

@dataclass
class LegalAssessment:
    """Evaluación de legalidad de un pentesting"""
    jurisdiction: Jurisdiction
    requires_consent: bool
    requires_authorization: bool
    regulations: List[str]
    restrictions: List[str]

class LegalComplianceChecker:
    """
    Verificador de cumplimiento legal para pentesting.
    """
    
    def __init__(self):
        self.legal_frameworks = {
            Jurisdiction.UE: {
                "consent": True,
                "authorization": True,
                "regulations": ["GDPR", "AI Act", "NIS2 Directive"],
                "restrictions": ["No acceder a datos personales sin consentimiento",
                               "Notificar brechas en 72 horas"]
            },
            Jurisdiction.USA: {
                "consent": True,
                "authorization": True,
                "regulations": ["CFAA", "CCPA", "HIPAA", "PCI DSS"],
                "restrictions": ["No exceder el alcance autorizado",
                               "No causar daños a sistemas críticos"]
            },
            Jurisdiction.MEXICO: {
                "consent": True,
                "authorization": True,
                "regulations": ["LFPDPPP", "Código Penal Federal"],
                "restrictions": ["No procesar datos personales sin consentimiento"]
            },
            Jurisdiction.ECUADOR: {
                "consent": True,
                "authorization": True,
                "regulations": ["Ley de Protección de Datos Personales", "Código Penal"],
                "restrictions": ["No realizar pruebas en sistemas gubernamentales sin autorización especial"]
            }
        }
    
    def check(self, jurisdiction: Jurisdiction, 
              target_type: str, consent_obtained: bool) -> LegalAssessment:
        """
        Verifica si un pentesting es legal en una jurisdicción dada.
        """
        framework = self.legal_frameworks.get(jurisdiction)
        if not framework:
            return LegalAssessment(
                jurisdiction=jurisdiction,
                requires_consent=True,
                requires_authorization=True,
                regulations=["Consultar legislación local"],
                restrictions=["Realizar evaluación legal detallada"]
            )
        
        restrictions = framework["restrictions"].copy()
        
        # Restricciones adicionales según tipo de sistema
        if target_type == "government":
            restrictions.append("Requiere autorización gubernamental especial")
        elif target_type == "healthcare":
            restrictions.append("Cumplir con HIPAA (USA) o normativas de salud locales")
        elif target_type == "ai_system":
            restrictions.append("Cumplir con AI Act (UE) si aplica")
            restrictions.append("Realizar evaluación de impacto algorítmico")
        
        if not consent_obtained:
            restrictions.append("⚠️ CONSENTIMIENTO NO OBTENIDO - ACTIVIDAD ILEGAL")
        
        return LegalAssessment(
            jurisdiction=jurisdiction,
            requires_consent=framework["consent"],
            requires_authorization=framework["authorization"],
            regulations=framework["regulations"],
            restrictions=restrictions
        )

# Ejemplo de uso
checker = LegalComplianceChecker()

# Evaluar pentesting en Ecuador
assessment = checker.check(
    jurisdiction=Jurisdiction.ECUADOR,
    target_type="financial_system",
    consent_obtained=True
)

print(f"Jurisdicción: {assessment.jurisdiction.value}")
print(f"Requiere consentimiento: {assessment.requires_consent}")
print(f"Regulaciones: {', '.join(assessment.regulations)}")
print(f"Restricciones:")
for r in assessment.restrictions:
    print(f"  - {r}")
