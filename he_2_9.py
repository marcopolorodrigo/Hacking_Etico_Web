from typing import List, Dict
from enum import Enum

class AIPolicy(Enum):
    ALLOW = "allow"
    BLOCK = "block"
    LIMITED = "limited"

class AIApplicationControl:
    """
    Control de aplicaciones de IA según políticas.
    """
    
    def __init__(self):
        self.policies = {
            "chatgpt": AIPolicy.LIMITED,
            "claude": AIPolicy.LIMITED,
            "copilot": AIPolicy.ALLOW,
            "cursor": AIPolicy.ALLOW,
            "llama": AIPolicy.BLOCK,
            "bard": AIPolicy.BLOCK
        }
        self.usage_log = []
    
    def check_application(self, app_name: str, user_role: str) -> Dict:
        """Verifica si una aplicación de IA está permitida para un usuario"""
        policy = self.policies.get(app_name, AIPolicy.BLOCK)
        
        # Los usuarios con rol admin tienen más permisos
        if user_role == "admin" and policy == AIPolicy.LIMITED:
            policy = AIPolicy.ALLOW
        
        # Los usuarios regulares tienen restricciones adicionales
        if user_role == "user" and policy == AIPolicy.LIMITED:
            policy = AIPolicy.BLOCK if "sensitive_data" in self._get_user_permissions(user_role) else AIPolicy.LIMITED
        
        self.usage_log.append({
            "app": app_name,
            "user": user_role,
            "policy": policy.value,
            "time": datetime.now().isoformat()
        })
        
        return {
            "application": app_name,
            "user_role": user_role,
            "allowed": policy in [AIPolicy.ALLOW, AIPolicy.LIMITED],
            "limited": policy == AIPolicy.LIMITED,
            "policy": policy.value,
            "message": "Permitido" if policy == AIPolicy.ALLOW else "Limitado" if policy == AIPolicy.LIMITED else "Bloqueado"
        }
    
    def _get_user_permissions(self, role: str) -> List[str]:
        permissions = {
            "admin": ["sensitive_data", "full_access"],
            "developer": ["sensitive_data"],
            "user": []
        }
        return permissions.get(role, [])

# Ejemplo de uso
control = AIApplicationControl()

# Verificar aplicaciones
apps = ["chatgpt", "copilot", "cursor", "llama", "bard"]
roles = ["admin", "developer", "user"]

for role in roles:
    print(f"\n👤 Usuario: {role}")
    for app in apps:
        result = control.check_application(app, role)
        status = "✅" if result["allowed"] else "❌"
        if result["limited"]:
            status = "⚠️"
        print(f"  {status} {app}: {result['message']}")
