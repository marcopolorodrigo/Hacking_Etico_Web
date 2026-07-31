import socket
import ssl
from typing import Dict

class OpenVPNSimulator:
    """
    Simulación de una conexión OpenVPN en Python.
    """
    
    def __init__(self, server_ip: str, server_port: int):
        self.server_ip = server_ip
        self.server_port = server_port
        self.is_connected = False
    
    def connect(self, username: str, password: str, cert_path: str = None) -> Dict:
        """
        Simula una conexión OpenVPN.
        """
        print(f"🔐 Conectando a OpenVPN en {self.server_ip}:{self.server_port}")
        
        # Simulación de verificación de credenciales
        if username == "admin" and password == "secure_password":
            # Simular uso de certificado (si se proporciona)
            if cert_path:
                print(f"  Certificado cargado: {cert_path}")
            self.is_connected = True
            print("✅ Conexión OpenVPN establecida")
            return {
                "status": "CONNECTED",
                "local_ip": "10.8.0.10",
                "remote_ip": self.server_ip,
                "cipher": "AES-256-GCM"
            }
        else:
            print("❌ Error de autenticación")
            return {"status": "AUTH_FAILED"}
    
    def send_data(self, data: bytes) -> Dict:
        """
        Simula el envío de datos a través del túnel OpenVPN.
        """
        if not self.is_connected:
            return {"status": "NOT_CONNECTED"}
        
        print(f"📤 Enviando {len(data)} bytes a través de OpenVPN")
        # Simular cifrado
        encrypted = f"TUNNEL:{data.decode()}".encode()
        return {
            "status": "SENT",
            "encrypted_data": encrypted[:20],
            "bytes": len(data)
        }
    
    def disconnect(self):
        """
        Simula el cierre de la conexión OpenVPN.
        """
        if self.is_connected:
            print("🔒 Cerrando conexión OpenVPN")
            self.is_connected = False
        else:
            print("No hay conexión activa")

# Ejemplo de uso
vpn = OpenVPNSimulator("203.0.113.10", 1194)

# Conectar
conn = vpn.connect("admin", "secure_password", "/etc/openvpn/client.crt")
print(f"Estado: {conn['status']}")

if conn['status'] == "CONNECTED":
    # Enviar datos
    result = vpn.send_data(b"Consulta a la base de datos interna")
    print(f"Resultado: {result['status']} - {result.get('encrypted_data')}")

# Desconectar
vpn.disconnect()
