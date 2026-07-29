from dataclasses import dataclass, field
from typing import List, Dict
import json
from datetime import datetime

@dataclass
class HighRiskAIDocumentation:
    system_name: str
    system_version: str
    purpose: str
    provider: str
    deployer: str
    data_sources: List[Dict] = field(default_factory=list)
    architecture: Dict = field(default_factory=dict)
    risk_assessment: Dict = field(default_factory=dict)
    test_results: Dict = field(default_factory=dict)
    monitoring_plan: Dict = field(default_factory=dict)
    
    def generate_documentation(self) -> Dict:
        """Genera la documentación completa para sistemas de alto riesgo"""
        return {
            "system_overview": {
                "name": self.system_name,
                "version": self.system_version,
                "purpose": self.purpose,
                "provider": self.provider,
                "deployer": self.deployer,
                "date": datetime.now().isoformat()
            },
            "data_governance": {
                "sources": self.data_sources,
                "protection_measures": [
                    "Cifrado en reposo y en tránsito",
                    "Control de acceso basado en roles",
                    "Anonimización de datos personales",
                    "Registro de auditoría de accesos"
                ]
            },
            "system_architecture": self.architecture,
            "risk_management": self.risk_assessment,
            "validation_testing": self.test_results,
            "post_market_monitoring": self.monitoring_plan,
            "conformity_declaration": {
                "status": "PENDIENTE_DE_EVALUACION",
                "standards_applied": [
                    "ISO/IEC 42001:2024",
                    "NIST AI RMF 1.0",
                    "AI Act Annex III requirements"
                ],
                "notified_body": "Pendiente de designación"
            }
        }

# Ejemplo: Documentación para sistema de selección de personal
doc = HighRiskAIDocumentation(
    system_name="Sistema de Selección de Personal IA",
    system_version="2.1.0",
    purpose="Preselección automatizada de candidatos para puestos de trabajo",
    provider="HR-Tech Solutions",
    deployer="Corporación Global S.A.",
    data_sources=[
        {"type": "CVs", "source": "Portal de empleo", "volume": "10,000+/mes"},
        {"type": "Entrevistas grabadas", "source": "Videoentrevistas", "volume": "500/mes"},
        {"type": "Evaluaciones psicotécnicas", "source": "Plataforma de testing", "volume": "1,000/mes"}
    ],
    architecture={
        "components": [
            "API Gateway (autenticación OAuth 2.1)",
            "Procesamiento de lenguaje natural (NLP)",
            "Motor de análisis de sentimiento",
            "Base de datos vectorial (embeddings)",
            "Sistema de recomendación",
            "Panel de administración"
        ],
        "data_flow": "CV -> NLP -> Embedding -> Recomendación -> Panel RRHH"
    },
    risk_assessment={
        "identified_risks": [
            {"type": "Sesgo", "severity": "CRÍTICO", "mitigation": "Auditoría de fairness"},
            {"type": "Privacidad", "severity": "ALTO", "mitigation": "Anonimización"},
            {"type": "Seguridad", "severity": "MEDIO", "mitigation": "Cifrado y control de acceso"}
        ]
    },
    test_results={
        "accuracy": "89%",
        "fairness_metrics": {"disparate_impact": 0.85},
        "robustness": "85% en pruebas adversariales",
        "explainability": "SHAP implementado"
    },
    monitoring_plan={
        "frequency": "Trimestral",
        "metrics": ["Precisión", "Sesgo", "Deriva de datos", "Satisfacción del usuario"],
        "responsibility": "Comité de Ética de IA",
        "reporting": "Informe anual a autoridades"
    }
)

# Generar documentación
documentation = doc.generate_documentation()
print(json.dumps(documentation, indent=2, default=str))
