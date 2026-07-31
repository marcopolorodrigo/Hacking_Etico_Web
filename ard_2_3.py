import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from typing import List, Dict

class ZeroDayDetector:
    """
    Simulación de un detector de ataques de día cero usando ML.
    """
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.trained = False
        self.feature_names = ['bytes', 'packets', 'protocol', 'port', 'connections', 'duration']
    
    def train(self, X: np.ndarray, y: np.ndarray):
        """
        Entrena el modelo con datos etiquetados (normal vs ataque conocido).
        """
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        accuracy = accuracy_score(y_test, self.model.predict(X_test))
        self.trained = True
        return accuracy
    
    def detect(self, packet_features: np.ndarray) -> Dict:
        """
        Detecta si un paquete es un ataque (incluyendo día cero).
        """
        if not self.trained:
            return {"is_attack": False, "confidence": 0}
        
        # Predicción: 1 = ataque, 0 = normal
        prediction = self.model.predict([packet_features])[0]
        probabilities = self.model.predict_proba([packet_features])[0]
        confidence = max(probabilities)
        
        return {
            "is_attack": bool(prediction),
            "confidence": float(confidence),
            "probability": {
                "normal": float(probabilities[0]),
                "attack": float(probabilities[1])
            }
        }

# Ejemplo de uso
detector = ZeroDayDetector()

# Generar datos sintéticos para entrenamiento
np.random.seed(42)
n_samples = 1000
X_normal = np.random.randn(n_samples, 6)
X_attack = np.random.randn(n_samples // 10, 6) * 2 + 1  # Ataques con desviación
X = np.vstack([X_normal, X_attack])
y = np.array([0] * n_samples + [1] * (n_samples // 10))

accuracy = detector.train(X, y)
print(f"Precisión del modelo: {accuracy:.2f}")

# Simular un ataque desconocido (día cero)
zero_day_attack = np.random.randn(1, 6) * 3 + 2  # Diferente a los datos de entrenamiento
result = detector.detect(zero_day_attack[0])
print(f"\nAtaque de día cero detectado: {result['is_attack']}")
print(f"Confianza: {result['confidence']:.2f}")
