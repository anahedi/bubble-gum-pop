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