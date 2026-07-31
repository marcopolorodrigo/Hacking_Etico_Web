from typing import Dict
import hashlib

class IPSecSimulator:
    """
    Simulación de IPsec en Python.
    """
    
    def __init__(self, local_ip: str, remote_ip: str):
        self.local_ip = local_ip
        self.remote_ip = remote_ip
        self.sa = None  # Security Association
        self.is_connected = False
    
    def ike_sa_init(self, pre_shared_key: str) -> Dict:
        """
        Simula la fase IKE (establecimiento de SA).
        """
        print(f"🔐 Iniciando IKE Phase 1 con {self.remote_ip}")
        
        # Simular intercambio de claves Diffie-Hellman
        self.sa = {
            "encryption": "AES-256-GCM",
            "hash": "SHA-256",
            "dh_group": "14",
            "key": hashlib.sha256(pre_shared_key.encode()).hexdigest()[:16]
        }
        print("✅ IKE Phase 1 completada")
        return self.sa
    
    def ipsec_sa_establish(self) -> Dict:
        """
        Simula la fase IKE Phase 2 (establecimiento de SA IPsec).
        """
        if not self.sa:
            return {"status": "ERROR", "message": "IKE Phase 1 no completada"}
        
        print("🔐 Iniciando IKE Phase 2 (IPsec SA)")
        self.is_connected = True
        print("✅ IPsec SA establecida")
        
        return {
            "status": "ESTABLISHED",
            "encryption": self.sa["encryption"],
            "spi": f"0x{hashlib.md5(f'{self.local_ip}-{self.remote_ip}'.encode()).hexdigest()[:8]}"
        }
    
    def send_encrypted(self, data: bytes) -> Dict:
        """
        Simula el envío de datos cifrados a través de IPsec.
        """
        if not self.is_connected:
            return {"status": "NOT_CONNECTED"}
        
        # Simular cifrado ESP
        encrypted = f"ESP:{data.decode()}".encode()
        return {
            "status": "SENT",
            "encrypted_data": encrypted[:20],
            "bytes": len(data)
        }
    
    def disconnect(self):
        """
        Simula el cierre de la conexión IPsec.
        """
        if self.is_connected:
            print("🔒 Cerrando conexión IPsec")
            self.is_connected = False
            self.sa = None
        else:
            print("No hay conexión activa")

# Ejemplo de uso
ipsec = IPSecSimulator("192.168.1.1", "10.0.0.1")

# Establecer conexión
ipsec.ike_sa_init("shared_secret_123")
ipsec.ipsec_sa_establish()

# Enviar datos
if ipsec.is_connected:
    result = ipsec.send_encrypted(b"Datos confidenciales entre sedes")
    print(f"Resultado: {result['status']} - {result.get('encrypted_data')}")

# Desconectar
ipsec.disconnect()
