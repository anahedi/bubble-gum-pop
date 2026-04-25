from crewai import Agent, LLM

# Configuración del "Cerebro" para tu M4
# Usamos Llama 3.1 8B para un razonamiento superior
local_llm = LLM(
    model="ollama/llama3.1:8b",
    base_url="http://localhost:11434"
)

# --- DEFINICIÓN DE AGENTES ---

# 1. El Orquestador (El que fallaba en el import)
orquestador_hey = Agent(
    role='Gerente de Experiencia Personalizada Hey',
    goal='Unificar hallazgos de comportamiento y finanzas para una atención proactiva.',
    backstory='Experto en hospitalidad digital y diseño de servicios bancarios.',
    llm=local_llm,
    verbose=True
)

# 2. El Analista TDA
analista_tda = Agent(
    role='Analista de Comportamiento Topológico',
    goal='Identificar patrones no lineales en logs de interacción HAVI.',
    backstory='Matemático especializado en el análisis de formas y persistencia de datos.',
    llm=local_llm,
    verbose=True
)

# 3. El Estratega Financiero
estratega_fin = Agent(
    role='Estratega de Crecimiento Financiero',
    goal='Optimizar el uso de productos y detectar elegibilidad para beneficios como Hey Pro.',
    backstory='Consultor financiero enfocado en maximizar el valor del usuario.',
    llm=local_llm,
    verbose=True
)