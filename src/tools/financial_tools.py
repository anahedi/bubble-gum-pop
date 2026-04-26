import pandas as pd
from crewai.tools import tool

@tool("herramienta_analisis_csv")
def herramienta_analisis_csv(user_id: str):
    """Analiza el perfil TDA y financiero real del usuario."""
    try:
        # 1. Cargamos el archivo que subiste (Asegúrate que esté en data/)
        df = pd.read_csv('data/multi_mapper_profile_final.csv')
        
        # 2. NORMALIZACIÓN TOTAL: Quitamos espacios y pasamos a minúsculas
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # 3. Buscamos al usuario (Asegúrate de buscar 'USR-00001')
        user_id = str(user_id).strip()
        cliente_data = df[df['user_id'] == user_id]
        
        if cliente_data.empty:
            return f"Usuario {user_id} no encontrado en la base de datos TDA."
            
        res = cliente_data.iloc[0]
        
        # 4. Construimos el reporte real
        reporte = (
            f"DATOS REALES TDA PARA {user_id}:\n"
            f"- Perfil: {res['perfil_final_tda']}\n"
            f"- Tags detectados: {res['tags_personalidad']}\n"
            f"- Contexto: El usuario pertenece a los nodos {res['nodos_financieros']}"
        )
        return reporte
        
    except Exception as e:
        return f"Error crítico en Capa de Contexto: {str(e)}"
    
    