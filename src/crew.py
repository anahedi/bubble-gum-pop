from crewai import LLM, Crew, Process
from src.agents import orquestador_hey, analista_tda, estratega_fin
from src.tasks import tarea_analisis_logs, tarea_analisis_transacciones, tarea_proactiva_final
from src.agents import local_llm
# src/crew.py
equipo_hey_proactivo = Crew(
    agents=[analista_tda, estratega_fin],
    tasks=[tarea_analisis_logs, tarea_analisis_transacciones, tarea_proactiva_final],
    manager_agent=orquestador_hey,
    process=Process.sequential,
    verbose=True,
    memory=False, # <--- DESACTÍVALO por ahora para evitar el error 401
    manager_llm=local_llm # <--- FORZAMOS al manager a usar tu M4
)

