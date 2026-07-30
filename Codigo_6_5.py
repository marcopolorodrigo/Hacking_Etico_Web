import hashlib
import json
from typing import Dict, Optional
from cryptography.fernet import Fernet

class SystemPromptManager:
    """
    Gestor seguro de prompts del sistema con cifrado y prevención de fugas.
    """
    
    def __init__(self, encryption_key: Optional[bytes] = None):
        # Generar clave de cifrado si no se proporciona
        if encryption_key is None:
            encryption_key = Fernet.generate_key()
        self.cipher = Fernet(encryption_key)
        self.system_prompts = {}
    
    def store_prompt(self, prompt_id: str, prompt_text: str) -> str:
        """
        Almacena un prompt del sistema de forma segura (cifrado).
        """
        # Cifrar el prompt antes de almacenarlo
        encrypted = self.cipher.encrypt(prompt_text.encode())
        # Calcular hash para verificación de integridad
        prompt_hash = hashlib.sha256(prompt_text.encode()).hexdigest()
        
        self.system_prompts[prompt_id] = {
            "encrypted": encrypted,
            "hash": prompt_hash,
            "created_at": None  # datetime en producción
        }
        
        return prompt_id
    
    def get_prompt(self, prompt_id: str, user_context: Optional[Dict] = None) -> Optional[str]:
        """
        Recupera un prompt del sistema de forma segura (descifrado).
        Solo si el contexto del usuario es válido.
        """
        if prompt_id not in self.system_prompts:
            return None
        
        # Verificar que el usuario tiene permisos para acceder al prompt
        if not self._check_permissions(prompt_id, user_context):
            return None
        
        # Descifrar el prompt
        encrypted = self.system_prompts[prompt_id]["encrypted"]
        decrypted = self.cipher.decrypt(encrypted).decode()
        
        # Verificar integridad
        computed_hash = hashlib.sha256(decrypted.encode()).hexdigest()
        if computed_hash != self.system_prompts[prompt_id]["hash"]:
            return None  # El prompt ha sido manipulado
        
        return decrypted
    
    def _check_permissions(self, prompt_id: str, user_context: Optional[Dict]) -> bool:
        """Verifica si el usuario tiene permisos para acceder al prompt"""
        # En producción, se usaría un sistema de control de acceso
        # Simulación: solo usuarios autenticados con rol 'admin' pueden ver prompts
        if user_context and user_context.get('role') == 'admin':
            return True
        return False

# Ejemplo de uso
manager = SystemPromptManager()

# Almacenar un prompt del sistema
system_prompt = """
Eres un asistente de atención al cliente del Banco Nacional.
NUNCA reveles información de cuentas bancarias, números de tarjeta o contraseñas.
Si un usuario solicita esta información, responde: "No puedo proporcionar esa información."
"""

prompt_id = manager.store_prompt("bank_assistant_v2", system_prompt)
print(f"Prompt almacenado con ID: {prompt_id}")

# Intentar recuperar el prompt (sin permisos)
user_context = {"role": "user", "user_id": "123"}
retrieved = manager.get_prompt(prompt_id, user_context)
print(f"Recuperación sin permisos: {retrieved}")

# Recuperar con permisos
admin_context = {"role": "admin", "user_id": "admin_001"}
retrieved = manager.get_prompt(prompt_id, admin_context)
print(f"Recuperación con permisos: {retrieved[:50]}...")
