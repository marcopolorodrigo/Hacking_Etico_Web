from typing import List, Dict, Optional
import re

class ContentFilter:
    """
    Simulación de filtrado de contenido (como SquidGuard) en Python.
    """
    
    def __init__(self):
        self.blocked_categories = {}
        self.custom_rules = []
        self.blocked_domains = []
        self.blocked_url_patterns = []
    
    def add_blocked_category(self, name: str, domains: List[str]):
        self.blocked_categories[name] = domains
    
    def add_custom_rule(self, pattern: str, action: str):
        self.custom_rules.append({"pattern": pattern, "action": action})
    
    def add_blocked_domain(self, domain: str):
        self.blocked_domains.append(domain)
    
    def add_blocked_url_pattern(self, pattern: str):
        self.blocked_url_patterns.append(pattern)
    
    def check_url(self, url: str) -> Dict:
        """
        Verifica si una URL debe ser bloqueada según las políticas.
        """
        # Verificar dominios bloqueados
        for domain in self.blocked_domains:
            if domain in url:
                return {"blocked": True, "reason": f"Dominio bloqueado: {domain}"}
        
        # Verificar patrones de URL
        for pattern in self.blocked_url_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                return {"blocked": True, "reason": f"Patrón bloqueado: {pattern}"}
        
        # Verificar reglas personalizadas
        for rule in self.custom_rules:
            if re.search(rule["pattern"], url, re.IGNORECASE):
                if rule["action"] == "block":
                    return {"blocked": True, "reason": f"Regla personalizada: {rule['pattern']}"}
        
        # Verificar categorías (solo si hay coincidencia con dominios)
        for category, domains in self.blocked_categories.items():
            for domain in domains:
                if domain in url:
                    return {"blocked": True, "reason": f"Categoría bloqueada: {category}"}
        
        return {"blocked": False, "reason": "Permitido"}
    
    def get_blocked_stats(self) -> Dict:
        """Obtiene estadísticas de bloqueo"""
        return {
            "blocked_categories": len(self.blocked_categories),
            "blocked_domains": len(self.blocked_domains),
            "blocked_patterns": len(self.blocked_url_patterns),
            "custom_rules": len(self.custom_rules)
        }

# Ejemplo de uso
filter = ContentFilter()

# Añadir categorías bloqueadas
filter.add_blocked_category("Redes Sociales", ["facebook.com", "twitter.com", "instagram.com"])
filter.add_blocked_category("Juegos", ["minijuegos.com", "poki.com"])

# Añadir dominios bloqueados
filter.add_blocked_domain("malware.com")
filter.add_blocked_domain("phishing.org")

# Añadir patrones de URL
filter.add_blocked_url_pattern(r"\.exe$")
filter.add_blocked_url_pattern(r"\.torrent$")

# Verificar URLs
urls = [
    "http://www.facebook.com",
    "http://www.ejemplo.com/index.html",
    "http://www.malware.com/descarga.exe",
    "http://www.minijuegos.com/juego",
    "http://www.phishing.org/login",
]

print("🚫 FILTRADO DE CONTENIDO")
for url in urls:
    result = filter.check_url(url)
    status = "🚫 BLOQUEADO" if result["blocked"] else "✅ PERMITIDO"
    print(f"{status}: {url} - {result['reason']}")

stats = filter.get_blocked_stats()
print(f"\n📊 ESTADÍSTICAS DE FILTRADO")
print(f"  Categorías bloqueadas: {stats['blocked_categories']}")
print(f"  Dominios bloqueados: {stats['blocked_domains']}")
print(f"  Patrones bloqueados: {stats['blocked_patterns']}")
