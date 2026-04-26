import numpy as np
import pandas as pd
import umap
import hdbscan
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.stats import spearmanr
import warnings
import re
from sentence_transformers import SentenceTransformer

# Omitir warnings para tener una salida más limpia
warnings.filterwarnings('ignore')

def limpiar_texto(text):
    if not isinstance(text, str):
        return ""
    try:
        text = text.encode('cp1252').decode('utf-8')
    except:
        pass 
    text = re.sub(r'[^\w\s¿?¡!.,]', '', text)
    text = " ".join(text.split())
    return text

def load_data():
    """
    1. Carga de Datos:
    Carga los embeddings y el dataframe principal.
    Ajusta esta función según la ubicación real de tus datos o 
    pásalos como argumentos si ya están en memoria.
    """
    print("Cargando datos...")
    # Cargar embeddings
    embeddings = np.load("data/embeddings_hey_banco.npy")
    
    # Asumiendo que df_final está guardado como CSV o Parquet
    # Ajusta la ruta a tu entorno (ej. pd.read_parquet("data/df_final.parquet"))
    df_final = pd.read_csv("data/df_final.csv") 
    
    return embeddings, df_final

def get_top_keywords(df_cluster, text_column, n_terms=5):
    """Obtiene los n términos más frecuentes por cluster usando TF-IDF."""
    if len(df_cluster) == 0:
        return ""
    
    # Stop words en español dado el contexto de usuarios de banco mexicano
    spanish_stop_words = [
        'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 'para', 
        'con', 'no', 'una', 'su', 'al', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o', 'este', 
        'sí', 'porque', 'esta', 'entre', 'cuando', 'muy', 'sin', 'sobre', 'también', 'me', 'hasta', 
        'hay', 'donde', 'quien', 'desde', 'todo', 'nos', 'durante', 'todos', 'uno', 'les', 'ni', 
        'contra', 'otros', 'ese', 'eso', 'ante', 'ellos', 'e', 'esto', 'mí', 'antes', 'algunos', 
        'qué', 'unos', 'yo', 'otro', 'otras', 'otra', 'él', 'tanto', 'esa', 'estos', 'mucho', 'quienes', 
        'nada', 'muchos', 'cual', 'poco', 'ella', 'estar', 'estas', 'algunas', 'algo', 'nosotros', 
        'mi', 'mis', 'tú', 'te', 'ti', 'tu', 'tus', 'ellas', 'nosotras', 'vosotros', 'vosotras', 
        'os', 'mío', 'mía', 'míos', 'mías', 'tuyo', 'tuya', 'tuyos', 'tuyas', 'suyo', 'suya', 'suyos', 
        'suyas', 'nuestro', 'nuestra', 'nuestros', 'nuestras', 'vuestro', 'vuestra', 'vuestros', 'vuestras', 
        'esos', 'esas', 'estoy', 'estás', 'está', 'estamos', 'estáis', 'están', 'esté', 'estés', 'estemos', 
        'estéis', 'estén', 'estaré', 'estarás', 'estará', 'estaremos', 'estaréis', 'estarán', 'estaría', 
        'estarías', 'estaríamos', 'estaríais', 'estarían', 'estaba', 'estabas', 'estábamos', 'estabais', 
        'estaban', 'estuve', 'estuviste', 'estuvo', 'estuvimos', 'estuvisteis', 'estuvieron', 'estuviera', 
        'estuvieras', 'estuviéramos', 'estuvierais', 'estuvieran', 'estuviese', 'estuvieses', 'estuviésemos', 
        'estuvieseis', 'estuviesen', 'estando', 'estado', 'estada', 'estados', 'estadas', 'soy', 'eres', 
        'es', 'somos', 'sois', 'son', 'sea', 'seas', 'seamos', 'seáis', 'sean', 'seré', 'serás', 'será', 
        'seremos', 'seréis', 'serán', 'sería', 'serías', 'seríamos', 'seríais', 'serían', 'era', 'eras', 
        'éramos', 'erais', 'eran', 'fui', 'fuiste', 'fue', 'fuimos', 'fuisteis', 'fueron', 'fuera', 'fueras', 
        'fuéramos', 'fuerais', 'fueran', 'fuese', 'fueses', 'fuésemos', 'fueseis', 'fuesen', 'siendo', 'sido', 
        'tengo', 'tienes', 'tiene', 'tenemos', 'tenéis', 'tienen', 'tenga', 'tengas', 'tengamos', 'tengáis', 
        'tengan', 'tendré', 'tendrás', 'tendrá', 'tendremos', 'tendréis', 'tendrán', 'tendría', 'tendrías', 
        'tendríamos', 'tendríais', 'tendrían', 'tenía', 'tenías', 'teníamos', 'teníais', 'tenían', 'tuve', 
        'tuviste', 'tuvo', 'tuvimos', 'tuvisteis', 'tuvieron', 'tuviera', 'tuvieras', 'tuviéramos', 'tuvierais', 
        'tuvieran', 'tuviese', 'tuvieses', 'tuviésemos', 'tuvieseis', 'tuviesen', 'teniendo', 'tenido', 'tenida', 
        'tenidos', 'tenidas', 'tened', 'banco', 'hey', 'app', 'cuenta', 'tarjeta' # Stopwords de dominio
    ]
    
    vectorizer = TfidfVectorizer(stop_words=spanish_stop_words, max_features=1000)
    try:
        tfidf_matrix = vectorizer.fit_transform(df_cluster[text_column])
        feature_names = vectorizer.get_feature_names_out()
        
        # Sumar los scores TF-IDF de las palabras dentro del cluster
        tfidf_scores = tfidf_matrix.sum(axis=0).A1
        top_indices = tfidf_scores.argsort()[-n_terms:][::-1]
        top_terms = [feature_names[i] for i in top_indices]
        
        return ", ".join(top_terms).title()
    except ValueError:
        return "Desconocido"

