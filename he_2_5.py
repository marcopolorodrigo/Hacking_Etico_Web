import subprocess
import json
from typing import List, Dict

class DependencyPatcher:
    """
    Gestor de parches para dependencias de IA.
    """
    
    def __init__(self):
        self.dependencies = []
        self.vulnerabilities = {}
    
    def scan_dependencies(self, requirements_file: str) -> List[Dict]:
        """Escanea dependencias en busca de vulnerabilidades conocidas"""
        # Simulación de escaneo (en producción usar Snyk, Trivy, etc.)
        vulnerable_packages = {
            "transformers": {"<4.30.0": ["CVE-2025-1234", "CVE-2025-5678"]},
            "torch": {"<2.0.0": ["CVE-2025-9012"]},
            "langchain": {"<0.1.0": ["CVE-2025-3456"]}
        }
        
        # Leer requirements.txt (simulado)
        dependencies = [
            {"name": "transformers", "version": "4.25.0"},
            {"name": "torch", "version": "1.13.0"},
            {"name": "langchain", "version": "0.0.8"}
        ]
        
        results = []
        for dep in dependencies:
            vulns = []
            for pkg, versions in vulnerable_packages.items():
                if dep['name'] == pkg:
                    for version_range, cves in versions.items():
                        if dep['version'] < version_range.replace('<', ''):
                            vulns.extend(cves)
            
            results.append({
                "package": dep['name'],
                "current_version": dep['version'],
                "vulnerabilities": vulns,
                "status": "VULNERABLE" if vulns else "SAFE"
            })
        
        return results
    
    def generate_report(self, scan_results: List[Dict]) -> Dict:
        """Genera un informe de parches recomendados"""
        vulnerable = [r for r in scan_results if r["status"] == "VULNERABLE"]
        
        report = {
            "total_packages": len(scan_results),
            "vulnerable_packages": len(vulnerable),
            "severity": {
                "CRITICAL": len([r for r in vulnerable if "CVE-2025" in str(r["vulnerabilities"])]),
                "HIGH": len([r for r in vulnerable if "CVE-2024" in str(r["vulnerabilities"])])
            },
            "recommendations": []
        }
        
        for v in vulnerable:
            report["recommendations"].append({
                "package": v["package"],
                "current_version": v["current_version"],
                "recommended_version": self._get_latest_version(v["package"]),
                "vulnerabilities": v["vulnerabilities"],
                "action": "PARCHE INMEDIATO" if "CVE-2025" in str(v["vulnerabilities"]) else "PARCHE PROGRAMADO"
            })
        
        return report
    
    def _get_latest_version(self, package: str) -> str:
        """Obtiene la última versión de un paquete (simulado)"""
        versions = {
            "transformers": "4.36.0",
            "torch": "2.1.0",
            "langchain": "0.1.0"
        }
        return versions.get(package, "latest")

# Ejemplo de uso
patcher = DependencyPatcher()
results = patcher.scan_dependencies("requirements.txt")
report = patcher.generate_report(results)

print("📊 INFORME DE VULNERABILIDADES EN DEPENDENCIAS")
print(f"Paquetes vulnerables: {report['vulnerable_packages']}/{report['total_packages']}")
print(f"Críticas: {report['severity']['CRITICAL']}, Altas: {report['severity']['HIGH']}")

print("\n📋 RECOMENDACIONES DE PARCHE:")
for rec in report["recommendations"]:
    print(f"  {rec['package']}: {rec['current_version']} -> {rec['recommended_version']} ({rec['action']})")
    if rec['vulnerabilities']:
        print(f"    CVEs: {', '.join(rec['vulnerabilities'])}")
