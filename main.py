from src.crew import equipo_hey_proactivo

def run_hey_agent():
    """
    Punto de entrada para el Agente Personalizable de Hey Banco.
    Inyecta el Estado Operacional inicial (user_id).
    """
    
    # 1. Definimos el Input (El usuario que queremos analizar del dataset)
    # Puedes cambiarlo a USR-00001 o USR-00002 para probar los diferentes Mocks
    inputs = {
        'user_id': 'USR-00001' 
    }

    print(f"\n{'='*50}")
    print(f"🤖 INICIANDO MOTOR DE INTELIGENCIA PROACTIVA HEY")
    print(f"Target: {inputs['user_id']}")
    print(f"{'='*50}\n")

    # 2. Ejecución del Kickoff
    # Aquí el Orquestador toma el mando y delega tareas a los especialistas
    try:
        resultado_final = equipo_hey_proactivo.kickoff(inputs=inputs)
        
        print(f"\n{'='*50}")
        print("✅ ANÁLISIS COMPLETADO EXITOSAMENTE")
        print(f"{'='*50}\n")
        print(resultado_final)
        
    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")

if __name__ == "__main__":
    run_hey_agent()
