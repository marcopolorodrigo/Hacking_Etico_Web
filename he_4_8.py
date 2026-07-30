import json
from datetime import datetime
from typing import List, Dict, Optional

class IncidentReportGenerator:
    """
    Generador de informes de incidentes de IA.
    """
    
    def __init__(self, incident_data: Dict):
        self.data = incident_data
    
    def generate_full_report(self) -> str:
        """Genera un informe completo del incidente"""
        return f"""
        ================================================
        INFORME DE INCIDENTE DE IA
        ================================================
        
        IDENTIFICACIÓN
        --------------
        Incidente ID: {self.data.get('incident_id', 'N/A')}
        Título: {self.data.get('title', 'N/A')}
        Tipo: {self.data.get('incident_type', 'N/A')}
        Severidad: {self.data.get('severity', 'N/A')}
        Fecha de detección: {self.data.get('detection_time', 'N/A')}
        Estado: {self.data.get('status', 'N/A')}
        
        DESCRIPCIÓN
        -----------
        {self.data.get('description', 'N/A')}
        
        IMPACTO
        -------
        Sistemas afectados: {', '.join(self.data.get('affected_systems', []))}
        Usuarios afectados: {self.data.get('affected_users', 'No determinado')}
        Impacto técnico: {self.data.get('technical_impact', 'N/A')}
        Impacto en el negocio: {self.data.get('business_impact', 'N/A')}
        
        RESPUESTA
        ---------
        Medidas de contención: {self.data.get('containment', 'N/A')}
        Medidas de erradicación: {self.data.get('eradication', 'N/A')}
        Medidas de recuperación: {self.data.get('recovery', 'N/A')}
        
        LECCIONES APRENDIDAS
        --------------------
        {self.data.get('lessons_learned', 'N/A')}
        
        RECOMENDACIONES
        ---------------
        {self.data.get('recommendations', 'N/A')}
        
        CUMPLIMIENTO NORMATIVO
        ----------------------
        Notificación regulatoria: {'Sí' if self.data.get('regulatory_notification', False) else 'No'}
        Fecha de notificación: {self.data.get('regulatory_notification_date', 'N/A')}
        Autoridad: {self.data.get('regulatory_authority', 'N/A')}
        
        ================================================
        Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
    
    def export_json(self) -> str:
        """Exporta el informe como JSON para auditoría"""
        return json.dumps(self.data, indent=2, default=str)

# Ejemplo de uso
incident_data = {
    "incident_id": "AI-2026-001",
    "title": "Inyección de Prompts en Chatbot Bancario",
    "incident_type": "prompt_injection",
    "severity": "CRITICAL",
    "detection_time": "2026-07-21 14:35:00",
    "status": "RESUELTO",
    "description": "Se detectaron múltiples intentos de inyección de prompts en el chatbot de atención al cliente. Un intento exitoso expuso información de un cliente.",
    "affected_systems": ["Chatbot API", "Modelo LLM", "Base de datos de clientes"],
    "affected_users": 1,
    "technical_impact": "Exposición de datos de un cliente, degradación temporal del modelo",
    "business_impact": "Posible multa GDPR, pérdida de confianza",
    "containment": "Aislamiento del modelo afectado, bloqueo de IPs sospechosas",
    "eradication": "Implementación de filtros de entrada, actualización del modelo",
    "recovery": "Restauración del modelo desde backup, verificación de integridad",
    "lessons_learned": "Necesidad de detección en tiempo real de inyección de prompts",
    "recommendations": "Implementar filtros de entrada, capacitar al equipo en riesgos de IA",
    "regulatory_notification": True,
    "regulatory_notification_date": "2026-07-21 16:00:00",
    "regulatory_authority": "CNIL"
}

generator = IncidentReportGenerator(incident_data)
print(generator.generate_full_report())

# Exportar JSON
print("\n📄 EXPORTACIÓN JSON:")
print(generator.export_json())
