# Instalación: pip install alibi-detect
import numpy as np
from alibi_detect.cd import KSDrift

# Datos de entrenamiento (baseline)
X_ref = np.random.normal(0, 1, (1000, 10))  # 1000 muestras, 10 características

# Inicializar detector de deriva (Kolmogorov-Smirnov)
drift_detector = KSDrift(X_ref, p_val=.05, preprocess_X_fn=None)

# Simular nuevos datos (con deriva)
X_new = np.random.normal(0.5, 1, (100, 10))  # Media 0.5 en lugar de 0

# Evaluar deriva
preds = drift_detector.predict(X_new)
print(f"Deriva detectada: {preds['data']['is_drift']}")
print(f"P-valor: {preds['data']['p_val']:.4f}")
