from crewai import Crew, Process
from src.agents import orquestador_hey, analista_tda, estratega_fin
from src.tasks import tarea_analisis_logs, tarea_analisis_transacciones, tarea_proactiva_final

# Configuramos la Crew con el Proceso Jerárquico (Recomendado por Gartner para sistemas complejos)
orquestador_hey = Crew(
    agents=[analista_tda, estratega_fin],
    tasks=[tarea_analisis_logs, tarea_analisis_transacciones, tarea_proactiva_final],
    manager_agent=orquestador_hey, # El orquestador central que maneja el estado [cite: 195]
    process=Process.hierarchical,
    verbose=True,
    memory=True # Memoria de corto y largo plazo para dar continuidad [cite: 109]
)

