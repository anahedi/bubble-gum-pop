from src.crew import equipo_hey_proactivo

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
