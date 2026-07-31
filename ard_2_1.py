import numpy as np
from sklearn.ensemble import IsolationForest
from typing import List, Dict
from datetime import datetime

class HeuristicDetector:
    """
    Simulación de un detector basado en heurística para IDS/IPS.
    """
    
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.baseline_trained = False
        self.training_data = []
    
    def train_baseline(self, normal_traffic: List[Dict]):
        """
        Entrena el modelo con tráfico normal (baseline).
        """
        # Convertir datos de tráfico a vectores numéricos
        X = []
        for packet in normal_traffic:
            vector = [
                packet.get('bytes', 0),
                packet.get('packet_count', 0),
                packet.get('protocol_weight', 0),
                packet.get('port_frequency', 0)
            ]
            X.append(vector)
        
        self.model.fit(np.array(X))
        self.baseline_trained = True
        self.training_data = normal_traffic
    
    def detect_anomaly(self, packet: Dict) -> Dict:
        """
        Detecta si un paquete es una anomalía (posible ataque).
        """
        if not self.baseline_trained:
            return {"is_anomaly": False, "confidence": 0}
        
        vector = np.array([[
            packet.get('bytes', 0),
            packet.get('packet_count', 0),
            packet.get('protocol_weight', 0),
            packet.get('port_frequency', 0)
        ]])
        
        prediction = self.model.predict(vector)[0]  # -1 = anomalía, 1 = normal
        score = self.model.score_samples(vector)[0]
        confidence = 1 / (1 + np.exp(-score))
        
        return {
            "is_anomaly": (prediction == -1),
            "confidence": float(confidence),
            "score": float(score)
        }

# Ejemplo de uso
detector = HeuristicDetector()

# Simular tráfico normal de entrenamiento
normal_traffic = [
    {"bytes": 1500, "packet_count": 10, "protocol_weight": 0.5, "port_frequency": 0.8},
    {"bytes": 1200, "packet_count": 8, "protocol_weight": 0.4, "port_frequency": 0.7},
    {"bytes": 1800, "packet_count": 12, "protocol_weight": 0.6, "port_frequency": 0.9},
    {"bytes": 1000, "packet_count": 6, "protocol_weight": 0.3, "port_frequency": 0.6},
]
detector.train_baseline(normal_traffic)

# Probar con un paquete sospechoso
suspicious_packet = {"bytes": 10000, "packet_count": 100, "protocol_weight": 0.9, "port_frequency": 0.2}
result = detector.detect_anomaly(suspicious_packet)
print(f"Anomalía detectada: {result['is_anomaly']}")
print(f"Confianza: {result['confidence']:.2f}")