def run_pipeline(embeddings, df_final):
    # Uso de StandardScaler si es necesario antes de UMAP
    # Los embeddings a veces pueden tener escalas ligeramente distintas, normalizarlos ayuda a UMAP
    print("Normalizando embeddings (StandardScaler)...")
    scaler = StandardScaler()
    embeddings_scaled = scaler.fit_transform(embeddings)
    
    # 2. Reducción de Dimensionalidad (UMAP 5D)
    print("Aplicando UMAP para reducir a 5 dimensiones...")
    umap_5d = umap.UMAP(n_neighbors=15, n_components=5, metric='cosine', random_state=42)
    embeddings_5d = umap_5d.fit_transform(embeddings_scaled)
    
    # 3. Clustering de Densidad (HDBSCAN)
    # min_cluster_size=50 asegura grupos de clientes significativos (~24k registros)
    print("Ejecutando HDBSCAN...")
    clusterer = hdbscan.HDBSCAN(min_cluster_size=150, metric='euclidean', core_dist_n_jobs=-1, prediction_data=True)
    df_final['cluster_id'] = clusterer.fit_predict(embeddings_5d)
    
    # 4. Visualización y Proyección (UMAP 2D)
    print("Reduciendo a 2D para visualización...")
    umap_2d = umap.UMAP(n_neighbors=15, n_components=2, metric='cosine', random_state=42)
    embeddings_2d = umap_2d.fit_transform(embeddings_scaled)
    
    df_final['umap_x'] = embeddings_2d[:, 0]
    df_final['umap_y'] = embeddings_2d[:, 1]
    
    # Formateo categórico para graficar. Los ruidos se marcan como "Ruido (-1)"
    df_final['cluster_label'] = df_final['cluster_id'].astype(str)
    df_final.loc[df_final['cluster_id'] == -1, 'cluster_label'] = 'Ruido (-1)'
    
    print("Generando scatter plot iteractivo con Plotly...")
    # render_mode='webgl' es crucial para optimizar el renderizado de ~24k puntos
    fig = px.scatter(
        df_final, 
        x='umap_x', 
        y='umap_y', 
        color='cluster_label',
        hover_data=['user_id', 'input_clean'],
        title='Hey Banco: Segmentación de Necesidades Implícitas',
        opacity=0.7,
        render_mode='webgl'
    )
    fig.write_html("clusters_visualization.html")
    print("[Exito] Visualizacion guardada en 'clusters_visualization.html'")
    
    # 5. Análisis de Correlación e Insights
    print("\nCalculando correlaciones y extrayendo insights (ignorando ruido)...")
    
    # Manejo de ruido: se filtra del análisis estadístico
    df_valid = df_final[df_final['cluster_id'] != -1].copy()
    
    variables_clave = ['ingresos', 'edad', 'monto_transaccion'] # Ajustar si tienen otros nombres
    unique_clusters = sorted(df_valid['cluster_id'].unique())
    
    print("\n" + "="*60)
    print("RESUMEN DE NECESIDADES IMPLÍCITAS (CLUSTERS)")
    print("="*60)
    
    cluster_labels_dict = {-1: 'Ruido'}
    
    for cluster in unique_clusters:
        df_cluster = df_valid[df_valid['cluster_id'] == cluster]
        
        # Etiquetado Automático (Top 5 términos con TF-IDF)
        cluster_label = get_top_keywords(df_cluster, 'input_clean', n_terms=5)
        cluster_labels_dict[cluster] = cluster_label
        
        print(f"\nCluster {cluster} | Etiqueta: [{cluster_label}] | Registros: {len(df_cluster)}")
        
        # Correlación de Spearman
        # Verificamos si pertenecer a este cluster se correlaciona con variables continuas
        df_valid['is_current_cluster'] = (df_valid['cluster_id'] == cluster).astype(int)
        
        for var in variables_clave:
            if var in df_valid.columns:
                corr, p_val = spearmanr(df_valid['is_current_cluster'], df_valid[var])
                
                if p_val < 0.05:
                    tendencia = "Positiva" if corr > 0 else "Negativa"
                    print(f"  -> Correlación {tendencia} con '{var}' (Spearman: {corr:.3f}, p-val: {p_val:.3e})")

    df_final['cluster_label_text'] = df_final['cluster_id'].map(cluster_labels_dict)
    return df_final, scaler, umap_5d, clusterer

