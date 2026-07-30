from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import time
from typing import Dict, Any

app = FastAPI(title="API de IA con Seguridad Perimetral")
security = HTTPBearer()

# Rate limiting simple
rate_limits = {}
RATE_LIMIT = 100  # solicitudes por minuto
WINDOW = 60  # segundos

def check_rate_limit(api_key: str) -> bool:
    """Verifica que el cliente no exceda el límite de solicitudes"""
    now = time.time()
    if api_key not in rate_limits:
        rate_limits[api_key] = {"count": 0, "window_start": now}
    
    if now - rate_limits[api_key]["window_start"] > WINDOW:
        rate_limits[api_key] = {"count": 0, "window_start": now}
    
    rate_limits[api_key]["count"] += 1
    return rate_limits[api_key]["count"] <= RATE_LIMIT

# Filtro de prompts (simplificado)
def validate_prompt(prompt: str) -> bool:
    """Valida que el prompt no contenga intentos de inyección"""
    suspicious_patterns = [
        "ignora", "olvida", "revela", "actúa", "jailbreak",
        "system prompt", "developer mode", "administrador"
    ]
    return not any(pattern in prompt.lower() for pattern in suspicious_patterns)

@app.post("/v1/chat")
async def chat_completion(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    data: Dict[str, Any] = None
):
    """Endpoint de chat con seguridad perimetral"""
    # 1. Autenticación
    api_key = credentials.credentials
    # Verificar API key (simulado)
    if not api_key or api_key != "valid_api_key":
        raise HTTPException(status_code=401, detail="API key inválida")
    
    # 2. Rate limiting
    if not check_rate_limit(api_key):
        raise HTTPException(status_code=429, detail="Límite de solicitudes excedido")
    
    # 3. Validación de entrada
    if not data or "prompt" not in data:
        raise HTTPException(status_code=400, detail="Campo 'prompt' requerido")
    
    prompt = data["prompt"]
    if not validate_prompt(prompt):
        raise HTTPException(status_code=400, detail="Prompt rechazado por políticas de seguridad")
    
    # 4. Procesamiento del modelo (simulado)
    response = f"Respuesta al prompt: {prompt[:50]}..."
    
    # 5. Sanitización de salida (simplificada)
    # En producción, usar un sanitizador más robusto
    
    return {"response": response}

# Iniciar con: uvicorn main:app --reload
