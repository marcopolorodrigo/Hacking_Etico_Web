from enum import Enum
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass

class PermissionLevel(Enum):
    READ_ONLY = "read_only"
    LIMITED_WRITE = "limited_write"
    FULL_WRITE = "full_write"
    ADMIN = "admin"

@dataclass


class ToolPermission:
    """Permiso para una herramienta específica"""
    tool_name: str
    allowed_actions: List[str]
    requires_approval: bool = True

class AgentPermissionManager:
    """
    Gestor de permisos para agentes de IA que previene Excessive Agency.
    """
        
    def __init__(self):
        self.permissions = {
            "read_file": ToolPermission("read_file", ["read"], requires_approval=False),
            "write_file": ToolPermission("write_file", ["write", "modify"], requires_approval=True),
            "execute_command": ToolPermission("execute_command", ["execute"], requires_approval=True),
            "network_request": ToolPermission("network_request", ["get", "post"], requires_approval=True),
            "database_query": ToolPermission("database_query", ["select"], requires_approval=True),
            "deploy": ToolPermission("deploy", ["deploy"], requires_approval=True)
        }
        self.approval_queue = []
    
    def check_permission(self, tool_name: str, action: str, 
                        user_context: Dict) -> Dict:
        """
        Verifica si un agente tiene permiso para ejecutar una acción.
        """
        if tool_name not in self.permissions:
            return {"allowed": False, "reason": f"Herramienta desconocida: {tool_name}"}
        
        perm = self.permissions[tool_name]
        
        # Verificar que la acción está permitida
        if action not in perm.allowed_actions:
            return {"allowed": False, "reason": f"Acción no permitida: {action}"}
        
        # Verificar si requiere aprobación humana
        if perm.requires_approval:
            # En producción, aquí se enviaría una notificación a un humano
            approval_id = self._request_approval(tool_name, action, user_context)
            return {
                "allowed": False,  # Temporalmente bloqueado
                "requires_approval": True,
                "approval_id": approval_id,
                "reason": "La acción requiere aprobación humana"
            }
        
        return {"allowed": True}
    
    def _request_approval(self, tool_name: str, action: str, 
                        user_context: Dict) -> str:
        """Solicita aprobación humana para una acción"""
        import uuid
        approval_id = str(uuid.uuid4())[:8]
        self.approval_queue.append({
            "id": approval_id,
            "tool": tool_name,
            "action": action,
            "user": user_context.get('user_id', 'unknown'),
            "status": "pending"
        })
        return approval_id
    
    def approve_action(self, approval_id: str) -> bool:
        """Aprueba una acción previamente bloqueada"""
        for item in self.approval_queue:
            if item["id"] == approval_id:
                item["status"] = "approved"
                return True
        return False

# Ejemplo de uso
perm_manager = AgentPermissionManager()

# Contexto de un agente de IA
agent_context = {"user_id": "developer_001", "role": "developer"}

# Intentar leer un archivo (permiso sin aprobación)
result = perm_manager.check_permission("read_file", "read", agent_context)
print(f"Leer archivo: {result}")

# Intentar ejecutar un comando (requiere aprobación)
result = perm_manager.check_permission("execute_command", "execute", agent_context)
print(f"Ejecutar comando: {result}")

# Si se requiere aprobación, simular aprobación
if result.get('requires_approval'):
    approval_id = result.get('approval_id')
    approved = perm_manager.approve_action(approval_id)
    print(f"Aprobación: {'Concedida' if approved else 'Denegada'}")
