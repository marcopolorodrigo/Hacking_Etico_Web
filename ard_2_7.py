from typing import Dict
import re

class IDSEvasionSimulator:
    """
    Simulación de técnicas de evasión de IDS/IPS.
    """
    
    def __init__(self):
        self.techniques = {
            "fragmentation": self._fragment_packet,
            "encoding": self._encode_payload,
            "obfuscation": self._obfuscate_payload,
            "split_attack": self._split_attack
        }
    
    def _fragment_packet(self, payload: str, size: int = 10) -> list:
        """Fragmenta un payload en partes más pequeñas"""
        return [payload[i:i+size] for i in range(0, len(payload), size)]
    
    def _encode_payload(self, payload: str) -> str:
        """Codifica el payload (URL encoding)"""
        return ''.join(f'%{ord(c):02x}' for c in payload)
    
    def _obfuscate_payload(self, payload: str) -> str:
        """Ofusca el payload usando casos mixtos"""
        return ''.join(c.lower() if i % 2 == 0 else c.upper() for i, c in enumerate(payload))
    
    def _split_attack(self, payload: str) -> tuple:
        """Divide un ataque en dos partes (parte 1 y parte 2)"""
        mid = len(payload) // 2
        return payload[:mid], payload[mid:]
    
    def simulate_evasion(self, payload: str, technique: str) -> Dict:
        """
        Simula una técnica de evasión en un payload.
        """
        result = {
            "original": payload,
            "technique": technique
        }
        
        if technique in self.techniques:
            result["evaded"] = self.techniques[technique](payload)
        else:
            result["evaded"] = payload
        
        return result

# Ejemplo de uso
evader = IDSEvasionSimulator()

payload = "SELECT * FROM users WHERE id=1 OR 1=1"

print("🔍 TÉCNICAS DE EVASIÓN DE IDS/IPS")
for technique in evader.techniques.keys():
    result = evader.simulate_evasion(payload, technique)
    print(f"\nTécnica: {technique}")
    print(f"Original: {result['original'][:50]}...")
    print(f"Evadido: {result['evaded'][:50]}...")
