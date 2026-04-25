import pandas as pd
import numpy as np

def analizador_transaccional_hey(user_id_target):
    """
    Realiza una auditoría financiera profunda cruzando los tres datasets principales.
    """
    # 1. Carga de Datasets 
    try:
        df_clientes = pd.read_csv('data/hey_clientes.csv')
        df_productos = pd.read_csv('data/hey_productos.csv')
        df_transacciones = pd.read_csv('data/hey_transacciones.csv')
    except FileNotFoundError:
        return "Error: No se encontraron los archivos CSV del dataset."

    # 2. Filtrado por Usuario 
    cliente = df_clientes[df_clientes['user_id'] == user_id_target].iloc[0]
    productos_user = df_productos[df_productos['user_id'] == user_id_target]
    transacciones_user = df_transacciones[df_transacciones['user_id'] == user_id_target]

    insights = []

    #Lógica 1: Verificación de Estatus Hey Pro  
    #criterio: 6 compras completadas > $100 MXN al mes
    compras_validas = transacciones_user[
        (transacciones_user['tipo_operacion'] == 'compra') & 
        (transacciones_user['estatus'] == 'completada') & 
        (transacciones_user['monto'] > 100)
    ]
    
    conteo_compras = len(compras_validas)
    es_pro_actual = cliente['es_hey_pro']

    if conteo_compras >= 6 and not es_pro_actual:
        cashback_perdido = compras_validas['monto'].sum() * 0.01 
        insights.append(f"CRÍTICO: Usuario elegible para Hey Pro ({conteo_compras} compras). Pierde ${cashback_perdido:.2f} de cashback mensual.")
    elif es_pro_actual:
        insights.append(f"ESTATUS: Usuario ya es Hey Pro. Beneficios activos.")

    #Lógica 2: Optimización de Activos (Inversión) 
    debito = productos_user[productos_user['tipo_producto'] == 'cuenta_debito']
    tiene_inversion = not productos_user[productos_user['tipo_producto'] == 'inversion_hey'].empty
    
    if not debito.empty:
        saldo_debito = debito['saldo_actual'].sum()
        if saldo_debito > (cliente['ingreso_mensual_mxn'] * 0.5) and not tiene_inversion:
            insights.append(f"OPORTUNIDAD: Saldo ocioso de ${saldo_debito:.2f}. Recomendado mover a Inversión Hey (GAT).")

    # Lógica 3: Análisis de Fricción (Transacciones Fallidas) 
    fallidas = transacciones_user[transacciones_user['estatus'] == 'no_procesada']
    if not fallidas.empty:
        motivo_frecuente = fallidas['motivos_no_procesada'].mode().iloc[0]
        insights.append(f"FRICCIÓN: {len(fallidas)} intentos fallidos. Motivo principal: {motivo_frecuente}.")

    #Lógica 4: Patrones de Gasto (Top Categorías) 
    top_mcc = transacciones_user.groupby('categoria_mcc')['monto'].sum().sort_values(ascending=False).head(2)
    insights.append(f"GASTOS: Sus mayores consumos son en {', '.join(top_mcc.index.tolist())}.")

    # Respuesta estructurada para el Agente Financiero
    return "\n".join(insights)

# Ejemplo de uso:
print(analizador_transaccional_hey('USR-00001'))