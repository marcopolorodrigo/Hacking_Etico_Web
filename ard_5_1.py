from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class NetworkAsset:
    """Representa un activo de red para la evaluación de riesgos"""
    id: str
    name: str
    type: str  # "hardware", "software", "data", "service", "personnel", "documentation"
    description: str
    ip_address: Optional[str] = None
    criticality: str = "MEDIUM"  # "CRITICAL", "HIGH", "MEDIUM", "LOW"
    owner: str = ""
    notes: str = ""

class AssetInventory:
    """
    Inventario de activos de red para evaluación de riesgos.
    """
    
    def __init__(self):
        self.assets: List[NetworkAsset] = []
    
    def add_asset(self, asset: NetworkAsset):
        self.assets.append(asset)
    
    def get_assets_by_criticality(self, criticality: str) -> List[NetworkAsset]:
        return [a for a in self.assets if a.criticality == criticality]
    
    def get_assets_by_type(self, asset_type: str) -> List[NetworkAsset]:
        return [a for a in self.assets if a.type == asset_type]
    
    def generate_report(self) -> Dict:
        """Genera un informe del inventario de activos"""
        return {
            "total_assets": len(self.assets),
            "by_type": {
                t: len([a for a in self.assets if a.type == t])
                for t in set(a.type for a in self.assets)
            },
            "by_criticality": {
                c: len([a for a in self.assets if a.criticality == c])
                for c in set(a.criticality for a in self.assets)
            },
            "critical_assets": [
                {"name": a.name, "type": a.type, "ip": a.ip_address}
                for a in self.assets if a.criticality == "CRITICAL"
            ]
        }

# Ejemplo de uso
inventory = AssetInventory()

# Añadir activos
inventory.add_asset(NetworkAsset(
    id="A-001", name="pfSense Firewall", type="hardware",
    description="Firewall perimetral de la red", ip_address="203.0.113.1",
    criticality="CRITICAL", owner="Equipo de Redes"
))

inventory.add_asset(NetworkAsset(
    id="A-002", name="Servidor Web", type="hardware",
    description="Servidor web de la empresa", ip_address="10.0.10.10",
    criticality="HIGH", owner="Equipo de Desarrollo"
))

inventory.add_asset(NetworkAsset(
    id="A-003", name="Base de Datos Clientes", type="data",
    description="Base de datos de clientes", ip_address="10.0.30.5",
    criticality="CRITICAL", owner="Equipo de Datos"
))

inventory.add_asset(NetworkAsset(
    id="A-004", name="Squid Proxy", type="software",
    description="Proxy de caché y filtrado", ip_address="10.0.20.10",
    criticality="MEDIUM", owner="Equipo de Redes"
))

inventory.add_asset(NetworkAsset(
    id="A-005", name="Suricata IDS/IPS", type="software",
    description="Sistema de detección y prevención de intrusiones", ip_address="10.0.20.11",
    criticality="HIGH", owner="Equipo de Seguridad"
))

report = inventory.generate_report()
print("📊 INFORME DE INVENTARIO DE ACTIVOS")
print(f"Total de activos: {report['total_assets']}")
print(f"Por tipo: {report['by_type']}")
print(f"Por criticidad: {report['by_criticality']}")
print("\nActivos críticos:")
for asset in report['critical_assets']:
    print(f"  - {asset['name']} ({asset['type']}) - IP: {asset['ip']}")
