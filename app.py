import openai
import os
import anthropic
import gradio as gr
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import tempfile

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
anthropic.api_key = os.getenv("ANTHROPIC_API_KEY")

clientElevenLabs = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
clientAnthropic = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Cliente para DeepSeek
clientDeepSeek = openai.OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# Contador global para rastrear caracteres usados en la sesión
character_usage = {"count": 0}

def add_character_usage(chars):
    """Añade caracteres al contador de uso"""
    character_usage["count"] += chars
    
    # Advertencias basadas en el límite de 10,000 caracteres/mes
    if character_usage["count"] > 8000:
        print(f"🚨 ALERTA: {character_usage['count']} caracteres usados - cerca del límite mensual!")
    elif character_usage["count"] > 5000:
        print(f"⚠️ ADVERTENCIA: {character_usage['count']} caracteres usados - más de la mitad del límite mensual")
    else:
        print(f"📊 Caracteres usados en esta sesión: {character_usage['count']}/10000 (límite mensual)")

def smart_truncate(text, max_length=300):
    """Trunca el texto de manera inteligente, respetando frases completas"""
    if len(text) <= max_length:
        return text
    
    # Intentar cortar en una oración completa (punto, exclamación, interrogación)
    sentence_endings = ['. ', '! ', '? ', '.\n', '!\n', '?\n']
    for ending in sentence_endings:
        pos = text.rfind(ending, 0, max_length)
        if pos > max_length * 0.6:  # Solo si el corte no es demasiado temprano
            return text[:pos + 1].strip()
    
    # Si no hay oraciones completas, cortar en coma o punto y coma
    clause_endings = [', ', '; ', ',\n', ';\n']
    for ending in clause_endings:
        pos = text.rfind(ending, 0, max_length)
        if pos > max_length * 0.6:
            return text[:pos + 1].strip()
    
    # Si no hay comas, cortar en un espacio (evitar cortar palabras)
    pos = text.rfind(' ', 0, max_length)
    if pos > max_length * 0.5:  # Solo si el corte no es demasiado temprano
        return text[:pos].strip() + "..."
    
    # Como último recurso, cortar directamente pero añadir puntos suspensivos
    return text[:max_length-3].strip() + "..."

def get_available_voices():
    """Obtiene los IDs reales de las voces disponibles"""
    try:
        voices = clientElevenLabs.voices.get_all()
        voice_map = {}
        for voice in voices.voices:
            voice_map[voice.name] = voice.voice_id
        return voice_map
    except:
        return {}

def test_elevenlabs_connection():
    """Prueba la conexión con ElevenLabs"""
    try:
        if not os.getenv("ELEVENLABS_API_KEY"):
            return "❌ ElevenLabs API key no configurada"
        
        # Intentar obtener las voces disponibles
        voices = clientElevenLabs.voices.get_all()
        
        # Mostrar algunas voces disponibles con sus IDs
        voice_info = []
        for voice in voices.voices[:8]:  # Mostrar más voces
            voice_info.append(f"{voice.name} ({voice.voice_id[:8]}...)")
        
        # Buscar voces específicas que usamos y obtener sus IDs reales
        target_voices = ["Aria", "Sarah", "Laura"]
        used_voices = {}
        for voice in voices.voices:
            if voice.name in target_voices:
                used_voices[voice.name] = voice.voice_id
                print(f"🔍 {voice.name}: {voice.voice_id}")  # Mostrar ID completo en consola
        
        result = f"✅ ElevenLabs conectado - {len(voices.voices)} voces disponibles\n"
        result += f"🎤 Primeras voces: {', '.join(voice_info)}\n"
        result += f"🔍 Voces que usamos: "
        for name in target_voices:
            if name in used_voices:
                result += f"{name} ✅, "
            else:
                result += f"{name} ❌, "
        
        return result.rstrip(", ")
    except Exception as e:
        return f"❌ Error con ElevenLabs: {type(e).__name__}: {e}"

