from enum import Enum
from dataclasses import dataclass
from typing import List, Dict

class RiskLevel(Enum):
    CRITICO = "CRITICO"
    ALTO = "ALTO"
    MEDIO = "MEDIO"
    BAJO = "BAJO"

@dataclass
class Risk:
    id: str
    description: str
    category: str  # "tecnico", "etico", "legal", "social"
    likelihood: float  # 0-1
    impact: float      # 0-1
    mitigation: str
    status: str = "IDENTIFICADO"

class ISO42001RiskManager:
    def __init__(self):
        self.risks: List[Risk] = []
    
    def add_risk(self, risk: Risk):
        self.risks.append(risk)
    
    def evaluate_risk(self, risk: Risk) -> RiskLevel:
        score = risk.likelihood * risk.impact * 10
        if score >= 8:
            return RiskLevel.CRITICO
        elif score >= 5:
            return RiskLevel.ALTO
        elif score >= 3:
            return RiskLevel.MEDIO
        else:
            return RiskLevel.BAJO
    
    def generate_risk_report(self) -> Dict:
        report = {
            "total_risks": len(self.risks),
            "critical_risks": 0,
            "high_risks": 0,
            "medium_risks": 0,
            "low_risks": 0,
            "risks_by_category": {}
        }
        for risk in self.risks:
            level = self.evaluate_risk(risk)
            if level == RiskLevel.CRITICO:
                report["critical_risks"] += 1
            elif level == RiskLevel.ALTO:
                report["high_risks"] += 1
            elif level == RiskLevel.MEDIO:
                report["medium_risks"] += 1
            else:
                report["low_risks"] += 1
            
            # Agrupar por categoría
            if risk.category not in report["risks_by_category"]:
                report["risks_by_category"][risk.category] = 0
            report["risks_by_category"][risk.category] += 1
        
        return report

# Ejemplo de uso
iso42001 = ISO42001RiskManager()
iso42001.add_risk(Risk("R001", "Envenenamiento de datos de entrenamiento", "tecnico", 0.7, 0.9, "Validación de datos y detección de outliers"))
iso42001.add_risk(Risk("R002", "Sesgo de género en predicciones", "etico", 0.6, 0.8, "Auditoría de fairness y reweighting"))
iso42001.add_risk(Risk("R003", "Incumplimiento de AI Act", "legal", 0.4, 0.9, "Evaluación de conformidad y documentación"))
print(iso42001.generate_risk_report())
