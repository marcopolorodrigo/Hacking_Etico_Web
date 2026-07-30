from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Tool:
    name: str
    category: str
    description: str
    use_case: str

class PentestToolManager:
    """
    Gestor de herramientas de pentesting recomendadas en 2026.
    """
    
    def __init__(self):
        self.tools = [
            # Escaneo y reconocimiento
            Tool("Nmap", "Reconnaissance", "Escaneo de puertos y servicios", "Descubrimiento de activos"),
            Tool("Shodan", "Reconnaissance", "Búsqueda de dispositivos conectados a Internet", "OSINT"),
            Tool("Amass", "Reconnaissance", "Enumeración de subdominios", "OSINT"),
            
            # Análisis de vulnerabilidades
            Tool("Nessus", "Vulnerability Assessment", "Escáner de vulnerabilidades", "Identificación de CVEs"),
            Tool("OpenVAS", "Vulnerability Assessment", "Escáner open-source", "Auditoría de seguridad"),
            
            # Explotación
            Tool("Metasploit", "Exploitation", "Framework de explotación", "Pruebas de penetración"),
            Tool("Burp Suite", "Web Application", "Proxy de interceptación HTTP", "Pruebas de aplicaciones web"),
            Tool("SQLMap", "Web Application", "Automatización de SQL Injection", "Pruebas de bases de datos"),
            
            # Herramientas específicas de IA (2026)
            Tool("Garak", "AI Security", "Escaneo de robustez de LLM", "Pruebas de prompt injection"),
            Tool("Sec-PaLM", "AI Security", "Detección de prompts maliciosos", "Análisis de seguridad de IA"),
            Tool("Invicti + IA", "Web Application", "Escaneo de aplicaciones web con IA", "Detección de vulnerabilidades en APIs de IA"),
            
            # Post-explotación
            Tool("Mimikatz", "Post-Exploitation", "Extracción de credenciales", "Escalada de privilegios"),
            Tool("BloodHound", "Post-Exploitation", "Análisis de Active Directory", "Mapeo de privilegios"),
            
            # Forense y reporte
            Tool("Wireshark", "Analysis", "Análisis de tráfico de red", "Investigación forense"),
            Tool("TheHarvester", "OSINT", "Recopilación de correos y subdominios", "Reconocimiento pasivo")
        ]
    
    def search_by_category(self, category: str) -> List[Tool]:
        return [t for t in self.tools if t.category == category]
    
    def get_ai_security_tools(self) -> List[Tool]:
        return [t for t in self.tools if "AI" in t.name or "IA" in t.description or "LLM" in t.description]
    
    def recommend_tool(self, task: str) -> List[Tool]:
        recommendations = []
        for t in self.tools:
            if any(keyword in t.use_case.lower() for keyword in task.lower().split()):
                recommendations.append(t)
        return recommendations

# Ejemplo de uso
tool_mgr = PentestToolManager()

print("🔧 HERRAMIENTAS DE SEGURIDAD PARA IA")
for t in tool_mgr.get_ai_security_tools():
    print(f"  {t.name}: {t.description}")

print("\n📌 RECOMENDACIÓN PARA 'ESCANEO WEB'")
for t in tool_mgr.recommend_tool("escaneo web"):
    print(f"  {t.name} - {t.use_case}")
