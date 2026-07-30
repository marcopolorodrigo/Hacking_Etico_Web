import hashlib
import json
from typing import Dict, List

class ModelIntegrityChecker:
    """
    Verificador de integridad de modelos de IA mediante hashing.
    """
    
    def __init__(self):
        self.trusted_hashes = {}  # model_name -> hash
    
    def add_trusted_model(self, model_name: str, expected_hash: str):
        self.trusted_hashes[model_name] = expected_hash
    
    def check_model(self, model_name: str, model_path: str) -> Dict:
        """Verifica la integridad de un modelo comparando su hash"""
        if model_name not in self.trusted_hashes:
            return {
                "model": model_name,
                "status": "UNKNOWN",
                "message": "Modelo no registrado en la lista de confianza"
            }
        
        # Calcular hash del archivo
        sha256 = hashlib.sha256()
        with open(model_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        computed_hash = sha256.hexdigest()
        
        is_valid = computed_hash == self.trusted_hashes[model_name]
        
        return {
            "model": model_name,
            "status": "VALID" if is_valid else "COMPROMETIDO",
            "expected_hash": self.trusted_hashes[model_name],
            "computed_hash": computed_hash,
            "message": "Hash verificado correctamente" if is_valid else "⚠️ HASH NO COINCIDE - POSIBLE MANIPULACIÓN"
        }

# Ejemplo de uso
checker = ModelIntegrityChecker()

# Registrar modelos de confianza (hashes obtenidos de fuentes seguras)
checker.add_trusted_model("bert-base-uncased", "abc123def456...")
checker.add_trusted_model("gpt2", "789xyz012abc...")

# Verificar un modelo
result = checker.check_model("bert-base-uncased", "modelos/bert-base-uncased.bin")
print(f"Verificación: {result['status']}")
print(result['message'])
