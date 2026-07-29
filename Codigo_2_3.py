# Instalación: pip install presidio-anonymizer presidio-analyzer
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# Inicializar motores
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def tokenize_sensitive_data(text):
    # Analizar el texto en busca de PII
    results = analyzer.analyze(text=text, language='es')
    
    # Configurar operadores: reemplazar por tokens sintéticos
    operators = {
        "PERSON": OperatorConfig("replace", {"new_value": "<REDACTADO>"}),
        "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "usuario@dominio.com"}),
        "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "555-000-0000"}),
        "CREDIT_CARD": OperatorConfig("replace", {"new_value": "****-****-****-1111"})
    }
    
    # Anonimizar el texto
    anonymized_result = anonymizer.anonymize(
        text=text,
        analyzer_results=results,
        operators=operators
    )
    return anonymized_result.text

# Ejemplo de log de aplicación
log_text = "Usuario: María Pérez, email: maria@banco.com, tarjeta: 4111-1111-1111-1111"
log_seguro = tokenize_sensitive_data(log_text)
print(f"Log original: {log_text}")
print(f"Log tokenizado: {log_seguro}")
