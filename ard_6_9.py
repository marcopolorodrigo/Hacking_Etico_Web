import hashlib
import json
from typing import Dict

class IntegrityVerifier:
    """
    Simulación de verificación de integridad de configuraciones en pfSense.
    """
    
    def __init__(self):
        self.hash_store = {}
    
    def store_hash(self, file_name: str, content: bytes) -> str:
        """
        Calcula y almacena el hash SHA-256 de un archivo.
        """
        file_hash = hashlib.sha256(content).hexdigest()
        self.hash_store[file_name] = file_hash
        return file_hash
    
    def verify_integrity(self, file_name: str, content: bytes) -> Dict:
        """
        Verifica la integridad de un archivo comparando su hash.
        """
        if file_name not in self.hash_store:
            return {"status": "NOT_FOUND", "message": "Hash no almacenado"}
        
        computed_hash = hashlib.sha256(content).hexdigest()
        stored_hash = self.hash_store[file_name]
        
        if computed_hash == stored_hash:
            return {"status": "VERIFIED", "message": "Integridad verificada"}
        else:
            return {"status": "COMPROMISED", "message": "El archivo ha sido alterado"}

# Ejemplo de uso
verifier = IntegrityVerifier()

# Simular archivo de configuración
config = {
    "hostname": "firewall",
    "lan_ip": "192.168.1.1",
    "rules": [{"action": "pass", "protocol": "tcp", "source": "192.168.1.0/24", "port": 80}]
}
config_content = json.dumps(config).encode()

# Almacenar hash
file_hash = verifier.store_hash("config.xml", config_content)
print(f"Hash almacenado: {file_hash[:20]}...")

# Verificar integridad (archivo sin modificar)
result = verifier.verify_integrity("config.xml", config_content)
print(f"Verificación: {result['status']} - {result['message']}")

# Modificar archivo y verificar nuevamente
config["hostname"] = "firewall_modificado"
modified_content = json.dumps(config).encode()
result = verifier.verify_integrity("config.xml", modified_content)
print(f"Verificación (modificado): {result['status']} - {result['message']}")
