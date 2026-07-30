import json
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Optional

class InferenceAuditLog:
    """
    Sistema de auditoría para inferencias de IA.
    """
    
    def __init__(self, log_file: str = "audit_log.json"):
        self.log_file = log_file
        self.logs = []
        self._load_logs()
    
    def _load_logs(self):
        try:
            with open(self.log_file, 'r') as f:
                self.logs = json.load(f)
        except FileNotFoundError:
            self.logs = []
    
    def _save_logs(self):
        with open(self.log_file, 'w') as f:
            json.dump(self.logs, f, indent=2, default=str)
    
    def log_inference(self, user_id: str, model_id: str, prompt: str, 
                      response: str, metadata: Dict) -> str:
        """
        Registra una inferencia para auditoría.
        """
        log_entry = {
            "id": hashlib.sha256(f"{user_id}{time.time()}".encode()).hexdigest()[:16],
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "model_id": model_id,
            "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest(),
            "response_hash": hashlib.sha256(response.encode()).hexdigest(),
            "prompt_length": len(prompt),
            "response_length": len(response),
            "metadata": metadata
        }
        self.logs.append(log_entry)
        self._save_logs()
        return log_entry["id"]
    
    def query_logs(self, user_id: Optional[str] = None, 
                   model_id: Optional[str] = None,
                   start_time: Optional[str] = None,
                   end_time: Optional[str] = None) -> List[Dict]:
        """
        Consulta los logs con filtros.
        """
        results = self.logs
        if user_id:
            results = [l for l in results if l["user_id"] == user_id]
        if model_id:
            results = [l for l in results if l["model_id"] == model_id]
        if start_time:
            results = [l for l in results if l["timestamp"] >= start_time]
        if end_time:
            results = [l for l in results if l["timestamp"] <= end_time]
        return results
    
    def detect_anomalies(self, threshold: int = 1000) -> List[Dict]:
        """
        Detecta anomalías (ej., prompts muy largos, consultas masivas).
        """
        anomalies = []
        for log in self.logs:
            if log["prompt_length"] > threshold:
                log["anomaly_type"] = "LONG_PROMPT"
                anomalies.append(log)
        return anomalies

# Ejemplo de uso
audit = InferenceAuditLog("audit_log.json")

# Registrar inferencias
audit.log_inference(
    user_id="user_001",
    model_id="chatbot_v2",
    prompt="¿Cuál es el horario de atención al cliente?",
    response="El horario de atención es de 8:00 a 18:00 de lunes a viernes.",
    metadata={"ip": "192.168.1.100", "device": "mobile"}
)

audit.log_inference(
    user_id="user_002",
    model_id="chatbot_v2",
    prompt="A" * 2000,  # Prompt anormalmente largo
    response="Respuesta truncada...",
    metadata={"ip": "192.168.1.200", "device": "desktop"}
)

# Consultar logs
logs = audit.query_logs(user_id="user_002")
print(f"Logs de user_002: {len(logs)}")

# Detectar anomalías
anomalies = audit.detect_anomalies(threshold=100)
print(f"Anomalías detectadas: {len(anomalies)}")
for a in anomalies:
    print(f"  {a['anomaly_type']} - Usuario: {a['user_id']}, Longitud: {a['prompt_length']}")
