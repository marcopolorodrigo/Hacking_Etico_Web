# Simulación de verificación de SBOM con Python
import hashlib
import json

class SBOMVerifier:
    def __init__(self, sbom_file):
        with open(sbom_file, 'r') as f:
            self.sbom = json.load(f)

    def check_dependency(self, package_name, version):
        for dep in self.sbom.get('dependencies', []):
            if dep['name'] == package_name and dep['version'] == version:
                # Verificar hash SHA-256 de la librería
                expected_hash = dep['hash_sha256']
                # Simular hash del archivo descargado
                computed_hash = hashlib.sha256(f"{package_name}-{version}".encode()).hexdigest()
                if computed_hash == expected_hash:
                    return True, "Hash verificado"
                else:
                    return False, "Hash no coincide, posible manipulación"
        return False, "Paquete no encontrado en SBOM"

# Ejemplo de uso
sbom = {
    "dependencies": [
        {"name": "requests", "version": "2.31.0", "hash_sha256": "abc123..."},
        {"name": "numpy", "version": "1.26.0", "hash_sha256": "def456..."}
    ]
}
with open("sbom.json", "w") as f:
    json.dump(sbom, f)

verifier = SBOMVerifier("sbom.json")
ok, msg = verifier.check_dependency("requests", "2.31.0")
print(f"Verificación: {ok} - {msg}")
