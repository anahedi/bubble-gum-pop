from crewai_tools import tool

@tool("tda_mapper_tool")
def tda_mapper_tool(user_id: str):
    """
    Simulación del Análisis Topológico de Datos (TDA) sobre logs de HAVI.
    Identifica clusters de comportamiento y sentimientos persistentes.
    """
    # RESPUESTAS GENÉRICAS PARA PRUEBAS (Escenarios posibles en Hey Banco)
    mock_responses = {
        "USR-00001": {
            "cluster": "Cazador de Beneficios (High Persistence)",
            "sentimiento": "Curiosidad Moderada",
            "insight_topologico": "El algoritmo Mapper detectó una conexión fuerte entre las consultas de 'cashback' y 'costos de membresía'. El usuario busca valor pero teme a las letras chiquitas.",
            "necesidad_implicita": "Deseo de optimizar gastos mediante beneficios de lealtad (Hey Pro)."
        },
        "USR-00002": {
            "cluster": "Usuario en Fricción Operativa",
            "sentimiento": "Frustración Alta",
            "insight_topologico": "Diagramas de persistencia muestran 'huecos' (H1) en el flujo de consulta de transferencias. El usuario se pierde en los pasos técnicos de la App.",
            "necesidad_implicita": "Asistencia proactiva en límites de transferencia y simplificación de UI."
        }
    }

    # Si el ID no está, devolvemos uno por defecto
    data = mock_responses.get(user_id, mock_responses["USR-00001"])
    
    return f"""
    --- REPORTE TDA (MOCK) ---
    CLUSTER: {data['cluster']}
    SENTIMIENTO: {data['sentimiento']}
    ANÁLISIS TDA: {data['insight_topologico']}
    CONCLUSIÓN: {data['necesidad_implicita']}
    """