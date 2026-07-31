from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Threat:
    """Representa una amenaza a la red"""
    id: str
    name: str
    category: str  # "external", "internal", "physical", "logical", "environmental", "ai_specific"
    description: str
    likelihood: str  # "HIGH", "MEDIUM", "LOW"
    impact: str  # "HIGH", "MEDIUM", "LOW"
    source: str
    affected_assets: List[str]

class ThreatIdentification:
    """
    Identificación de amenazas para redes con pfSense.
    """
    
    def __init__(self):
        self.threats: List[Threat] = []
        self._initialize_threats()
    
    def _initialize_threats(self):
        """Inicializa una lista de amenazas comunes en redes con pfSense"""
        self.threats = [
            Threat(
                id="T-001",
                name="Ataque DDoS",
                category="external",
                description="Ataque de denegación de servicio distribuido que inunda el firewall con tráfico malicioso",
                likelihood="HIGH",
                impact="HIGH",
                source="Internet",
                affected_assets=["pfSense", "Servidor Web", "VPN"]
            ),
            Threat(
                id="T-002",
                name="Escaneo de Puertos",
                category="external",
                description="Intentos de descubrir puertos abiertos y servicios vulnerables",
                likelihood="HIGH",
                impact="MEDIUM",
                source="Internet",
                affected_assets=["pfSense", "Servidor Web"]
            ),
            Threat(
                id="T-003",
                name="Fuerza Bruta SSH",
                category="external",
                description="Intentos repetitivos de autenticación SSH para obtener acceso no autorizado",
                likelihood="MEDIUM",
                impact="HIGH",
                source="Internet",
                affected_assets=["pfSense", "Servidor SSH"]
            ),
            Threat(
                id="T-004",
                name="Phishing",
                category="external",
                description="Correos electrónicos maliciosos que intentan robar credenciales",
                likelihood="HIGH",
                impact="MEDIUM",
                source="Internet",
                affected_assets=["Usuarios", "Servidor de Correo"]
            ),
            Threat(
                id="T-005",
                name="Inyección de Prompts en Chatbot IA",
                category="ai_specific",
                description="Manipulación del chatbot de IA mediante prompts maliciosos",
                likelihood="MEDIUM",
                impact="HIGH",
                source="Internet",
                affected_assets=["Chatbot IA", "Base de datos de clientes"]
            ),
            Threat(
                id="T-006",
                name="Fallo de Hardware",
                category="physical",
                description="Fallo del hardware del firewall o servidores",
                likelihood="MEDIUM",
                impact="HIGH",
                source="Interna",
                affected_assets=["pfSense", "Servidores"]
            )
        ]
    
    def add_threat(self, threat: Threat):
        self.threats.append(threat)
    
    def get_threats_by_category(self, category: str) -> List[Threat]:
        return [t for t in self.threats if t.category == category]
    
    def get_threats_by_likelihood(self, likelihood: str) -> List[Threat]:
        return [t for t in self.threats if t.likelihood == likelihood]
    
    def generate_report(self) -> Dict:
        """Genera un informe de amenazas"""
        return {
            "total_threats": len(self.threats),
            "by_category": {
                c: len([t for t in self.threats if t.category == c])
                for c in set(t.category for t in self.threats)
            },
            "by_likelihood": {
                l: len([t for t in self.threats if t.likelihood == l])
                for l in set(t.likelihood for t in self.threats)
            },
            "by_impact": {
                i: len([t for t in self.threats if t.impact == i])
                for i in set(t.impact for t in self.threats)
            },
            "threats": [
                {"id": t.id, "name": t.name, "category": t.category, "likelihood": t.likelihood, "impact": t.impact}
                for t in self.threats
            ]
        }

# Ejemplo de uso
threats = ThreatIdentification()
report = threats.generate_report()

print("📊 INFORME DE AMENAZAS")
print(f"Total de amenazas: {report['total_threats']}")
print(f"Por categoría: {report['by_category']}")
print(f"Por probabilidad: {report['by_likelihood']}")
print(f"Por impacto: {report['by_impact']}")
print("\nLista de amenazas:")
for t in report['threats']:
    print(f"  {t['id']}: {t['name']} ({t['category']}) - Prob: {t['likelihood']}, Impacto: {t['impact']}")
