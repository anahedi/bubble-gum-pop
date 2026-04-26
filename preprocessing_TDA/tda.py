import pandas as pd
from crewai_tools import BaseTool
from pydantic import Field
import os

# Configuramos la herramienta siguiendo la estructura de CrewAI
class TDAUserProfileTool(BaseTool):
    name: str = "tda_user_profiler"
    description: str = (
        "Consulta el motor de Análisis Topológico de Datos (TDA) para obtener "
        "el arquetipo conductual de un usuario. Devuelve etiquetas de 'Alta Definición' "
        "basadas en patrones financieros y conversacionales ocultos."
    )
    
    # Definimos el input esperado para que el Orquestador sepa qué enviar
    user_id: str = Field(..., description="El ID único del cliente (ej. USR-00005)")

    def _run(self, user_id: str) -> str:
        # 1. Verificación de existencia del archivo de perfiles
        file_path = "multi_mapper_profile_final.csv"
        if not os.path.exists(file_path):
            return "Error: El Meta-Dataset TDA no ha sido generado. Favor de ejecutar el pipeline de TDA primero."

        try:
            # 2. Carga de datos (Capa de Estado Operacional)
            df = pd.read_csv(file_path)
            df.set_index('user_id', inplace=True)

            if user_id not in df.index:
                return f"El usuario {user_id} no tiene un perfil TDA específico. Sugerencia: Tratar como Usuario General."

            # 3. Extracción de la Capa Semántica
            perfil_fin = df.loc[user_id, 'perfil_final_tda']
            nodos_f = df.loc[user_id, 'nodos_financieros']
            
            # 4. Construcción del Reporte de Procedencia (Provenance)
            # Esto le da al Orquestador la justificación del porqué del perfil
            reporte = (
                f"--- REPORTE SEMÁNTICO TDA ---\n"
                f"ID Usuario: {user_id}\n"
                f"Arquetipo Detectado: {perfil_fin}\n"
                f"Evidencia Topológica: Asignado a los nodos financieros {nodos_f}.\n"
                f"Insight: Este perfil sugiere una personalización basada en {perfil_fin.split(': ')[-1]}."
            )
            
            return reporte

        except Exception as e:
            return f"Error técnico al consultar la herramienta TDA: {str(e)}"