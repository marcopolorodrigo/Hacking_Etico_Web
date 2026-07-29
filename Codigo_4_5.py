import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

# Simulación de un modelo objetivo (en realidad sería una API)
class TargetModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=10)
        X, y = make_classification(n_samples=1000, n_features=10, n_informative=5, random_state=42)
        self.model.fit(X, y)
    
    def predict(self, X):
        return self.model.predict_proba(X)

# Atacante: intenta robar el modelo mediante consultas
class ModelStealer:
    def __init__(self, target_api):
        self.target = target_api
        self.queries = []
        self.responses = []
    
    def steal(self, num_queries=100):
        # Generar consultas aleatorias en el espacio de entrada
        for _ in range(num_queries):
            query = np.random.rand(10)  # vector de 10 características
            prob = self.target.predict([query])
            self.queries.append(query)
            self.responses.append(prob[0])
        
        # Entrenar un modelo sustituto con las consultas-respuestas
        X = np.array(self.queries)
        y = np.argmax(self.responses, axis=1)  # clasificación simple
        surrogate = RandomForestClassifier(n_estimators=10)
        surrogate.fit(X, y)
        return surrogate
    
    def evaluate_similarity(self, surrogate, test_samples):
        # Evaluar la precisión del modelo robado frente al original
        original_preds = np.argmax(self.target.predict(test_samples), axis=1)
        surrogate_preds = surrogate.predict(test_samples)
        accuracy = np.mean(original_preds == surrogate_preds)
        return accuracy

# Simulación del ataque
target = TargetModel()
stealer = ModelStealer(target)
surrogate = stealer.steal(num_queries=200)

# Evaluar qué tan bien funciona el modelo robado
test_X, _ = make_classification(n_samples=100, n_features=10, n_informative=5, random_state=43)
accuracy = stealer.evaluate_similarity(surrogate, test_X)
print(f"Precisión del modelo robado: {accuracy*100:.2f}%")
