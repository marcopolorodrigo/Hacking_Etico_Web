import json
import hashlib
import time
from datetime import datetime

class AuditLog:
    def __init__(self):
        self.logs = []
    
    def log_inference(self, user_id, prompt, response, metadata):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest(),
            "response_hash": hashlib.sha256(response.encode()).hexdigest(),
            "metadata": metadata,
            "audit_id": hashlib.sha256(f"{user_id}{time.time()}".encode()).hexdigest()[:16]
        }
        self.logs.append(entry)
        return entry["audit_id"]

# Uso en un endpoint de API
audit = AuditLog()
user = "soporte@empresa.com"
prompt = "¿Cuál es el balance de la cuenta 1234?"
response = "No tengo acceso a información financiera específica."
metadata = {"model": "gpt-4o", "version": "2026-07", "latency": 120}

audit_id = audit.log_inference(user, prompt, response, metadata)
print(f"Auditoría registrada con ID: {audit_id}")