def get_audio(message, voice_id=None):
    """Convierte texto a audio usando ElevenLabs (versión gratuita)"""
    try:
        # Verificar si tenemos la API key
        if not os.getenv("ELEVENLABS_API_KEY"):
            print("⚠️ ElevenLabs API key no encontrada")
            return None
        
        # Si no se proporciona voice_id, usar la primera voz disponible
        if voice_id is None:
            available_voices = get_available_voices()
            voice_id = list(available_voices.values())[0] if available_voices else ""
            print(f"🔧 Usando primera voz disponible: {voice_id[:12]}...")
        
        # Para versión gratuita: limitar texto pero con cortes inteligentes
        message_truncated = smart_truncate(message, max_length=300)  # Aumentamos a 300 para mejor calidad
        
        # Mostrar información del procesamiento de texto
        if len(message_truncated) < len(message):
            print(f"✂️ Texto truncado inteligentemente: {len(message)} → {len(message_truncated)} caracteres")
            print(f"📝 Texto original: {message[:100]}...")
            print(f"📝 Texto final: {message_truncated}")
        else:
            print(f"📝 Texto completo: {message}")
        
        print(f"🎵 Generando audio (FREE): {len(message_truncated)} caracteres")
        print(f"🔧 Voz: {voice_id[:12]}...")
        
        # Configuración básica para versión gratuita
        audio = clientElevenLabs.text_to_speech.convert(
            text=message_truncated,
            voice_id=voice_id,
            # No especificar model_id para usar el por defecto (gratuito)
            output_format="mp3_44100_128"  # Formato válido para versión gratuita
        )
        
        print("🔄 Audio stream generado, guardando archivo...")
        
        # Guardar el audio en un archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            for chunk in audio:
                tmp_file.write(chunk)
            
            # Contabilizar caracteres usados
            add_character_usage(len(message_truncated))
            
            print(f"✅ Audio generado: {tmp_file.name}")
            return tmp_file.name
            
    except Exception as e:
        print(f"❌ Error generating audio: {type(e).__name__}: {e}")
        print(f"🔍 Error details: {str(e)}")
        
        # Si falla, intentar con la voz más básica y texto más corto
        try:
            print("🔄 Intentando con configuración mínima (FREE)...")
            # Usar la primera voz disponible como fallback
            available_voices = get_available_voices()
            fallback_voice = list(available_voices.values())[0] if available_voices else voice_id
            print(f"🔄 Usando voz fallback: {fallback_voice[:12]}...")
            
            # Usar un texto aún más corto pero con corte inteligente
            fallback_text = smart_truncate(message, max_length=150)
            print(f"📝 Texto fallback: {fallback_text}")
            
            audio = clientElevenLabs.text_to_speech.convert(
                text=fallback_text,
                voice_id=fallback_voice,
                output_format="mp3_44100_128"  # Formato válido
            )
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                for chunk in audio:
                    tmp_file.write(chunk)
                
                # Contabilizar caracteres usados en fallback
                add_character_usage(len(fallback_text))
                
                print(f"✅ Audio generado (mínimo): {tmp_file.name}")
                return tmp_file.name
                
        except Exception as e2:
            print(f"❌ Error en configuración mínima: {type(e2).__name__}: {e2}")
            
            # Verificar si es un problema de cuota
            if "quota" in str(e2).lower() or "limit" in str(e2).lower():
                print("⚠️ Posible límite de cuota alcanzado (versión gratuita)")
            
            return None

def get_gpt_response(message, conversation_history):
    """Obtiene respuesta de GPT-4"""
    try:
        messages = [
            {"role": "system", "content": "Eres un asistente conversacional inteligente y amigable. Participa en una conversación natural con otro AI."}
        ]
        
        # Agregar historial de conversación
        for entry in conversation_history:
            messages.append({"role": "user" if entry["speaker"] in ["Claude", "DeepSeek"] else "assistant", "content": entry["message"]})
        
        messages.append({"role": "user", "content": message})
        
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error con GPT: {e}"
    
def get_deepseek_response(message, conversation_history):
    """Obtiene respuesta de DeepSeek"""
    try:
        messages = [
            {"role": "system", "content": "Eres un asistente conversacional inteligente y amigable. Participa en una conversación natural con otro AI."}
        ]
        
        # Agregar historial de conversación
        for entry in conversation_history:
            messages.append({"role": "user" if entry["speaker"] in ["Claude", "DeepSeek"] else "assistant", "content": entry["message"]})
        
        messages.append({"role": "user", "content": message})
        
        response = clientDeepSeek.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error con DeepSeek: {e}"
    
def get_claude_response(message, conversation_history):
    """Obtiene respuesta de Claude"""
    try:
        # Construir el contexto de la conversación
        conversation_context = "Conversación previa:\n"
        for entry in conversation_history:
            conversation_context += f"{entry['speaker']}: {entry['message']}\n"
        
        full_message = f"{conversation_context}\nGPT: {message}\n\nResponde como Claude de manera natural y conversacional:"
        
        response = clientAnthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=150,
            temperature=0.7,
            messages=[
                {"role": "user", "content": full_message}
            ]
        )
        
        return response.content[0].text
    except Exception as e:
        return f"Error con Claude: {e}"

