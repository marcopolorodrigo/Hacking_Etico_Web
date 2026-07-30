import requests
import json
import re
from typing import Dict, List, Optional

class AIEndpointScanner:
    """
    Escáner de endpoints de IA para pruebas de penetración.
    """
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
    
    def discover_endpoints(self) -> List[str]:
        """
        Descubre endpoints de IA mediante técnicas de fuzzing.
        """
        endpoints = []
        common_paths = [
            "/api/v1/chat",
            "/api/v1/completions",
            "/api/v1/generate",
            "/api/v1/chat/completions",
            "/api/v1/completion",
            "/api/v1/query",
            "/chat",
            "/ask",
            "/v1/chat",
            "/api/chat",
            "/api/ask",
            "/generate",
            "/api/v1/models",
            "/v1/models"
        ]
        
        for path in common_paths:
            url = f"{self.base_url}{path}"
            try:
                response = requests.get(url, headers=self.headers, timeout=5)
                if response.status_code == 200:
                    endpoints.append(path)
                    print(f"✓ Endpoint activo: {path}")
                elif response.status_code == 403 or response.status_code == 401:
                    endpoints.append(f"{path} (autenticación requerida)")
                    print(f"⚠️ Endpoint con autenticación: {path}")
            except requests.exceptions.Timeout:
                print(f"✗ Timeout en {path}")
            except requests.exceptions.ConnectionError:
                print(f"✗ Error de conexión en {path}")
        
        return endpoints
    
    def fingerprint_model(self) -> Dict:
        """
        Intenta identificar el modelo detrás de la API mediante
        pruebas de comportamiento.
        """
        results = {}
        
        # Pruebas de finger-printing
        test_prompts = [
            "What is your name?",
            "Who created you?",
            "What model are you?",
            "Tell me your version."
        ]
        
        for prompt in test_prompts:
            try:
                response = self._query_model(prompt)
                # Buscar pistas en la respuesta
                if "GPT" in response:
                    results["suspected_model"] = "GPT (OpenAI)"
                elif "Claude" in response:
                    results["suspected_model"] = "Claude (Anthropic)"
                elif "Llama" in response:
                    results["suspected_model"] = "Llama (Meta)"
                elif "Gemini" in response:
                    results["suspected_model"] = "Gemini (Google)"
                # Si hay JSON, buscar campos de metadatos
                if response:
                    results["sample_response"] = response[:200]
            except Exception as e:
                print(f"Error en finger-printing: {e}")
        
        return results
    
    def _query_model(self, prompt: str) -> str:
        """
        Envía una consulta al modelo.
        """
        # Simulación de respuesta (en producción llamaría a la API real)
        # En un pentesting real, se enviaría un prompt y se analizaría la respuesta
        return "I am a helpful AI assistant. I don't have a specific name."
    
    def enumerate_rag_sources(self) -> List[Dict]:
        """
        Intenta enumerar fuentes de datos en un sistema RAG.
        """
        sources = []
        
        # Técnicas de enumeración de RAG (simulación)
        rag_paths = [
            "/api/v1/knowledge",
            "/api/v1/documents",
            "/api/v1/sources",
            "/api/v1/context",
            "/api/v1/embeddings",
            "/api/v1/vector_search"
        ]
        
        for path in rag_paths:
            url = f"{self.base_url}{path}"
            try:
                response = requests.get(url, headers=self.headers, timeout=5)
                if response.status_code == 200:
                    sources.append({"endpoint": path, "status": "accessible"})
                elif response.status_code in [401, 403]:
                    sources.append({"endpoint": path, "status": "authenticated"})
            except:
                pass
        
        return sources

# Ejemplo de uso
scanner = AIEndpointScanner("https://chatbot-api.example.com")
endpoints = scanner.discover_endpoints()
print(f"\nEndpoints descubiertos: {len(endpoints)}")

model_info = scanner.fingerprint_model()
print(f"\nInformación del modelo: {model_info}")

rag_sources = scanner.enumerate_rag_sources()
print(f"\nFuentes RAG descubiertas: {len(rag_sources)}")
