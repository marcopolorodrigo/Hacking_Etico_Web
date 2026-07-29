# Instalación: pip install diffprivlib
from diffprivlib import mechanisms

# Mecanismo de Laplace para agregar ruido a una consulta de suma
dp_mechanism = mechanisms.Laplace(epsilon=1.0, sensitivity=1.0)
valor_real = 100
valor_anonimo = dp_mechanism.randomise(valor_real)
print(f"Valor real: {valor_real}, Valor con ruido DP: {valor_anonimo}")
