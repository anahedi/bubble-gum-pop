from crewai import Agent, LLM

# Configuración del motor local para tu M4
local_llm = LLM(
    model="ollama/llama3.2:3b",
    base_url="http://localhost:11434"
)

# --- AGENTES ---

orquestador_hey = Agent(
    role='Orquestador de Experiencia Hey',
    goal='Unificar visión financiera y sentimiento para atención proactiva.',
    backstory='Líder en hospitalidad bancaria encargado de la toma de decisiones final.',
    llm=local_llm,
    max_iter=3, # Limitamos a 3 intentos para evitar sobrecalentamiento
    verbose=True
)

analista_tda = Agent(
    role='Analista de Comportamiento Topológico y Semántico',
    goal='Encontrar patrones en logs y sentimientos profundos con BERT.',
    backstory='Matemático que interpreta el estado anímico y patrones de uso del cliente.',
    llm=local_llm,
    verbose=True
)

estratega_fin = Agent(
    role='Estratega de Crecimiento Financiero',
    goal='Detectar oportunidades de ahorro e inversión en el portafolio del cliente.',
    backstory='Analista senior que utiliza datos transaccionales para sugerir mejoras.',
    llm=local_llm,
    verbose=True
)

# Esto asegura que los nombres sean exportables sin errores
__all__ = ['orquestador_hey', 'analista_tda', 'estratega_fin']