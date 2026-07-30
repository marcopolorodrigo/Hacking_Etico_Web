import hashlib
import json
from typing import Dict, List

class SupplyChainVerifier:
    def __init__(self, sbom_file: str):
        """
        sbom_file: archivo JSON con el Software Bill of Materials (SBOM)
        """
        with open(sbom_file, 'r') as f:
            self.sbom = json.load(f)
    
    def verify_model(self, model_name: str, model_path: str, expected_hash: str) -> Dict:
        """
        Verifica la integridad de un modelo comparando su hash SHA-256.
        """
        # Calcular hash del archivo del modelo
        sha256 = hashlib.sha256()
        with open(model_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        computed_hash = sha256.hexdigest()
        
        return {
            "model": model_name,
            "expected_hash": expected_hash,
            "computed_hash": computed_hash,
            "is_valid": computed_hash == expected_hash,
            "action": "APROBADO" if computed_hash == expected_hash else "RECHAZADO - Posible manipulación"
        }
    
    def check_dependencies(self) -> List[Dict]:
        """
        Verifica que todas las dependencias declaradas en el SBOM estén actualizadas y sean seguras.
        """
        results = []
        for dep in self.sbom.get('dependencies', []):
            # Simulación: en producción, se consultaría una base de datos de vulnerabilidades
            is_vulnerable = self._check_vulnerability(dep['name'], dep['version'])
            results.append({
                "package": dep['name'],
                "version": dep['version'],
                "is_vulnerable": is_vulnerable,
                "status": "CRÍTICO" if is_vulnerable else "SEGURO"
            })
        return results
    
    def _check_vulnerability(self, name: str, version: str) -> bool:
        # Simulación: vulnerabilidades conocidas en versiones antiguas
        vulnerable = {
            "transformers": {"<4.30.0": True},
            "torch": {"<2.0.0": True},
            "langchain": {"<0.1.0": True}
        }
        # Lógica simplificada
        return False  # En producción, se usaría una API como NVD o Snyk

# Ejemplo de uso (SBOM simulado)
sbom = {
    "dependencies": [
        {"name": "transformers", "version": "4.36.0"},
        {"name": "torch", "version": "2.1.0"},
        {"name": "langchain", "version": "0.1.0"}
    ]
}
with open("sbom.json", "w") as f:
    json.dump(sbom, f)

verifier = SupplyChainVerifier("sbom.json")
print(verifier.check_dependencies())
