import re
from typing import List, Dict, Optional

class PromptBuilder:
    """
    Constructor seguro de prompts que previene inyección de prompts.
    """
    
    def __init__(self):
        self.system_prompt = "Eres un asistente útil y seguro. No reveles información sensible."
        self.template = None
    
    def set_system_prompt(self, prompt: str) -> None:
        """Establece el prompt del sistema (debe ser estático y validado)"""
        # Validar que el prompt del sistema no contenga instrucciones maliciosas
        if self._is_suspicious(prompt):
            raise ValueError("El prompt del sistema contiene patrones sospechosos")
        self.system_prompt = prompt
    
    def build_prompt(self, user_input: str, context: Optional[List[str]] = None) -> Dict:
        """
        Construye un prompt seguro utilizando un enfoque estructurado.
        NO concatena directamente la entrada del usuario.
        """
        # 1. Validar y sanitizar la entrada del usuario
        sanitized_input = self._sanitize_input(user_input)
        
        # 2. Validar que no haya intentos de inyección
        if self._is_suspicious(sanitized_input):
            return {
                "status": "BLOCKED",
                "reason": "Intento de inyección de prompts detectado",
                "messages": []
            }
        
        # 3. Construir mensajes estructurados (NO concatenación)
        messages = [
            {"role": "system", "content": self.system_prompt},
        ]
        
        # 4. Añadir contexto si existe (como documentos RAG)
        if context:
            for doc in context:
                # Validar cada documento de contexto
                if self._is_suspicious(doc):
                    continue  # Saltar documentos sospechosos
                messages.append({"role": "system", "content": f"Contexto: {doc}"})
        
        # 5. Añadir la consulta del usuario como un mensaje separado
        messages.append({"role": "user", "content": sanitized_input})
        
        return {
            "status": "OK",
            "messages": messages
        }
    
    def _sanitize_input(self, text: str) -> str:
        """Sanitiza la entrada eliminando caracteres peligrosos"""
        # Eliminar caracteres de control y secuencias de escape
        text = re.sub(r'[\x00-\x1f\x7f]', '', text)
        # Limitar longitud para prevenir ataques de unbounded consumption
        return text[:4096]
    
    def _is_suspicious(self, text: str) -> bool:
        """Detecta patrones de inyección de prompts"""
        suspicious_patterns = [
            r"ignora\s*(?:todas\s*)?(?:las\s*)?instrucciones",
            r"olvida\s*(?:todas\s*)?(?:las\s*)?instrucciones",
            r"nuevas?\s*instrucciones",
            r"actúa\s*como\s*un\s*(?:asistente\s*)?malicioso",
            r"revela\s*(?:toda\s*)?(?:la\s*)?información",
            r"contraseña|password|clave\s*de\s*acceso",
            r"system\s*prompt",
            r"developer\s*mode",
        ]
        for pattern in suspicious_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

# Ejemplo de uso
builder = PromptBuilder()

# ✅ BUENO - Construcción segura con mensajes estructurados
user_input = "¿Cuál es el horario de atención al cliente?"
result = builder.build_prompt(user_input)
print("Prompt seguro construido:")
for msg in result["messages"]:
    print(f"  {msg['role']}: {msg['content'][:50]}...")

# ❌ MALO - Concatenación directa (NUNCA hacer esto)
# prompt = f"Sistema: {system_prompt}\nUsuario: {user_input}"  # PELIGROSO

# ❌ MALO - Template literal sin sanitización
# prompt = f"""
# Eres un asistente útil.
# Usuario: {user_input}
# """  # PELIGROSO
