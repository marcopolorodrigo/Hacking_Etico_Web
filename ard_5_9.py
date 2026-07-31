from typing import List, Dict

class RiskPrioritizer:
    """
    Priorización de vulnerabilidades basada en CVSS y EPSS.
    """
    
    def __init__(self):
        self.vulnerabilities = []
    
    def add_vulnerability(self, name: str, cvss_score: float, epss_score: float):
        self.vulnerabilities.append({
            "name": name,
            "cvss_score": cvss_score,
            "epss_score": epss_score
        })
    
    def classify_risk(self, cvss_score: float, epss_score: float) -> Dict:
        """Clasifica el riesgo según CVSS y EPSS"""
        # Determinar severidad CVSS
        if cvss_score >= 9.0:
            cvss_level = "CRITICAL"
        elif cvss_score >= 7.0:
            cvss_level = "HIGH"
        elif cvss_score >= 4.0:
            cvss_level = "MEDIUM"
        else:
            cvss_level = "LOW"
        
        # Determinar probabilidad EPSS
        if epss_score > 0.7:
            epss_level = "HIGH"
        elif epss_score > 0.3:
            epss_level = "MEDIUM"
        else:
            epss_level = "LOW"
        
        # Determinar acción
        if cvss_level == "CRITICAL" and epss_level == "HIGH":
            action = "PARCHE INMEDIATO (2 horas)"
        elif cvss_level == "CRITICAL" and epss_level in ["MEDIUM", "LOW"]:
            action = "PARCHE URGENTE (4 horas)"
        elif cvss_level == "HIGH" and epss_level == "HIGH":
            action = "PARCHE URGENTE (24 horas)"
        elif cvss_level in ["CRITICAL", "HIGH"] and epss_level == "LOW":
            action = "PARCHE PROGRAMADO (7 días)"
        else:
            action = "MONITOREAR Y CORREGIR EN MANTENIMIENTO"
        
        return {
            "cvss_level": cvss_level,
            "epss_level": epss_level,
            "action": action
        }
    
    def prioritize(self) -> List[Dict]:
        """Prioriza las vulnerabilidades"""
        results = []
        for vuln in self.vulnerabilities:
            risk = self.classify_risk(vuln["cvss_score"], vuln["epss_score"])
            results.append({
                "name": vuln["name"],
                "cvss_score": vuln["cvss_score"],
                "epss_score": vuln["epss_score"],
                "cvss_level": risk["cvss_level"],
                "epss_level": risk["epss_level"],
                "action": risk["action"]
            })
        
        # Ordenar por severidad (CVSS descendente)
        results.sort(key=lambda x: x["cvss_score"], reverse=True)
        return results
    
    def generate_report(self) -> Dict:
        """Genera un informe de priorización"""
        prioritized = self.prioritize()
        return {
            "total_vulnerabilities": len(prioritized),
            "by_action": {
                "PARCHE INMEDIATO": len([v for v in prioritized if "INMEDIATO" in v["action"]]),
                "PARCHE URGENTE": len([v for v in prioritized if "URGENTE" in v["action"]]),
                "PARCHE PROGRAMADO": len([v for v in prioritized if "PROGRAMADO" in v["action"]]),
                "MONITOREAR": len([v for v in prioritized if "MONITOREAR" in v["action"]])
            },
            "vulnerabilities": prioritized
        }

# Ejemplo de uso
prioritizer = RiskPrioritizer()

# Añadir vulnerabilidades (CVSS y EPSS simulados)
prioritizer.add_vulnerability("CVE-2026-1234 (pfSense RCE)", 9.8, 0.85)
prioritizer.add_vulnerability("CVE-2026-5678 (OpenVPN DoS)", 7.5, 0.45)
prioritizer.add_vulnerability("CVE-2026-9012 (Suricata bypass)", 6.8, 0.25)
prioritizer.add_vulnerability("CVE-2026-3456 (Unbound DNS cache)", 5.0, 0.10)

report = prioritizer.generate_report()

print("📊 INFORME DE PRIORIZACIÓN DE VULNERABILIDADES")
print(f"Total de vulnerabilidades: {report['total_vulnerabilities']}")
print(f"Por acción: {report['by_action']}")

print("\n📋 VULNERABILIDADES PRIORIZADAS:")
for v in report['vulnerabilities']:
    print(f"  {v['name']}")
    print(f"    CVSS: {v['cvss_score']} ({v['cvss_level']}) | EPSS: {v['epss_score']} ({v['epss_level']})")
    print(f"    ACCIÓN: {v['action']}")
