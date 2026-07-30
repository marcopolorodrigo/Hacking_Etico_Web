from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class Role(Enum):
    ADMIN = "admin"
    DATA_SCIENTIST = "data_scientist"
    DEVELOPER = "developer"
    USER = "user"
    GUEST = "guest"

@dataclass
class Permission:
    resource: str
    actions: List[str]  # ["read", "write", "execute", "delete"]

class AccessControl:
    """
    Sistema de control de acceso basado en roles (RBAC) para sistemas de IA.
    """
    
    def __init__(self):
        self.role_permissions = {
            Role.ADMIN: [
                Permission("models", ["read", "write", "delete", "deploy"]),
                Permission("data", ["read", "write", "delete"]),
                Permission("users", ["read", "write", "delete"]),
                Permission("logs", ["read"]),
            ],
            Role.DATA_SCIENTIST: [
                Permission("models", ["read", "write"]),
                Permission("data", ["read", "write"]),
                Permission("logs", ["read"]),
            ],
            Role.DEVELOPER: [
                Permission("models", ["read"]),
                Permission("data", ["read"]),
                Permission("logs", ["read"]),
            ],
            Role.USER: [
                Permission("models", ["read"]),
                Permission("data", ["read"]),
            ],
            Role.GUEST: [
                Permission("models", ["read"]),
            ]
        }
        self.user_roles = {}  # user_id -> Role
    
    def assign_role(self, user_id: str, role: Role):
        self.user_roles[user_id] = role
    
    def check_permission(self, user_id: str, resource: str, action: str) -> bool:
        """Verifica si un usuario tiene permiso para realizar una acción"""
        if user_id not in self.user_roles:
            return False
        
        role = self.user_roles[user_id]
        for perm in self.role_permissions.get(role, []):
            if perm.resource == resource and action in perm.actions:
                return True
        return False
    
    def enforce(self, user_id: str, resource: str, action: str) -> Dict:
        """Evalúa y aplica la política de control de acceso"""
        if not self.check_permission(user_id, resource, action):
            return {
                "status": "DENIED",
                "message": f"Usuario {user_id} no tiene permiso para {action} en {resource}",
                "action": "BLOCK"
            }
        return {
            "status": "ALLOWED",
            "message": f"Permiso concedido para {action} en {resource}",
            "action": "ALLOW"
        }

# Ejemplo de uso
ac = AccessControl()

# Asignar roles
ac.assign_role("alice", Role.ADMIN)
ac.assign_role("bob", Role.DATA_SCIENTIST)
ac.assign_role("charlie", Role.USER)

# Verificar permisos
print("Alice intentando desplegar un modelo:")
result = ac.enforce("alice", "models", "deploy")
print(f"  {result['status']}: {result['message']}")

print("\nCharlie intentando desplegar un modelo:")
result = ac.enforce("charlie", "models", "deploy")
print(f"  {result['status']}: {result['message']}")

print("\nBob intentando eliminar un modelo:")
result = ac.enforce("bob", "models", "delete")
print(f"  {result['status']}: {result['message']}")
