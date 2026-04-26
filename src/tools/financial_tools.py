import pandas as pd
from crewai.tools import tool

@tool("herramienta_analisis_csv")
def herramienta_analisis_csv(user_id: str):
    """
    Analiza el historial transaccional real usando 'tipo_operacion' y 'monto'.
    Detecta patrones de gasto en comercios y categorías MCC.
    """
    try:
        df_tx = pd.read_csv('data/hey_transacciones.csv')
        
        # 1. Normalizamos por si acaso (quita espacios)
        df_tx.columns = df_tx.columns.str.strip()
        
        user_id = str(user_id).strip()
        user_tx = df_tx[df_tx['user_id'] == user_id]
        
        if user_tx.empty:
            return f"No hay transacciones para {user_id}."

        # 2. Ajustamos la lógica de balance con tus columnas reales
        # Nota: He puesto 'compra' y 'deposito' como ejemplo, 
        # pero el código ahora es más flexible.
        total_egresos = user_tx[user_tx['tipo_operacion'].str.contains('compra|cargo|egreso', case=False, na=False)]['monto'].sum()
        total_ingresos = user_tx[user_tx['tipo_operacion'].str.contains('deposito|abono|ingreso', case=False, na=False)]['monto'].sum()
        balance_neto = total_ingresos - total_egresos
        
        # 3. Extraemos contexto de valor (Comercios y Categorías)
        # Esto le sirve al Orquestador para saber en QUÉ gasta
        top_comercios = user_tx['comercio_nombre'].value_counts().head(3).index.tolist()
        
        # 4. Últimos movimientos
        ultimas_tx = user_tx.tail(5)[['fecha_hora', 'comercio_nombre', 'monto', 'tipo_operacion']].to_string(index=False)
        
        return (
            f"--- AUDITORÍA FINANCIERA REAL ({user_id}) ---\n"
            f"Flujo Mensual Neto: ${balance_neto:,.2f}\n"
            f"Ingresos: ${total_ingresos:,.2f} | Egresos: ${total_egresos:,.2f}\n\n"
            f"COMERCIOS FRECUENTES: {', '.join(top_comercios)}\n\n"
            f"ÚLTIMOS 5 MOVIMIENTOS:\n{ultimas_tx}\n"
            f"--------------------------------------------"
        )
        
    except Exception as e:
        return f"Error en lectura de transacciones: {str(e)}"