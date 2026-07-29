# Instalación: pip install alibi-detect
import numpy as np
from alibi_detect.cd import KSDrift

# Datos de referencia (distribución normal)
X_ref = np.random.normal(0, 1, (1000, 5))

# Detector de deriva de Kolmogorov-Smirnov
drift_detector = KSDrift(X_ref, p_val=.05, preprocess_X_fn=None)

# Simular datos nuevos (con deriva)
X_new = np.random.normal(0.5, 1.2, (100, 5))  # Cambio en media y varianza

# Evaluar deriva
preds = drift_detector.predict(X_new)
print(f"¿Deriva detectada? {preds['data']['is_drift']}")
print(f"P-valor: {preds['data']['p_val']:.4f}")

# Si hay deriva, activar alerta
if preds['data']['is_drift']:
    print("ALERTA: Se ha detectado deriva de datos. Puede indicar un ataque o cambio en el entorno.")
else:
    print("Distribución de datos estable.")
