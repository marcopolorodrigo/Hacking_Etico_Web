import subprocess
import time
from datetime import datetime
from typing import List, Dict

class AvailabilityMonitor:
    """
    Monitor de disponibilidad para simular el monitoreo de servicios en red.
    """
    
    def __init__(self, targets: List[str]):
        self.targets = targets
        self.results = []
    
    def check_host(self, host: str) -> Dict:
        """
        Verifica la disponibilidad de un host mediante ping.
        """
        try:
            # Simulación de ping (en producción se usaría subprocess)
            response_time = 0.5  # Simulación en ms
            status = "UP"
        except Exception:
            status = "DOWN"
            response_time = None
        
        return {
            "host": host,
            "status": status,
            "response_time_ms": response_time,
            "timestamp": datetime.now().isoformat()
        }
    
    def check_all(self) -> List[Dict]:
        """
        Verifica todos los hosts configurados.
        """
        for target in self.targets:
            result = self.check_host(target)
            self.results.append(result)
        return self.results
    
    def get_availability_report(self) -> Dict:
        """
        Genera un informe de disponibilidad.
        """
        total = len(self.results)
        up = len([r for r in self.results if r["status"] == "UP"])
        down = total - up
        
        return {
            "total_hosts": total,
            "up": up,
            "down": down,
            "availability": round((up / total) * 100, 2) if total > 0 else 0,
            "timestamp": datetime.now().isoformat()
        }

# Ejemplo de uso
monitor = AvailabilityMonitor(["192.168.1.1", "192.168.1.100", "10.0.0.1"])
monitor.check_all()
report = monitor.get_availability_report()

print("📊 INFORME DE DISPONIBILIDAD")
print(f"Hosts totales: {report['total_hosts']}")
print(f"  Activos: {report['up']}")
print(f"  Inactivos: {report['down']}")
print(f"Disponibilidad: {report['availability']}%")
