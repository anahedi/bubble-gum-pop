from crewai import Crew, Process
# Importamos los agentes que definimos en agents.py
from src.agents import orquestador_hey, analista_tda, estratega_fin, local_llm
# Importamos las tareas que definiremos en tasks.py
from src.tasks import tarea_analisis_logs, tarea_analisis_transacciones, tarea_proactiva_final


# src/crew.py
equipo_hey_proactivo = Crew(
    agents=[analista_tda, estratega_fin],
    tasks=[tarea_analisis_logs, tarea_analisis_transacciones, tarea_proactiva_final],
    manager_agent=orquestador_hey,
    process=Process.hierarchical,
    verbose=True,
    memory=False, # <--- DESACTÍVALO por ahora para evitar el error 401
    manager_llm=local_llm # <--- FORZAMOS al manager a usar tu M4
)
