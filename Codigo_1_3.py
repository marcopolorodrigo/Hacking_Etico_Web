from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def clasificar_texto(texto):
    etiquetas = ["financiero", "salud", "personal", "código_fuente", "contrato"]
    resultado = classifier(texto, etiquetas)
    print(f"Texto clasificado como: {resultado['labels'][0]} (confianza: {resultado['scores'][0]:.2f})")
    return resultado
# Ejemplo
clasificar_texto("La clave de acceso al servidor es Admin2026")
# Salida esperada: "financiero" o "personal" con alta confianza
