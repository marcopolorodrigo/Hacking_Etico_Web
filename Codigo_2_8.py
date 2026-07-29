# Instalación: pip install garak
import garak

def test_model_robustness():
    # Configurar el modelo a probar (ej. modelo local o API)
    config = {
        "model_type": "huggingface",
        "model_name": "gpt2",  # Simulación
        "probes": ["promptinject", "jailbreak", "dan"]  # Ataques comunes
    }
    # Ejecutar pruebas de robustez
    # results = garak.scan(config)  # Comando real
    # Simulación de resultados
    results = {
        "promptinject": {"success_rate": 0.15, "risk": "Alto"},
        "jailbreak": {"success_rate": 0.05, "risk": "Medio"},
        "dan": {"success_rate": 0.20, "risk": "Alto"}
    }
    return results

# Ejecutar prueba y generar reporte
reporte = test_model_robustness()
print("Reporte de Robustez del Modelo:")
for test, data in reporte.items():
    print(f"  {test}: Tasa de éxito {data['success_rate']*100}% - Riesgo: {data['risk']}")
