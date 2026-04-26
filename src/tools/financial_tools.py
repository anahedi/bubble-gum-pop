import pandas as pd
from crewai.tools import tool

@tool("herramienta_analisis_csv")
def herramienta_analisis_csv(user_id: str):
    """
    Analiza los datasets de Hey Banco (clientes, productos y transacciones).
    Normaliza nombres de columnas y genera insights financieros.
    """
    # Limpieza de seguridad: Si el LLM manda basura, intentamos rescatar el ID
    if isinstance(user_id, dict):
        user_id = user_id.get('user_id', 'USR-00001')
    
    user_id = str(user_id).strip()
    try:
        # 1. Carga de datos con normalización de columnas (espacios -> guiones bajos)
        df_clientes = pd.read_csv('data/hey_clientes.csv')
        df_clientes.columns = df_clientes.columns.str.replace(' ', '_')

        df_productos = pd.read_csv('data/hey_productos.csv')
        df_productos.columns = df_productos.columns.str.replace(' ', '_')

        df_transacciones = pd.read_csv('data/hey_transacciones.csv')
        df_transacciones.columns = df_transacciones.columns.str.replace(' ', '_')

        # 2. Filtrado de información (Ahora 'user_id' es consistente en todos)
        cliente = df_clientes[df_clientes['user_id'] == user_id].iloc[0]
        productos = df_productos[df_productos['user_id'] == user_id]
        transacciones = df_transacciones[df_transacciones['user_id'] == user_id]

        resumen = []
        
        # --- Análisis Hey Pro ---
        # El diccionario define 'tipo_operacion' y 'estatus' 
        compras_mes = transacciones[
            (transacciones['tipo_operacion'] == 'compra') & 
            (transacciones['estatus'] == 'completada') & 
            (transacciones['monto'] >= 100)
        ]
        num_compras = len(compras_mes)
        
        if num_compras >= 6 and not cliente['es_hey_pro']:
            resumen.append(f"- ELEGIBILIDAD: El usuario tiene {num_compras} compras. ¡Candidato a Hey Pro!")
        
        # --- Análisis de Inversión ---
        # 'saldo_actual' ahora tiene guion bajo gracias a nuestra normalización
        saldo_debito = productos[productos['tipo_producto'] == 'cuenta_debito']['saldo_actual'].sum()
        tiene_inversion = not productos[productos['tipo_producto'] == 'inversion_hey'].empty
        
        if saldo_debito > (cliente['ingreso_mensual_mxn'] * 0.4) and not tiene_inversion:
            resumen.append(f"- OPORTUNIDAD: Tiene ${saldo_debito} ociosos en débito. Sugerir Inversión Hey.")

        # --- Análisis de Fricción ---
        fallidas = transacciones[transacciones['estatus'] == 'no_procesada']
        if not fallidas.empty:
            motivo = fallidas['motivos_no_procesada'].mode()[0]
            resumen.append(f"- ALERTA: {len(fallidas)} transacciones fallidas por {motivo}.")

        return "\n".join(resumen) if resumen else "Usuario estable, sin alertas inmediatas."

    except Exception as e:
        return f"Error procesando datos: {str(e)}"