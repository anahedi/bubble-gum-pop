from crewai import Task
from src.tools.financial_tools import herramienta_analisis_csv
from src.agents import orquestador_hey

# Tarea 1: Análisis de logs (Aquí entrará el TDA de tu compañera)
tarea_analisis_logs = Task(
    description="Analizar los logs de comportamiento del usuario {user_id} para detectar frustración.",
    expected_output="Un reporte de clusters de comportamiento y sentimiento BERT.",
    agent=None # El orquestador lo asignará
)

# Tarea 2: Análisis financiero
tarea_analisis_transacciones = Task(
    description="Revisar los CSVs de Hey Banco para el usuario {user_id}.",
    expected_output="Resumen de elegibilidad para Hey Pro y oportunidades de inversión.",
    agent=None,
    tools=[herramienta_analisis_csv]
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