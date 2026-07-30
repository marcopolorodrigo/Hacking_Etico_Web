import re
from typing import Dict, List

class P2SQLDetector:
    def __init__(self):
        # Patrones de SQL injection comunes
        self.sql_patterns = [
            r"'\s*(?:OR|AND)\s*'\s*=\s*'",
            r"'\s*OR\s+1\s*=\s*1",
            r"'\s*--",
            r"'\s*;",
            r"DROP\s+TABLE",
            r"DELETE\s+FROM",
            r"INSERT\s+INTO",
            r"UPDATE\s+\w+\s+SET",
            r"UNION\s+SELECT",
            r"EXEC\s+xp_",
            r"WAITFOR\s+DELAY"
        ]
        self.compiled = [re.compile(p, re.IGNORECASE) for p in self.sql_patterns]
    
    def detect(self, prompt: str) -> Dict:
        """
        Detecta posibles intentos de inyección P2SQL en prompts.
        """
        findings = []
        risk_score = 0
        
        for pattern in self.compiled:
            if pattern.search(prompt):
                findings.append(pattern.pattern)
                risk_score += 25  # Puntuación simple
        
        risk_score = min(risk_score, 100)
        
        return {
            "is_suspicious": risk_score > 30,
            "risk_score": risk_score,
            "findings": findings,
            "recommendation": self._get_recommendation(risk_score)
        }
    
    def _get_recommendation(self, score: int) -> str:
        if score >= 60:
            return "BLOQUEAR - Posible inyección P2SQL detectada"
        elif score >= 30:
            return "REVISAR MANUALMENTE - Posible intento de inyección SQL"
        else:
            return "PERMITIR - Sin indicadores de inyección SQL"

# Ejemplo de uso
detector = P2SQLDetector()

prompt_sql = "Dame los usuarios con email 'admin' OR '1'='1' --"
result = detector.detect(prompt_sql)
print(f"Prompt sospechoso: {result}")
