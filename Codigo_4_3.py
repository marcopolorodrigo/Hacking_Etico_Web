class OCTAVEAIAssessment:
    def __init__(self, organization):
        self.org = organization
        self.assets = []
        self.threats = []
        self.vulnerabilities = []
        self.risks = []
    
    def identify_assets(self):
        # Simulación de identificación de activos en un pipeline de IA
        self.assets = [
            {"name": "Datos de entrenamiento", "type": "data", "criticality": "high"},
            {"name": "Modelo LLM", "type": "model", "criticality": "critical"},
            {"name": "API de inferencia", "type": "service", "criticality": "high"},
            {"name": "Prompts del sistema", "type": "configuration", "criticality": "medium"}
        ]
        return self.assets
    
    def identify_threats(self):
        self.threats = [
            {"name": "Data Poisoning", "source": "externo", "impact": "alteración de comportamiento"},
            {"name": "Prompt Injection", "source": "externo", "impact": "exfiltración de datos"},
            {"name": "Model Stealing", "source": "externo", "impact": "pérdida de propiedad intelectual"},
            {"name": "Sesgo interno", "source": "interno", "impact": "discriminación"}
        ]
        return self.threats
    
    def identify_vulnerabilities(self):
        self.vulnerabilities = [
            {"name": "Falta de validación de prompts", "asset": "API"},
            {"name": "Permisos excesivos en modelo", "asset": "Modelo LLM"},
            {"name": "Ausencia de monitoreo de deriva", "asset": "Datos de entrenamiento"}
        ]
        return self.vulnerabilities
    
    def assess_risks(self):
        # Simulación de cálculo de riesgo (impacto * probabilidad)
        for threat in self.threats:
            for vuln in self.vulnerabilities:
                # Asignar probabilidad e impacto de forma subjetiva (simulación)
                likelihood = 0.7 if "externa" in threat["source"] else 0.4
                impact = 0.9 if "crítico" in vuln["asset"].lower() else 0.5
                risk_score = likelihood * impact * 10
                self.risks.append({
                    "threat": threat["name"],
                    "vulnerability": vuln["name"],
                    "score": round(risk_score, 1),
                    "level": "ALTO" if risk_score >= 7 else "MEDIO" if risk_score >= 4 else "BAJO"
                })
        return self.risks

# Ejecutar evaluación
assessment = OCTAVEAIAssessment("TechCorp")
assets = assessment.identify_assets()
threats = assessment.identify_threats()
vulns = assessment.identify_vulnerabilities()
risks = assessment.assess_risks()

print("Activos identificados:", len(assets))
print("Amenazas identificadas:", len(threats))
print("Vulnerabilidades:", len(vulns))
print("Riesgos evaluados:")
for r in risks:
    print(f"  {r['threat']} + {r['vulnerability']} -> Score: {r['score']} ({r['level']})")
