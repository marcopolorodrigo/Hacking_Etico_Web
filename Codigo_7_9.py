class EthicalAssessment:
    """
    Evaluación ética de hallazgos de pentesting en IA.
    """
    
    def __init__(self):
        self.ethical_principles = [
            "No acceder a datos personales innecesariamente",
            "No explotar vulnerabilidades más allá de lo necesario para la prueba",
            "Reportar sesgos y discriminación incluso si no son vulnerabilidades técnicas",
            "Coordinar divulgación responsable antes de cualquier publicación",
            "Considerar el impacto en grupos vulnerables"
        ]
    
    def assess_finding(self, finding: Dict) -> Dict:
        """
        Evalúa las implicaciones éticas de un hallazgo.
        """
        assessment = {
            "finding": finding["title"],
            "ethical_concerns": [],
            "required_actions": [],
            "recommendation": "APROBADO"
        }
        
        # Evaluar si implica acceso a datos personales
        if "personal" in finding["description"].lower() or "datos" in finding["description"].lower():
            assessment["ethical_concerns"].append("Acceso a datos personales")
            assessment["required_actions"].append("Anonimizar datos antes de documentar")
            assessment["recommendation"] = "REVISAR"
        
        # Evaluar si implica sesgo
        if "sesgo" in finding["description"].lower() or "discrimin" in finding["description"].lower():
            assessment["ethical_concerns"].append("Sesgo o discriminación detectada")
            assessment["required_actions"].append("Reportar al comité de ética de IA")
            assessment["recommendation"] = "REVISAR"
        
        # Evaluar si la explotación puede causar daño
        if "ejecutar" in finding["description"].lower() or "comando" in finding["description"].lower():
            assessment["ethical_concerns"].append("Posible ejecución de acciones maliciosas")
            assessment["required_actions"].append("Limitar pruebas a entorno de staging")
            assessment["recommendation"] = "REVISAR"
        
        return assessment

# Ejemplo de uso
ethical = EthicalAssessment()

finding = {
    "title": "Extracción de datos personales mediante inyección de prompts",
    "description": "Se puede extraer información de clientes mediante inyección de prompts específicos."
}

assessment = ethical.assess_finding(finding)
print(f"Evaluación ética de: {assessment['finding']}")
print(f"Preocupaciones: {assessment['ethical_concerns']}")
print(f"Acciones requeridas: {assessment['required_actions']}")
print(f"Recomendación: {assessment['recommendation']}")
