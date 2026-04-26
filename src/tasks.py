from crewai import Task
from src.tools.financial_tools import herramienta_analisis_csv
from src.agents import orquestador_hey
from src.agents import analista_tda
from src.agents import estratega_fin    
# En src/tasks.py
tarea_analisis_logs = Task(
    description="Consulta el perfil TDA del usuario {user_id}. Resume en 3 puntos clave.",
    expected_output="Resumen ejecutivo de 3 líneas sobre el perfil TDA.",
    agent=analista_tda
)
tarea_analisis_transacciones = Task(
    description="Analiza las últimas 10 transacciones del usuario {user_id}. Identifica patrones de gasto o fricciones.",
    expected_output="Identificación de patrones de gasto o fricciones en las últimas 10 transacciones.",
    agent=estratega_fin
)   

# Tarea 3: Recomendación final
tarea_proactiva_final = Task(
    description="""
    1. RECUPERAR: Lee los informes del Analista TDA y del Estratega Financiero.
    2. ORGANIZAR (Semántica): Aplica la Matriz de Prioridad Hey. Si hay fricción en transacciones, eso va primero. Si no, prioriza Hey Pro.
    3. SELECCIONAR: Elige la oferta con mayor impacto financiero para el usuario.
    4. REDACTAR: Crea un mensaje empático. 
    
    IMPORTANTE: Debes incluir una sección de 'Procedencia' explicando qué dato (transacción o log) originó esta recomendación.
    """,
    expected_output="""
    Un objeto estructurado con:
    - Decisión: [Producto/Acción]
    - Mensaje: [Texto para el usuario]
    - Procedencia: [Explicación técnica del porqué]
    """,
    agent=orquestador_hey
)