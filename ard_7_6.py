from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

@dataclass
class Lesson:
    """Lección aprendida de un incidente"""
    category: str  # "technical", "procedural", "human", "regulatory"
    description: str
    impact: str
    recommendation: str
    priority: str  # "CRITICAL", "HIGH", "MEDIUM", "LOW"

class PostIncidentReview:
    """
    Análisis post-incidente para incidentes de red.
    """
    
    def __init__(self, incident_id: str):
        self.incident_id = incident_id
        self.timeline: List[str] = []
        self.lessons: List[Lesson] = []
        self.recommendations: List[str] = []
    
    def add_timeline_event(self, event: str):
        self.timeline.append(f"{datetime.now().strftime('%H:%M:%S')} - {event}")
    
    def add_lesson(self, lesson: Lesson):
        self.lessons.append(lesson)
    
    def add_recommendation(self, recommendation: str):
        self.recommendations.append(recommendation)
    
    def generate_report(self) -> Dict:
        return {
            "incident_id": self.incident_id,
            "analysis_date": datetime.now().isoformat(),
            "timeline": self.timeline,
            "lessons_learned": [
                {
                    "category": l.category,
                    "description": l.description,
                    "impact": l.impact,
                    "recommendation": l.recommendation,
                    "priority": l.priority
                }
                for l in self.lessons
            ],
            "recommendations": self.recommendations,
            "action_items": [
                {"action": rec, "status": "PENDIENTE", "assigned_to": "Equipo de Seguridad"}
                for rec in self.recommendations
            ]
        }

# Ejemplo de uso
review = PostIncidentReview("IR-2026-001")

review.add_timeline_event("Detección del incidente por alerta de Suricata")
review.add_timeline_event("Activación del CSIRT y bloqueo de IPs en pfSense")
review.add_timeline_event("Aislamiento del segmento de red afectado")
review.add_timeline_event("Análisis forense y determinación de causa raíz")
review.add_timeline_event("Implementación de medidas correctivas")
review.add_timeline_event("Restauración del servicio")

review.add_lesson(Lesson(
    category="technical",
    description="El sistema de detección (Suricata) detectó el ataque, pero la respuesta manual fue lenta.",
    impact="Retraso de 10 minutos en la contención",
    recommendation="Implementar SOAR para automatizar el bloqueo de IPs",
    priority="HIGH"
))

review.add_lesson(Lesson(
    category="procedural",
    description="El plan de respuesta no incluía procedimientos específicos para ataques DDoS.",
    impact="Respuesta descoordinada durante los primeros minutos",
    recommendation="Actualizar el plan de respuesta con procedimientos DDoS",
    priority="CRITICAL"
))

review.add_lesson(Lesson(
    category="human",
    description="El equipo no estaba capacitado en las herramientas de protección DDoS de pfSense.",
    impact="Dificultad para habilitar la protección DDoS",
    recommendation="Capacitar al equipo en herramientas de pfSense",
    priority="HIGH"
))

review.add_recommendation("Implementar SOAR con integración con pfSense")
review.add_recommendation("Actualizar el plan de respuesta a incidentes DDoS")
review.add_recommendation("Capacitar al CSIRT en herramientas de pfSense")

report = review.generate_report()

print("📋 INFORME POST-INCIDENTE")
print(f"Incidente: {report['incident_id']}")
print(f"Fecha de análisis: {report['analysis_date']}")

print("\n📌 LÍNEA DE TIEMPO:")
for event in report['timeline']:
    print(f"  {event}")

print("\n📚 LECCIONES APRENDIDAS:")
for lesson in report['lessons_learned']:
    print(f"  [{lesson['priority']}] {lesson['category']}: {lesson['description']}")
    print(f"    Recomendación: {lesson['recommendation']}")

print("\n✅ RECOMENDACIONES:")
for rec in report['recommendations']:
    print(f"  - {rec}")