import pandas as pd
from crewai.tools import tool

@tool("consultar_perfil_tda_real")
def consultar_perfil_tda_real(user_id: str):
    """
    Busca el perfil topológico del usuario en los resultados del Mapper.
    Devuelve tags de personalidad y perfil de especialista para personalización extrema.
    """
    try:
        # Cargamos el archivo que nos pasaste
        df = pd.read_csv('data/multi_mapper_profile_final.csv')
        
        # Limpieza por seguridad
        user_id = str(user_id).strip()
        
        # Extraemos la fila del usuario
        row = df[df['user_id'] == user_id].iloc[0]
        
        return {
            "nodos_financieros": row['nodos_financieros'],
            "tags": row['tags_personalidad'],
            "perfil_especialista": row['perfil_final_tda']
        }
    except Exception as e:
        return f"Usuario {user_id} en zona de datos generales (sin nodo específico)."