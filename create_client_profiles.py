import pandas as pd
import json

def generar_perfiles(df_path="df_final_clustered.csv", output_path="client_profiles.csv"):
    print(f"Cargando datos desde {df_path}...")
    try:
        df = pd.read_csv(df_path)
    except FileNotFoundError:
        print(f"[Error] No se encontró el archivo {df_path}. Ejecuta primero clustering_pipeline.py.")
        return

    # Convertir 'date' a datetime si existe
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    print("Calculando métricas por cliente...")

    # Función auxiliar para extraer el valor más frecuente
    def get_most_frequent(series, exclude=None):
        if exclude is not None:
            series = series[series != exclude]
        if series.empty:
            return "Desconocido/Ninguno"
        return series.value_counts().index[0]

    # Función auxiliar para contar clusters (en formato JSON string para fácil lectura/exportación)
    def get_cluster_frequencies(series):
        counts = series.value_counts().to_dict()
        return json.dumps(counts, ensure_ascii=False)

    # Agrupación y cálculo
    perfiles = []
    grupos = df.groupby('user_id')
    
    total_users = len(grupos)
    print(f"Se procesarán {total_users} clientes únicos.")

    # Usar apply() o diccionarios agregados. Lo haremos estructurado para mantener control total
    agg_funcs = {
        'total_interacciones': ('user_id', 'count'),
        'necesidad_principal': ('cluster_label_text', lambda x: get_most_frequent(x, exclude='Ruido')),
        'canal_preferido': ('channel_source', lambda x: get_most_frequent(x) if 'channel_source' in df.columns else "N/A"),
        'ratio_ruido': ('cluster_id', lambda x: (x == -1).sum() / len(x)),
        'clusters_frecuentes': ('cluster_label_text', get_cluster_frequencies)
    }

    if 'date' in df.columns:
        agg_funcs['primera_interaccion'] = ('date', 'min')
        agg_funcs['ultima_interaccion'] = ('date', 'max')

    # Ejecutar la agregación
    df_profiles = df.groupby('user_id').agg(**agg_funcs).reset_index()

    # Formateo de las salidas
    df_profiles['ratio_ruido'] = (df_profiles['ratio_ruido'] * 100).round(2).astype(str) + "%"
    
    # Manejar fechas para que no se exporten como timestamps crudos
    if 'date' in df.columns:
        df_profiles['primera_interaccion'] = df_profiles['primera_interaccion'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df_profiles['ultima_interaccion'] = df_profiles['ultima_interaccion'].dt.strftime('%Y-%m-%d %H:%M:%S')

    print(f"Exportando base de perfiles a {output_path}...")
    try:
        df_profiles.to_csv(output_path, index=False, encoding='utf-8')
        print(f"[Exito] Se generaron los perfiles para {len(df_profiles)} clientes y se guardaron en {output_path}.")
        
        # Muestra rápida
        print("\n--- MUESTRA DE PERFILES ---")
        print(df_profiles.head(5).to_string())
        df_profiles.to_csv("df_profiles.csv", index=False, encoding='utf-8')
        print("---------------------------\n")
    except PermissionError:
        print(f"[Error] Permiso denegado al escribir {output_path}. Cierra el archivo e intenta nuevamente.")

if __name__ == "__main__":
    generar_perfiles()