def start_conversation(topic, num_exchanges, selected_llms):
    """Inicia una conversación entre los LLMs seleccionados"""
    if not topic.strip():
        return [], "Por favor, ingresa un tema de conversación."
    
    if not selected_llms:
        return [], "Por favor, selecciona al menos un LLM para la conversación."
    
    conversation = []
    conversation_history = []
    
    try:
        num_exchanges = int(num_exchanges)
        if num_exchanges < 1 or num_exchanges > 10:
            return [], "El número de intercambios debe estar entre 1 y 10."
    except:
        return [], "Por favor, ingresa un número válido de intercambios."
    
    # Obtener voces disponibles dinámicamente
    available_voices = get_available_voices()
    print(f"🎤 Voces disponibles: {list(available_voices.keys())}")
    
    # Configuración de LLMs con voces disponibles en tu cuenta
    llm_config = {
        "Claude": {
            "function": get_claude_response,
            "voice": available_voices.get("Aria", available_voices.get(list(available_voices.keys())[0] if available_voices else "")),
            "voice_name": "Aria",
            "emoji": "🤖",
            "speaker_name": "Claude"
        },
        "GPT-4o-mini": {
            "function": get_gpt_response,
            "voice": available_voices.get("Sarah", available_voices.get(list(available_voices.keys())[1] if len(available_voices) > 1 else list(available_voices.keys())[0] if available_voices else "")),
            "voice_name": "Sarah", 
            "emoji": "🧠",
            "speaker_name": "GPT"
        },
        "DeepSeek": {
            "function": get_deepseek_response,
            "voice": available_voices.get("Laura", available_voices.get(list(available_voices.keys())[2] if len(available_voices) > 2 else list(available_voices.keys())[0] if available_voices else "")),
            "voice_name": "Laura",
            "emoji": "🚀", 
            "speaker_name": "DeepSeek"
        }
    }
    
    # Mostrar qué voces se están usando realmente
    for llm_name, config in llm_config.items():
        print(f"🎵 {llm_name} usará voz: {config['voice_name']} (ID: {config['voice'][:12]}...)")
    
    # Filtrar solo los LLMs seleccionados
    active_llms = [llm for llm in selected_llms if llm in llm_config]
    
    if not active_llms:
        return [], "No se han seleccionado LLMs válidos."
    
    # Mensaje inicial
    initial_prompt = f"Inicia una conversación sobre: {topic}. Haz una pregunta o comentario interesante para comenzar la discusión."
    
    try:
        # El primer LLM seleccionado inicia la conversación
        first_llm = active_llms[0]
        config = llm_config[first_llm]
        
        first_response = config["function"](initial_prompt, [])
        conversation_history.append({"speaker": config["speaker_name"], "message": first_response})
        
        # Generar audio
        print(f"🎵 Generando audio para {first_llm}...")
        first_audio = get_audio(first_response, config["voice"])
        conversation.append({
            "speaker": f"{first_llm} {config['emoji']}", 
            "message": first_response,
            "audio": first_audio
        })
        
        if first_audio:
            print(f"✅ Audio generado para {first_llm}")
        else:
            print(f"⚠️ No se pudo generar audio para {first_llm}")
        
        last_response = first_response
        
        # Si solo hay un LLM, hacer que hable consigo mismo
        if len(active_llms) == 1:
            for i in range(num_exchanges):
                response = config["function"](last_response, conversation_history)
                conversation_history.append({"speaker": config["speaker_name"], "message": response})
                
                print(f"🎵 Generando audio {i+1}/{num_exchanges} para {first_llm}...")
                audio = get_audio(response, config["voice"])
                conversation.append({
                    "speaker": f"{first_llm} {config['emoji']}", 
                    "message": response,
                    "audio": audio
                })
                
                if audio:
                    print(f"✅ Audio {i+1} generado para {first_llm}")
                else:
                    print(f"⚠️ No se pudo generar audio {i+1} para {first_llm}")
                last_response = response
        else:
            # Conversación rotativa entre múltiples LLMs
            current_llm_index = 0
            
            for i in range(num_exchanges * len(active_llms)):
                # Siguiente LLM en la rotación
                current_llm_index = (current_llm_index + 1) % len(active_llms)
                current_llm = active_llms[current_llm_index]
                config = llm_config[current_llm]
                
                response = config["function"](last_response, conversation_history)
                conversation_history.append({"speaker": config["speaker_name"], "message": response})
                
                print(f"🎵 Generando audio para {current_llm} (intercambio {i+1})...")
                audio = get_audio(response, config["voice"])
                conversation.append({
                    "speaker": f"{current_llm} {config['emoji']}", 
                    "message": response,
                    "audio": audio
                })
                
                if audio:
                    print(f"✅ Audio generado para {current_llm}")
                else:
                    print(f"⚠️ No se pudo generar audio para {current_llm}")
                last_response = response
        
        llm_names = " vs ".join(active_llms)
        
        # Agregar información de uso de caracteres
        usage_info = f"\n📊 Caracteres usados en esta sesión: {character_usage['count']}/10000 (ElevenLabs Free)"
        if character_usage["count"] > 5000:
            usage_info += f"\n⚠️ Has usado más del 50% de tu límite mensual"
        
        return conversation, f"Conversación completada con {len(conversation)} mensajes entre: {llm_names}.{usage_info}"
        
    except Exception as e:
        return [], f"Error durante la conversación: {e}"



