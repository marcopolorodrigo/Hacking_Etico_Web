from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime, timedelta

@dataclass
class TrainingActivity:
    name: str
    category: str
    estimated_hours: int
    priority: int  # 1=alta, 2=media, 3=baja
    completed: bool = False

class TrainingPlan:
    """
    Plan de formación personalizado en hacking ético.
    """
    
    def __init__(self, user_level: str, goals: List[str]):
        self.user_level = user_level
        self.goals = goals
        self.activities: List[TrainingActivity] = []
        self._generate_plan()
    
    def _generate_plan(self):
        """Genera un plan de formación según el nivel y objetivos"""
        if self.user_level == "novato":
            self.activities.extend([
                TrainingActivity("Fundamentos de Networking (CCNA)", "Networking", 40, 1),
                TrainingActivity("Linux Basics", "Sistemas Operativos", 20, 1),
                TrainingActivity("CEH Training Course", "Certificación", 80, 1),
                TrainingActivity("Hack The Box - Starting Point", "Práctica", 20, 2)
            ])
        elif self.user_level == "intermedio":
            self.activities.extend([
                TrainingActivity("OSCP Preparation Course", "Certificación", 120, 1),
                TrainingActivity("TryHackMe - Red Team Path", "Práctica", 30, 1),
                TrainingActivity("Web Security Academy (PortSwigger)", "Aplicaciones Web", 60, 2),
                TrainingActivity("Python for Security", "Programación", 40, 2)
            ])
        elif self.user_level == "avanzado":
            self.activities.extend([
                TrainingActivity("OSWE Preparation", "Certificación", 120, 1),
                TrainingActivity("AI Red Teaming (EC-Council)", "Certificación", 80, 1),
                TrainingActivity("SANS SEC504 - Hacker Tools", "Formación", 40, 2),
                TrainingActivity("NIST AI RMF Implementation", "Formación", 30, 2),
                TrainingActivity("CVE Research and Exploit Development", "Investigación", 60, 1)
            ])
        
        # Actividades según objetivos
        if "IA" in self.goals or "AI" in self.goals:
            self.activities.append(TrainingActivity(
                "OWASP Top 10 for LLMs - Study", 
                "IA", 20, 1
            ))
            self.activities.append(TrainingActivity(
                "Garak - Practical LLM Scanning", 
                "IA", 15, 2
            ))
        
        if "web" in self.goals:
            self.activities.append(TrainingActivity(
                "Burp Suite Mastery", 
                "Aplicaciones Web", 30, 1
            ))
        
        # Ordenar por prioridad
        self.activities.sort(key=lambda x: (x.priority, -x.estimated_hours))
    
    def get_timeline(self) -> Dict:
        """Genera un cronograma de formación"""
        total_hours = sum(a.estimated_hours for a in self.activities if not a.completed)
        hours_per_day = 2  # 2 horas diarias
        days_needed = total_hours // hours_per_day
        
        timeline = {
            "total_hours": total_hours,
            "estimated_days": days_needed,
            "estimated_weeks": days_needed // 7,
            "activities": [
                {
                    "name": a.name,
                    "category": a.category,
                    "hours": a.estimated_hours,
                    "priority": a.priority,
                    "completed": a.completed
                }
                for a in self.activities
            ]
        }
        return timeline

# Ejemplo de uso
plan = TrainingPlan(
    user_level="intermedio",
    goals=["IA", "web", "certificación OSCP"]
)

timeline = plan.get_timeline()
print("📚 PLAN DE FORMACIÓN EN HACKING ÉTICO")
print(f"Total de horas estimadas: {timeline['total_hours']}")
print(f"Días estimados (2h/día): {timeline['estimated_days']}")
print("\nActividades:")
for a in timeline['activities']:
    status = "✅" if a['completed'] else "⬜"
    priority_label = "ALTA" if a['priority'] == 1 else "MEDIA" if a['priority'] == 2 else "BAJA"
    print(f"  {status} {a['name']} ({a['category']}) - {a['hours']}h - Prioridad: {priority_label}")
