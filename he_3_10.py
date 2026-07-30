import os
import json
import hashlib
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
from typing import Dict, Optional

class AIKeyManagementSystem:
    """
    Sistema de gestión de claves para IA (AI-KMS).
    """
    
    def __init__(self, config_file: str = "key_management.json"):
        self.config_file = config_file
        self.keys = {}
        self.rotation_policies = {}
        self._load_keys()
    
    def _load_keys(self):
        try:
            with open(self.config_file, 'r') as f:
                data = json.load(f)
                self.keys = data.get('keys', {})
                self.rotation_policies = data.get('policies', {})
        except FileNotFoundError:
            self.keys = {}
            self.rotation_policies = {}
    
    def _save_keys(self):
        data = {
            'keys': self.keys,
            'policies': self.rotation_policies
        }
        with open(self.config_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def generate_key(self, key_id: str, algorithm: str = "AES-256", 
                    rotation_days: int = 90) -> Dict:
        """
        Genera una nueva clave criptográfica.
        """
        if algorithm == "AES-256":
            key = Fernet.generate_key()
            key_value = key.decode()
        else:
            key_value = os.urandom(32).hex()
        
        key_entry = {
            "id": key_id,
            "algorithm": algorithm,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(days=rotation_days)).isoformat(),
            "key": key_value,
            "status": "ACTIVE",
            "rotation_days": rotation_days
        }
        
        self.keys[key_id] = key_entry
        self.rotation_policies[key_id] = {"rotation_days": rotation_days}
        self._save_keys()
        
        return key_entry
    
    def get_key(self, key_id: str) -> Optional[Dict]:
        """
        Recupera una clave si está activa.
        """
        key = self.keys.get(key_id)
        if not key:
            return None
        
        # Verificar expiración
        expiry = datetime.fromisoformat(key["expires_at"])
        if datetime.now() > expiry:
            key["status"] = "EXPIRED"
            return None
        
        return key
    
    def rotate_key(self, key_id: str) -> Dict:
        """
        Rota una clave, generando una nueva y archivando la anterior.
        """
        old_key = self.keys.get(key_id)
        if old_key:
            old_key["status"] = "ARCHIVED"
        
        rotation_days = self.rotation_policies.get(key_id, {}).get("rotation_days", 90)
        new_key = self.generate_key(key_id, rotation_days=rotation_days)
        
        self._save_keys()
        return new_key
    
    def revoke_key(self, key_id: str):
        """
        Revoca una clave.
        """
        if key_id in self.keys:
            self.keys[key_id]["status"] = "REVOKED"
            self._save_keys()
    
    def list_keys(self, status: Optional[str] = None) -> list:
        if status:
            return [k for k in self.keys.values() if k["status"] == status]
        return list(self.keys.values())

# Ejemplo de uso
kms = AIKeyManagementSystem()

# Generar clave
key = kms.generate_key("model_encryption_key", rotation_days=60)
print(f"🔑 CLAVE GENERADA")
print(f"ID: {key['id']}")
print(f"Algoritmo: {key['algorithm']}")
print(f"Valida hasta: {key['expires_at']}")

# Recuperar clave
retrieved = kms.get_key("model_encryption_key")
if retrieved:
    print(f"\n🔐 CLAVE RECUPERADA: {retrieved['key'][:20]}...")

# Listar claves
keys = kms.list_keys(status="ACTIVE")
print(f"\n📋 CLAVES ACTIVAS: {len(keys)}")

# Rotar clave
new_key = kms.rotate_key("model_encryption_key")
print(f"\n🔄 CLAVE ROTADA: {new_key['key'][:20]}...")
