from src.crew import equipo_hey_proactivo
import sys

# Forzar codificación UTF-8 para evitar que los Emojis crasheen el servidor en Windows
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def run_hey_agent(user_id: str):
    """
    Punto de entrada para el Agente Personalizable de Hey Banco.
    Inyecta el Estado Operacional inicial (user_id).
    """
    
    # 1. Definimos el Input (El usuario que queremos analizar del dataset)
    inputs = {
        'user_id': user_id 
    }

    print(f"\n{'='*50}")
    print(f"🤖 INICIANDO MOTOR DE INTELIGENCIA PROACTIVA HEY")
    print(f"Target: {inputs['user_id']}")
    print(f"{'='*50}\n")

    # 2. Ejecución del Kickoff
    try:
        resultado_final = equipo_hey_proactivo.kickoff(inputs=inputs)
        
        print(f"\n{'='*50}")
        print("✅ ANÁLISIS COMPLETADO EXITOSAMENTE")
        print(f"{'='*50}\n")
        return str(resultado_final)
        
    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")
        return f"Error: {e}"

if __name__ == "__main__":
    print(run_hey_agent('USR-00001'))

from openai import AzureOpenAI
import os

def chat_with_agent(user_id: str, message: str, history: list):
    """
    Función para continuar la conversación con el usuario usando el contexto.
    """
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY", "dummy"),  
        api_version=os.getenv("AZURE_OPENAI_VERSION", "2023-05-15"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "https://dummy.openai.azure.com/")
    )
    
    messages = [{"role": "system", "content": f"Eres Havi, el asistente financiero inteligente y empático de Hey Banco. Estás ayudando al usuario {user_id}. Responde de forma natural, amigable y usando formato markdown para resaltar cosas importantes."}]
    
    for msg in history:
        messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})
    
    messages.append({"role": "user", "content": message})
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error al conectar con la IA de chat: {str(e)}"
