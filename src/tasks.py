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
    4. VALIDACIÓN OBLIGATORIA (RAG): Es ESTRICTAMENTE NECESARIO que utilices la 'herramienta_web_hey' 
    para buscar los beneficios actuales del producto seleccionado en heybanco.com. 
    No des una respuesta basada en tus conocimientos generales; cita un beneficio real de la web.
    5. REDACTAR: Crea un mensaje empático. 
    
    IMPORTANTE: Debes dar la salida en formato JSON puro. No envuelvas el JSON en markdown.
    """,
    expected_output="""
    {
        "Decision": "El producto o tarjeta a ofrecer (Ej. Tarjeta Hey Pro)",
        "Mensaje": "Un párrafo empático explicando por qué le conviene este producto según su historial.",
        "Razon1_Titulo": "Motivo 1 corto (Ej. Cargos recurrentes)",
        "Razon1_Desc": "Explicación del motivo 1 basado en sus gastos.",
        "Razon2_Titulo": "Motivo 2 corto (Ej. Perfil digital global)",
        "Razon2_Desc": "Explicación del motivo 2 o beneficio clave extraído de la web."
    }
    """,
    agent=orquestador_hey
)
