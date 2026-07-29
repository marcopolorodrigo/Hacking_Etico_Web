import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

class PatchPrioritizer:
    def __init__(self):
        # Modelo de ML para predecir la criticidad de un parche
        self.model = RandomForestRegressor(n_estimators=50)
        self._train_synthetic_model()
    
    def _train_synthetic_model(self):
        # Datos sintéticos para entrenamiento (en producción se usarían datos reales)
        X = np.random.rand(100, 4)  # CVSS_score, EPSS_score, age_days, #affected_systems
        y = np.random.rand(100) * 10  # Criticidad (0-10)
        self.model.fit(X, y)
    
    def prioritize(self, vulnerabilities):
        """
        vulnerabilities: lista de diccionarios con CVSS, EPSS, días desde disclosura, sistemas afectados
        """
        df = pd.DataFrame(vulnerabilities)
        features = df[['cvss_score', 'epss_score', 'age_days', 'affected_systems']]
        df['priority_score'] = self.model.predict(features)
        df['action'] = df['priority_score'].apply(
            lambda x: 'PARCHE INMEDIATO' if x >= 8 else 'PARCHE PROGRAMADO' if x >= 5 else 'MONITOREAR'
        )
        return df.sort_values('priority_score', ascending=False)

# Ejemplo de vulnerabilidades
vulns = [
    {"id": "CVE-2026-1234", "cvss_score": 9.8, "epss_score": 0.95, "age_days": 10, "affected_systems": 50},
    {"id": "CVE-2026-5678", "cvss_score": 7.5, "epss_score": 0.3, "age_days": 60, "affected_systems": 3},
    {"id": "CVE-2026-9012", "cvss_score": 4.3, "epss_score": 0.1, "age_days": 120, "affected_systems": 1}
]

prioritizer = PatchPrioritizer()
priorities = prioritizer.prioritize(vulns)
print(priorities[['id', 'cvss_score', 'epss_score', 'priority_score', 'action']])