def predict_new_client(messages, scaler, umap_5d, clusterer, df_valid):
    print("\n" + "="*60)
    print("PROBANDO NUEVO CLIENTE")
    print("="*60)
    
    # 1. Limpieza de texto
    cleaned_messages = [limpiar_texto(m) for m in messages]
    
    # 2. Generar embeddings
    print("Generando embeddings para los nuevos mensajes...")
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    new_embeddings = model.encode(cleaned_messages, show_progress_bar=False)
    
    # 3. Normalizar
    new_embeddings_scaled = scaler.transform(new_embeddings)
    
    # 4. Reducir dimensionalidad con UMAP ya ajustado
    new_embeddings_5d = umap_5d.transform(new_embeddings_scaled)
    
    # 5. Predecir cluster con HDBSCAN
    labels, probabilities = hdbscan.approximate_predict(clusterer, new_embeddings_5d)
    
    for i, msg in enumerate(messages):
        cluster_id = labels[i]
        prob = probabilities[i]
        print(f"\nMensaje Original: {msg}")
        if cluster_id == -1:
            print(f"-> Predicción: Ruido (-1) (Probabilidad: {prob:.2f})")
        else:
            df_cluster = df_valid[df_valid['cluster_id'] == cluster_id]
            cluster_label = get_top_keywords(df_cluster, 'input_clean', n_terms=5)
            print(f"-> Predicción: Cluster {cluster_id} [{cluster_label}] (Probabilidad: {prob:.2f})")

if __name__ == "__main__":
    try:
        embeddings, df_final = load_data()
        df_final, scaler, umap_5d, clusterer = run_pipeline(embeddings, df_final)
        try:
            df_final.to_csv("df_final_clustered.csv", index=False)
            print("[Exito] Exportado df_final_clustered.csv con exito.")
        except PermissionError:
            print("[Error] Permiso denegado al escribir df_final_clustered.csv. Cierra el archivo e intenta nuevamente.")
        
        df_valid = df_final[df_final['cluster_id'] != -1].copy()
        
        # Nuevos mensajes de prueba
        nuevos_mensajes = [
            "Quiero cancelar mi tarjeta de crédito porque me cobran anualidad.",
            "¿Dónde puedo depositar a mi cuenta en efectivo? ¿Tienen cajeros cerca?",
            "Me aprobaron un crédito automotriz, ¿cuál es la tasa de interés?",
            "No puedo entrar a la aplicación, se queda cargando y me marca error de conexión.",
            "Hola, buenas tardes, disculpe una pregunta."
        ]
        predict_new_client(nuevos_mensajes, scaler, umap_5d, clusterer, df_valid)
        
    except FileNotFoundError as e:
        print(f"Error: No se encontró el archivo de datos. Asegúrate de ajustar las rutas en load_data(). ({e})")