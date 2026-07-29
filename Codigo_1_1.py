import re

def detectar_con_regex(texto):
    patrones = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'tarjeta_credito': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',  # Formato 1234-5678-9012-3456
        'telefono': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    }
    resultados = {}
    for tipo, patron in patrones.items():
        encontrados = re.findall(patron, texto)
        if encontrados:
            resultados[tipo] = encontrados
    return resultados
# Ejemplo de uso
texto_ejemplo = "Contacto: juan@empresa.com, tarjeta: 4111-1111-1111-1111, tel: 555-123-4567"
print(detectar_con_regex(texto_ejemplo))
