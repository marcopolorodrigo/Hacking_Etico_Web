from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

@dataclass
class Lesson:
    """Lección aprendida de un incidente de IA"""
    category: str  # "technical", "procedural", "human", "regulatory"
    description: str
    recommendation: str
    priority: str  # "CRITICAL", "HIGH", "MEDIUM", "LOW"

class PostIncidentReview:
    """Análisis post-incidente para incidentes de IA"""
    
    def __init__(self, incident_id: str):
        self.incident_id = incident_id
        self.lessons: List[Lesson] = []
        self.recommendations: List[str] = []
    
    def add_lesson(self, lesson: Lesson):
        self.lessons.append(lesson)
    
    def generate_report(self) -> Dict:
        return {
            "incident_id": self.incident_id,
            "lessons_learned": [
                {"category": l.category, "description": l.description, 
                 "recommendation": l.recommendation, "priority": l.priority}
                for l in self.lessons
            ],
            "recommendations": self.recommendations
        }

# Ejemplo de uso
review = PostIncidentReview("AI-2026-001")
review.add_lesson(Lesson(
    category="technical",
    description="El sistema de monitoreo detectó la inyección de prompts, pero la respuesta fue lenta.",
    recommendation="Implementar SOAR para automatizar la respuesta",
    priority="HIGH"
))
report = review.generate_report()
print(report)
