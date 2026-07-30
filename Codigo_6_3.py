import hashlib
import json
import os
from typing import Dict, List, Optional
from datetime import datetime

class SupplyChainVerifier:
    """
    Verificador de integridad de la cadena de suministro para dependencias de IA.
    """
    
    def __init__(self, sbom_path: Optional[str] = None):
        self.sbom = {}
        if sbom_path and os.path.exists(sbom_path):
            with open(sbom_path, 'r') as f:
                self.sbom = json.load(f)
    
    def generate_sbom(self, dependencies: List[Dict]) -> Dict:
        """
        Genera un SBOM (Software Bill of Materials) para las dependencias.
        """
        sbom = {
            "version": "1.0",
            "generated_at": datetime.now().isoformat(),
            "dependencies": []
        }
        
        for dep in dependencies:
            # Calcular hash SHA-256 del paquete (simulado)
            hash_val = hashlib.sha256(f"{dep['name']}-{dep['version']}".encode()).hexdigest()
            sbom["dependencies"].append({
                "name": dep['name'],
                "version": dep['version'],
                "hash_sha256": hash_val,
                "source": dep.get('source', 'unknown'),
                "license": dep.get('license', 'unknown')
            })
        
        return sbom
    
    def verify_package(self, package_name: str, version: str, 
                       expected_hash: str) -> Dict:
        """
        Verifica la integridad de un paquete comparando su hash.
        """
        # Calcular hash del paquete (simulado)
        computed_hash = hashlib.sha256(f"{package_name}-{version}".encode()).hexdigest()
        
        return {
            "package": package_name,
            "version": version,
            "expected_hash": expected_hash,
            "computed_hash": computed_hash,
            "is_valid": computed_hash == expected_hash,
            "status": "VALID" if computed_hash == expected_hash else "COMPROMETIDO"
        }
    
    def check_vulnerabilities(self) -> List[Dict]:
        """
        Verifica vulnerabilidades conocidas en dependencias.
        En producción, se usaría una API como Snyk o NVD.
        """
        # Simulación de vulnerabilidades conocidas
        vulnerable_packages = {
            "transformers": {"<4.30.0": ["CVE-2025-1234", "CVE-2025-5678"]},
            "torch": {"<2.0.0": ["CVE-2025-9012"]},
            "langchain": {"<0.1.0": ["CVE-2025-3456"]}
        }
        
        results = []
        for dep in self.sbom.get('dependencies', []):
            vulns = []
            for pkg, versions in vulnerable_packages.items():
                if dep['name'] == pkg:
                    for version_range, cves in versions.items():
                        # Verificación simplificada de versión
                        if dep['version'] < version_range.replace('<', ''):
                            vulns.extend(cves)
            
            results.append({
                "package": dep['name'],
                "version": dep['version'],
                "vulnerabilities": vulns,
                "status": "CRÍTICO" if vulns else "SEGURO"
            })
        
        return results

# Ejemplo de uso
verifier = SupplyChainVerifier()

# Generar SBOM para dependencias de un proyecto de IA
deps = [
    {"name": "transformers", "version": "4.36.0", "source": "PyPI", "license": "Apache-2.0"},
    {"name": "torch", "version": "2.1.0", "source": "PyPI", "license": "BSD-3-Clause"},
    {"name": "langchain", "version": "0.1.5", "source": "PyPI", "license": "MIT"}
]

sbom = verifier.generate_sbom(deps)
print("SBOM generado:")
print(json.dumps(sbom, indent=2))

# Verificar vulnerabilidades
vuln_results = verifier.check_vulnerabilities()
print("\nAnálisis de vulnerabilidades:")
for r in vuln_results:
    print(f"  {r['package']} {r['version']}: {r['status']}")
