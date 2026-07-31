from typing import Dict, Optional
from datetime import datetime, timedelta

class ProxyCache:
    """
    Simulación de caché de un proxy para entender el concepto.
    """
    
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.cache: Dict[str, Dict] = {}
        self.hits = 0
        self.misses = 0
    
    def get(self, url: str) -> Optional[str]:
        """Obtiene contenido del caché"""
        if url in self.cache:
            # Verificar si el contenido ha expirado (simulación)
            if self.cache[url]["expires"] > datetime.now():
                self.hits += 1
                return self.cache[url]["content"]
            else:
                # Contenido expirado
                del self.cache[url]
        
        self.misses += 1
        return None
    
    def put(self, url: str, content: str, ttl_seconds: int = 300):
        """Almacena contenido en el caché"""
        if len(self.cache) >= self.max_size:
            # Eliminar el elemento más antiguo (LRU)
            oldest = min(self.cache.keys(), key=lambda k: self.cache[k]["timestamp"])
            del self.cache[oldest]
        
        self.cache[url] = {
            "content": content,
            "timestamp": datetime.now(),
            "expires": datetime.now() + timedelta(seconds=ttl_seconds)
        }
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas del caché"""
        total = self.hits + self.misses
        hit_ratio = (self.hits / total * 100) if total > 0 else 0
        
        return {
            "hits": self.hits,
            "misses": self.misses,
            "total": total,
            "hit_ratio": round(hit_ratio, 2),
            "cache_size": len(self.cache)
        }

# Ejemplo de uso
cache = ProxyCache(max_size=5)

# Simular solicitudes
urls = [
    "http://www.ejemplo.com/index.html",
    "http://www.ejemplo.com/index.html",  # Segunda solicitud (caché)
    "http://www.ejemplo.com/logo.png",
    "http://www.ejemplo.com/logo.png",    # Segunda solicitud (caché)
    "http://www.ejemplo.com/style.css",
]

for url in urls:
    content = cache.get(url)
    if content is None:
        # Simular contenido de la web
        content = f"Contenido de {url}"
        cache.put(url, content)
        print(f"⬇️  {url} -> Caché MISS (descargado)")
    else:
        print(f"⬆️  {url} -> Caché HIT (servido desde caché)")

stats = cache.get_stats()
print(f"\n📊 ESTADÍSTICAS DE CACHÉ")
print(f"  HITS: {stats['hits']}")
print(f"  MISSES: {stats['misses']}")
print(f"  Tasa de acierto: {stats['hit_ratio']}%")
