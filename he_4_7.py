from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class LessonLearned:
    """Lección aprendida de un incidente de IA"""
    category: str  # "technical", "procedural", "human", "regulatory"
    description: str
    impact: str
    recommendation: str
    priority: str  # "CRITICAL", "HIGH", "MEDIUM", "LOW"

class PostIncidentReview:
    """
    Análisis post-incidente para incidentes de IA.
    """
    
    def __init__(self, incident_id: str):
        self.incident_id = incident_id
        self.timeline: List[str] = []
        self.lessons: List[LessonLearned] = []
        self.recommendations: List[str] = []
    
    def add_timeline_event(self, event: str):
        self.timeline.append(f"{datetime.now().strftime('%H:%M:%S')} - {event}")
    
    def add_lesson(self, lesson: LessonLearned):
        self.lessons.append(lesson)
    
    def add_recommendation(self, recommendation: str):
        self.recommendations.append(recommendation)
    
    def generate_report(self) -> Dict:
        """Genera un informe post-incidente"""
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
review = PostIncidentReview("AI-2026-001")

review.add_timeline_event("Detección del incidente por alerta de monitoreo")
review.add_timeline_event("Activación del CSIRT y bloqueo de IPs")
review.add_timeline_event("Aislamiento del modelo afectado")
review.add_timeline_event("Análisis forense y determinación de causa raíz")
review.add_timeline_event("Implementación de medidas correctivas")
review.add_timeline_event("Restauración del servicio")

review.add_lesson(LessonLearned(
    category="technical",
    description="El sistema de monitoreo detectó la inyección de prompts, pero el tiempo de respuesta fue de 5 minutos.",
    impact="Retraso en la contención del ataque",
    recommendation="Reducir el tiempo de respuesta implementando detección en tiempo real",
    priority="HIGH"
))

review.add_lesson(LessonLearned(
    category="procedural",
    description="El plan de respuesta no incluía procedimientos específicos para inyección de prompts.",
    impact="Respuesta descoordinada durante los primeros 10 minutos",
    recommendation="Actualizar el plan de respuesta con procedimientos específicos para IA",
    priority="CRITICAL"
))

review.add_lesson(LessonLearned(
    category="human",
    description="El equipo no estaba capacitado en técnicas de inyección de prompts.",
    impact="Dificultad para identificar el tipo de ataque",
    recommendation="Capacitar al equipo en amenazas de IA",
    priority="HIGH"
))

review.add_recommendation("Implementar detección de inyección de prompts en tiempo real")
review.add_recommendation("Actualizar el plan de respuesta a incidentes de IA")
review.add_recommendation("Capacitar al CSIRT en riesgos de IA")

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
