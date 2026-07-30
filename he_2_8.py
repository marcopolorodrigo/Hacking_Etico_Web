import shutil
import os
from datetime import datetime
from typing import List, Dict

class AIModelBackup:
    """
    Sistema de respaldo de modelos de IA.
    """
    
    def __init__(self, backup_dir: str):
        self.backup_dir = backup_dir
        self.backups = []
        os.makedirs(backup_dir, exist_ok=True)
    
    def create_backup(self, model_name: str, model_path: str, metadata: Dict) -> Dict:
        """Crea un respaldo de un modelo de IA"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{model_name}_{timestamp}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        os.makedirs(backup_path, exist_ok=True)
        
        # Copiar modelo
        shutil.copy2(model_path, os.path.join(backup_path, "model.pkl"))
        
        # Guardar metadatos
        metadata["backup_date"] = timestamp
        metadata["model_name"] = model_name
        metadata["backup_path"] = backup_path
        
        # Guardar metadatos en JSON (simulado)
        with open(os.path.join(backup_path, "metadata.txt"), 'w') as f:
            for key, value in metadata.items():
                f.write(f"{key}: {value}\n")
        
        backup_info = {
            "name": backup_name,
            "path": backup_path,
            "metadata": metadata,
            "created_at": timestamp
        }
        self.backups.append(backup_info)
        
        return backup_info
    
    def list_backups(self, model_name: str = None) -> List[Dict]:
        """Lista los respaldos disponibles"""
        if model_name:
            return [b for b in self.backups if b["metadata"]["model_name"] == model_name]
        return self.backups
    
    def restore_backup(self, backup_name: str, target_path: str) -> bool:
        """Restaura un respaldo a una ubicación específica"""
        for backup in self.backups:
            if backup["name"] == backup_name:
                source = os.path.join(backup["path"], "model.pkl")
                if os.path.exists(source):
                    shutil.copy2(source, target_path)
                    return True
        return False
    
    def cleanup_old_backups(self, keep_count: int = 5):
        """Elimina respaldos antiguos manteniendo solo los más recientes"""
        for model_name in set(b["metadata"]["model_name"] for b in self.backups):
            model_backups = [b for b in self.backups if b["metadata"]["model_name"] == model_name]
            model_backups.sort(key=lambda x: x["created_at"], reverse=True)
            
            for backup in model_backups[keep_count:]:
                if os.path.exists(backup["path"]):
                    shutil.rmtree(backup["path"])
                self.backups.remove(backup)

# Ejemplo de uso
backup_system = AIModelBackup("./model_backups")

# Crear respaldos
backup1 = backup_system.create_backup(
    "chatbot_v2", "./models/chatbot_v2.pkl",
    {"version": "2.0", "accuracy": "92.5%", "dataset": "customer_chat_2025"}
)
print(f"Respaldo creado: {backup1['name']}")

backup2 = backup_system.create_backup(
    "chatbot_v2", "./models/chatbot_v2.pkl",
    {"version": "2.1", "accuracy": "93.2%", "dataset": "customer_chat_2026"}
)
print(f"Respaldo creado: {backup2['name']}")

# Listar respaldos
backups = backup_system.list_backups("chatbot_v2")
print(f"\nRespaldos disponibles: {len(backups)}")
for b in backups:
    print(f"  {b['name']} - {b['metadata']['version']} ({b['created_at']})")
