class AIEthicsAssessment:
    """
    Evaluación ética del uso de IA en hacking ético.
    """
    
    def __init__(self):
        self.ethical_concerns = {
            "sesgo": {
                "description": "La IA puede tener sesgos que afecten los resultados",
                "mitigation": "Auditar y validar los hallazgos de IA manualmente"
            },
            "falsos_positivos": {
                "description": "La IA puede generar hallazgos incorrectos",
                "mitigation": "Verificar cada hallazgo con pruebas manuales"
            },
            "privacidad": {
                "description": "La IA puede procesar datos sensibles",
                "mitigation": "Anonimizar datos antes de usar IA"
            },
            "sobredependencia": {
                "description": "Los pentesters pueden perder habilidades manuales",
                "mitigation": "Combinar IA con capacitación continua en técnicas manuales"
            },
            "seguridad_herramientas": {
                "description": "Las herramientas de IA pueden ser vulnerables",
                "mitigation": "Auditar y mantener actualizadas las herramientas"
            }
        }
    
    def assess(self, tool_name: str, use_case: str) -> Dict:
        """
        Evalúa las implicaciones éticas del uso de una herramienta de IA.
        """
        assessment = {
            "tool": tool_name,
            "use_case": use_case,
            "concerns": [],
            "recommendations": []
        }
        
        for key, concern in self.ethical_concerns.items():
            if key in use_case.lower() or key in tool_name.lower():
                assessment["concerns"].append(concern["description"])
                assessment["recommendations"].append(concern["mitigation"])
        
        if not assessment["concerns"]:
            assessment["recommendations"].append("Uso ético, continuar con buenas prácticas")
        
        return assessment

# Ejemplo de uso
ethics = AIEthicsAssessment()

tool = "Garak (AI LLM Scanner)"
use_case = "Escaneo de robustez de modelos LLM"

result = ethics.assess(tool, use_case)
print(f"🔍 EVALUACIÓN ÉTICA: {tool}")
print(f"Uso: {use_case}")
print(f"Preocupaciones: {result['concerns']}")
print(f"Recomendaciones: {result['recommendations']}")
