import hashlib
import os
from typing import Dict

class ModelHasher:
    """
    Generador de hashes para modelos de IA.
    """
    
    def __init__(self):
        self.algorithms = {
            "sha256": hashlib.sha256,
            "sha512": hashlib.sha512,
            "blake2b": hashlib.blake2b
        }
    
    def hash_model(self, model_path: str, algorithm: str = "sha256") -> Dict:
        """
        Calcula el hash de un modelo de IA.
        """
        if algorithm not in self.algorithms:
            raise ValueError(f"Algoritmo no soportado: {algorithm}")
        
        hasher = self.algorithms[algorithm]()
        
        try:
            with open(model_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hasher.update(chunk)
        except FileNotFoundError:
            return {
                "status": "ERROR",
                "message": f"Archivo no encontrado: {model_path}"
            }
        
        return {
            "model": model_path,
            "algorithm": algorithm,
            "hash": hasher.hexdigest(),
            "file_size": os.path.getsize(model_path),
            "status": "OK"
        }
    
    def verify_model(self, model_path: str, expected_hash: str, 
                     algorithm: str = "sha256") -> Dict:
        """
        Verifica la integridad de un modelo comparando su hash.
        """
        result = self.hash_model(model_path, algorithm)
        
        if result["status"] == "ERROR":
            return result
        
        is_valid = result["hash"] == expected_hash
        
        return {
            "model": model_path,
            "algorithm": algorithm,
            "is_valid": is_valid,
            "computed_hash": result["hash"],
            "expected_hash": expected_hash,
            "status": "VALID" if is_valid else "COMPROMETIDO",
            "message": "Hash verificado correctamente" if is_valid else "⚠️ HASH NO COINCIDE"
        }

# Ejemplo de uso
hasher = ModelHasher()

# Crear un modelo simulado
with open("modelo_simulado.pkl", "wb") as f:
    f.write(b"Pesos del modelo de IA")

# Calcular hash
result = hasher.hash_model("modelo_simulado.pkl", "sha256")
print(f"📊 HASH DEL MODELO")
print(f"Algoritmo: {result['algorithm']}")
print(f"Hash: {result['hash'][:20]}...")
print(f"Tamaño: {result['file_size']} bytes")

# Verificar integridad
expected_hash = result["hash"]  # Simular hash esperado
verification = hasher.verify_model("modelo_simulado.pkl", expected_hash)
print(f"\n🔍 VERIFICACIÓN DE INTEGRIDAD")
print(f"Estado: {verification['status']}")
print(f"Mensaje: {verification['message']}")

# Limpiar
os.remove("modelo_simulado.pkl")
