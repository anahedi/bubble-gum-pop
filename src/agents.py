from crewai import Agent, LLM
# IMPORTANTE: Esta es la línea que faltaba para corregir el NameError
from src.tools.financial_tools import herramienta_analisis_csv

# Configuración ligera para la MacBook Air M4 (Ollama)
local_llm = LLM(
    model="ollama/llama3.2:3b",
    base_url="http://localhost:11434"
)

# Agente Orquestador (El Manager)
orquestador_hey = Agent(
    role='Orquestador de Experiencia Hey',
    goal='Coordinar la visión financiera y el perfil del usuario para una oferta proactiva.',
    backstory='Líder en hospitalidad bancaria. Asegura que los mensajes sean empáticos y precisos.',
    llm=local_llm,
    max_iter=2, # Límite para evitar calor
    verbose=True
)

# Agente Analista (El que lee el CSV real)
analista_tda = Agent(
    role='Analista de Perfilamiento TDA',
    goal='Extraer UNICAMENTE la información del archivo CSV para el usuario.',
    backstory='Eres un experto en lectura de datos. Tu fuente de verdad es el CSV multi_mapper_profile_final.',
    tools=[herramienta_analisis_csv], # <--- Ahora ya está definida por el import de arriba
    allow_delegation=False,
    max_iter=2,
    llm=local_llm,
    verbose=True
)

# Agente Estratega (El de los números)
estratega_fin = Agent(
    role='Estratega de Crecimiento Financiero',
    goal='Identificar si el usuario califica para Hey Pro o Inversión.',
    backstory='Especialista en productos bancarios de Hey Banco.',
    llm=local_llm,
    max_iter=2,
    verbose=True
)