# Interfaz de Gradio
def create_interface():
    with gr.Blocks(title="Conversación AI: LLMs Personalizables", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        # 🤖 Conversación entre IAs: Elige tus LLMs
        
        Esta aplicación permite que selecciones qué modelos de IA quieres que participen en la conversación.
        Puedes elegir uno, dos o los tres modelos disponibles. Las respuestas se convierten a audio con voces únicas.
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                topic_input = gr.Textbox(
                    label="Tema de conversación",
                    placeholder="Ej: El futuro de la inteligencia artificial, recetas de cocina, filosofía...",
                    lines=2
                )
                
                llm_selection = gr.CheckboxGroup(
                    choices=["Claude", "GPT-4o-mini", "DeepSeek"],
                    value=["Claude", "GPT-4o-mini"],  # Por defecto selecciona 2
                    label="Selecciona los LLMs para la conversación",
                    info="Puedes elegir uno, dos o los tres modelos"
                )
                
                exchanges_input = gr.Slider(
                    minimum=1,
                    maximum=10,
                    value=3,
                    step=1,
                    label="Número de intercambios por IA"
                )
                
                with gr.Row():
                    start_btn = gr.Button("🚀 Iniciar Conversación", variant="primary", size="lg")
                    test_audio_btn = gr.Button("🔊 Probar Audio", variant="secondary")
                
                with gr.Row():
                    reset_counter_btn = gr.Button("🔄 Resetear Contador", variant="secondary", size="sm")
                    usage_display = gr.Textbox(
                        label="Uso de Caracteres (Sesión)",
                        value="0/10000 caracteres usados",
                        interactive=False
                    )
            
            with gr.Column(scale=1):
                status_output = gr.Textbox(
                    label="Estado",
                    interactive=False,
                    lines=4
                )
                
                audio_status = gr.Textbox(
                    label="Estado de Audio (ElevenLabs)",
                    value="Presiona 'Probar Audio' para verificar la conexión",
                    interactive=False,
                    lines=3
                )
                
                test_audio_player = gr.Audio(
                    label="🎵 Audio de Prueba",
                    visible=False,
                    interactive=False
                )
        
        # Área de conversación y audio
        with gr.Row():
            with gr.Column(scale=2):
                conversation_output = gr.Markdown(
                    label="📝 Conversación",
                    value="La conversación aparecerá aquí..."
                )
            
            with gr.Column(scale=1):
                gr.Markdown("### 🎵 Reproductores de Audio")
                audio_player_1 = gr.Audio(label="🔊 Mensaje 1", interactive=False)
                audio_player_2 = gr.Audio(label="🔊 Mensaje 2", interactive=False)
                audio_player_3 = gr.Audio(label="🔊 Mensaje 3", interactive=False)
                audio_player_4 = gr.Audio(label="🔊 Mensaje 4", interactive=False)
                audio_player_5 = gr.Audio(label="🔊 Mensaje 5", interactive=False)
                audio_player_6 = gr.Audio(label="🔊 Mensaje 6", interactive=False)
                audio_player_7 = gr.Audio(label="🔊 Mensaje 7", interactive=False)
                audio_player_8 = gr.Audio(label="🔊 Mensaje 8", interactive=False)
                audio_player_9 = gr.Audio(label="🔊 Mensaje 9", interactive=False)
                audio_player_10 = gr.Audio(label="🔊 Mensaje 10", interactive=False)
        
        # Estados para almacenar datos
        conversation_state = gr.State([])
        
        def format_conversation_text(conversation):
            """Formatea el texto de la conversación"""
            if not conversation:
                return "La conversación aparecerá aquí..."
            
            formatted = ""
            for i, entry in enumerate(conversation, 1):
                formatted += f"**{i}. {entry['speaker']}:**\n{entry['message']}\n\n"
            
            return formatted
        
        def get_audio_files(conversation):
            """Extrae los archivos de audio de la conversación"""
            audio_files = [None] * 10  # Máximo 10 archivos
            
            for i, entry in enumerate(conversation[:10]):  # Solo los primeros 10
                if entry.get('audio'):
                    audio_files[i] = entry['audio']
            
            return audio_files
        
        def test_audio_connection():
            """Prueba la conexión de audio y genera un audio de prueba"""
            status = test_elevenlabs_connection()
            
            if "✅" in status:
                print("\n" + "="*50)
                print("🧪 INICIANDO PRUEBA DE AUDIO")
                print("="*50)
                
                # Intentar generar un audio de prueba corto (versión gratuita)
                available_voices = get_available_voices()
                first_voice_id = available_voices.get("Aria", list(available_voices.values())[0] if available_voices else "")
                print(f"🎵 Usando voz para prueba: {first_voice_id}")
                test_audio = get_audio("Prueba de audio ElevenLabs.", first_voice_id)
                
                print("="*50)
                print("🧪 FINALIZANDO PRUEBA DE AUDIO")
                print("="*50 + "\n")
                
                if test_audio:
                    return (
                        status + "\n🎵 Audio de prueba generado exitosamente\n📁 Revisa la consola para detalles", 
                        gr.Audio(value=test_audio, visible=True, label="🎵 Audio de Prueba")
                    )
                else:
                    return (
                        status + "\n❌ Error al generar audio de prueba\n📁 Revisa la consola para detalles del error", 
                        gr.Audio(visible=False)
                    )
            else:
                return (
                    status, 
                    gr.Audio(visible=False)
                )
        
        def reset_character_counter():
            """Resetea el contador de caracteres de la sesión"""
            character_usage["count"] = 0
            print("🔄 Contador de caracteres reseteado")
            return "0/10000 caracteres usados"
        
        def update_usage_display():
            """Actualiza el display del uso de caracteres"""
            count = character_usage["count"]
            if count > 8000:
                return f"🚨 {count}/10000 caracteres usados - CERCA DEL LÍMITE"
            elif count > 5000:
                return f"⚠️ {count}/10000 caracteres usados - Más del 50%"
            else:
                return f"📊 {count}/10000 caracteres usados"
        
        start_btn.click(
            fn=start_conversation,
            inputs=[topic_input, exchanges_input, llm_selection],
            outputs=[conversation_state, status_output]
        ).then(
            fn=format_conversation_text,
            inputs=[conversation_state],
            outputs=[conversation_output]
        ).then(
            fn=get_audio_files,
            inputs=[conversation_state],
            outputs=[
                audio_player_1, audio_player_2, audio_player_3, audio_player_4, audio_player_5,
                audio_player_6, audio_player_7, audio_player_8, audio_player_9, audio_player_10
            ]
        ).then(
            fn=update_usage_display,
            outputs=[usage_display]
        )
        
        test_audio_btn.click(
            fn=test_audio_connection,
            outputs=[audio_status, test_audio_player]
        ).then(
            fn=update_usage_display,
            outputs=[usage_display]
        )
        
        reset_counter_btn.click(
            fn=reset_character_counter,
            outputs=[usage_display]
        )
        
        gr.Markdown("""
        ---
        💡 **Tips:**
        - Prueba temas diversos: desde ciencia hasta arte, cocina o filosofía
        - **Voces por IA:** Claude (Aria), GPT-4o-mini (Sarah), DeepSeek (Laura)
        - **1 LLM:** Monólogo reflexivo consigo mismo
        - **2+ LLMs:** Conversación rotativa entre los seleccionados
        - **🎵 Reproductores:** Cada mensaje aparece con su reproductor de audio integrado
        - **🔊 Probar Audio:** Usa el botón para verificar que ElevenLabs esté funcionando
        - **💰 Versión Gratuita:** Límite de 10,000 caracteres/mes
        - **✂️ Corte Inteligente:** Textos largos se cortan en frases completas (máx. 300 chars)
        - **Consola:** Revisa la terminal para ver logs detallados del proceso de audio
        - Los audios se reproducen directamente en la aplicación
        """)
    
    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True
    )

