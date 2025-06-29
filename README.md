# 🤖 Conversación entre IAs: Elige tus LLMs

Una aplicación demo avanzada que permite que múltiples modelos de IA (GPT-4o-mini, Claude y DeepSeek) mantengan conversaciones naturales sobre cualquier tema, con síntesis de voz de alta calidad usando ElevenLabs. Optimizada para la versión gratuita de ElevenLabs con sistema de corte inteligente y reproductores integrados.

## 🚀 Características Principales

### 🎯 **Conversación Inteligente**
- **Selección flexible de LLMs**: Elige uno, dos o los tres modelos disponibles
- **Conversación adaptativa**: 
  - **1 LLM**: Monólogo reflexivo consigo mismo
  - **2+ LLMs**: Conversación rotativa dinámica entre los seleccionados
- **Temas personalizables**: Conversa sobre cualquier tema que elijas
- **Intercambios configurables**: De 1 a 10 intercambios por IA

### 🎵 **Audio de Alta Calidad**
- **Text-to-Speech Premium**: Síntesis de voz natural con ElevenLabs
- **Voces diferenciadas**: Cada IA tiene su propia voz única
- **Reproductores integrados**: Audio directo en la aplicación (sin descargas)
- **Corte inteligente**: Textos largos se cortan respetando frases completas
- **Optimizado para versión gratuita**: Gestión eficiente de la cuota de caracteres

### 🛠️ **Funcionalidades Avanzadas**
- **Sistema dinámico de voces**: Detecta automáticamente las voces disponibles
- **Contador de caracteres**: Monitor en tiempo real del uso de ElevenLabs
- **Diagnóstico de audio**: Herramientas para probar y solucionar problemas
- **Interfaz moderna**: UI intuitiva y responsive con Gradio
- **Logs detallados**: Información completa en consola para debugging

## 📋 Requisitos

### 🐍 **Software**
- **Python 3.8+** (Recomendado: 3.10+)
- **Sistema Operativo**: Windows, macOS, Linux

### 🔑 **API Keys Necesarias**
| Servicio | Propósito | Tipo de Cuenta | Límites Gratuitos |
|----------|-----------|----------------|-------------------|
| **OpenAI** | GPT-4o-mini | Pago | Créditos según plan |
| **Anthropic** | Claude | Pago | Créditos según plan |
| **DeepSeek** | DeepSeek Chat | Gratuito/Pago | Variable |
| **ElevenLabs** | Text-to-Speech | **Gratuito/Pago** | **10,000 caracteres/mes** |

> 💡 **Nota**: La aplicación está especialmente optimizada para la **versión gratuita de ElevenLabs** (10k caracteres/mes)

## 🛠️ Instalación

### 📦 **Paso 1: Descarga del Proyecto**
```bash
# Clona el repositorio
git clone https://github.com/EstebanDevJR/Demo_LLM_Conversacionales.git
cd IAs-conversacionales-demo

# O descarga directamente y extrae los archivos
```

### 🐍 **Paso 2: Entorno Virtual (Recomendado)**
```bash
# Crear entorno virtual
python -m venv env

# Activar entorno virtual
# En Windows:
env\Scripts\activate
# En macOS/Linux:
source env/bin/activate
```

### 📚 **Paso 3: Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### 🔑 **Paso 4: Configurar API Keys**
Crea un archivo `.env` en el directorio raíz:

```env
# API Keys (reemplaza con tus claves reales)
OPENAI_API_KEY=tu_clave_openai_aqui
ANTHROPIC_API_KEY=tu_clave_anthropic_aqui  
DEEPSEEK_API_KEY=tu_clave_deepseek_aqui
ELEVENLABS_API_KEY=tu_clave_elevenlabs_aqui
```

> ⚠️ **Importante**: Nunca compartas tus API keys públicamente

## 🎯 Uso

### 🚀 **Iniciar la Aplicación**
```bash
# Asegúrate de estar en el directorio del proyecto y con el entorno activado
python app.py
```

### 🌐 **Acceder a la Interfaz**
- **URL Local**: `http://localhost:7860`
- **URL Pública**: Se genera automáticamente (válida por 1 semana)
- La aplicación se abre automáticamente en tu navegador por defecto

### 🎮 **Guía de Uso Paso a Paso**

#### **1. 🔊 Probar Audio (Recomendado)**
- Presiona **"🔊 Probar Audio"** para verificar que ElevenLabs funcione
- Revisa el estado de conexión y voces disponibles
- Escucha el audio de prueba generado

#### **2. 📝 Configurar Conversación**
```
📋 Tema de conversación:
└── Ej: "El futuro de la inteligencia artificial"
    
☑️ Seleccionar LLMs:
├── Claude (Voz: Aria) 🤖
├── GPT-4o-mini (Voz: Sarah) 🧠  
└── DeepSeek (Voz: Laura) 🚀

🎛️ Intercambios por IA: 1-10
└── Número de veces que cada IA participará
```

#### **3. 🚀 Iniciar y Disfrutar**
- Presiona **"🚀 Iniciar Conversación"**
- Observa el progreso en tiempo real
- Escucha los audios con los reproductores integrados
- Monitorea el uso de caracteres de ElevenLabs

## 💡 Ejemplos de Temas

### 🔬 **Ciencia y Tecnología**
- "El futuro de la inteligencia artificial y su impacto en la humanidad"
- "Exploración espacial: ¿colonización de Marte o exploración del espacio profundo?"
- "Biotecnología: beneficios y riesgos de la edición genética"
- "Computación cuántica y sus aplicaciones prácticas"

### 🎨 **Arte y Creatividad**
- "El papel del arte en la expresión de emociones humanas"
- "Inteligencia artificial vs creatividad humana en el arte"
- "La evolución de la música a través de las décadas"
- "Fotografía digital vs análoga: ¿cuál captura mejor la realidad?"

### 🍳 **Estilo de Vida**
- "Recetas de cocina fusion: combinando tradiciones culinarias"
- "Minimalismo vs maximalismo en el diseño de interiores"
- "Beneficios de la meditación en la vida moderna"
- "Sostenibilidad: pequeños cambios, gran impacto"

### 🧠 **Filosofía y Ética**
- "¿Qué define la consciencia en seres artificiales?"
- "Dilemas éticos en la era de la automatización"
- "El libre albedrío en un universo determinista"
- "La naturaleza de la felicidad según diferentes culturas"

## 🎵 Sistema de Voces

### 🎤 **Voces Asignadas (Dinámicas)**
| IA | Voz Principal | Tipo | Características |
|-----|---------------|------|-----------------|
| **Claude 🤖** | Aria | Femenina | Natural, clara |
| **GPT-4o-mini 🧠** | Sarah | Femenina | Profesional, cálida |
| **DeepSeek 🚀** | Laura | Femenina | Moderna, expresiva |

> 🔄 **Sistema Dinámico**: La aplicación detecta automáticamente las voces disponibles en tu cuenta de ElevenLabs y se adapta accordingly.

### ✂️ **Corte Inteligente de Texto**
- **Límite**: 300 caracteres por audio (optimizado para ElevenLabs gratuito)
- **Prioridad de corte**:
  1. Oraciones completas (`. ! ?`)
  2. Cláusulas (`, ;`)
  3. Palabras completas (espacios)
  4. Puntos suspensivos como último recurso

## 📝 Características Especiales

### 💰 **Optimización para ElevenLabs Gratuito**
- **Contador en tiempo real**: Monitorea caracteres usados (límite: 10,000/mes)
- **Advertencias inteligentes**: Alertas al 50% y 80% del límite
- **Corte inteligente**: Preserva frases completas mientras optimiza uso
- **Botón de reset**: Reinicia contador de sesión

### 🔍 **Herramientas de Diagnóstico**
- **Prueba de conexión**: Verifica estado de todas las APIs
- **Detección de voces**: Lista voces disponibles dinámicamente
- **Logs detallados**: Información completa en consola
- **Manejo de errores**: Fallbacks automáticos para problemas comunes

### 🎛️ **Flexibilidad de Configuración**
- **Modos de conversación**:
  - **1 LLM**: Monólogo reflexivo (útil para análisis profundos)
  - **2 LLMs**: Diálogo dinámico (debate balanceado)
  - **3 LLMs**: Conversación grupal (perspectivas múltiples)
- **Intercambios ajustables**: 1-10 rondas por IA
- **Reproductores integrados**: Sin necesidad de descargas

## 🔧 Solución de Problemas

### 🚨 **Problemas Comunes y Soluciones**

#### 🔑 **Errores de API Keys**
```
❌ Error: "API key not found" / "Invalid API key"
✅ Solución:
1. Verifica que el archivo .env esté en el directorio raíz
2. Confirma que las API keys no tengan espacios extra
3. Asegúrate de que las APIs tengan créditos/límites disponibles
4. Reinicia la aplicación después de cambiar las keys
```

#### 🎵 **Problemas de Audio**
```
❌ Error: "No se generan audios" / "Voice not found"
✅ Solución:
1. Usa el botón "🔊 Probar Audio" para diagnosticar
2. Verifica que tengas caracteres disponibles en ElevenLabs
3. La aplicación detecta voces automáticamente - no edites IDs manualmente
4. Revisa los logs en consola para errores específicos
```

#### 🌐 **Errores de Conexión**
```
❌ Error: "Connection timeout" / "API unreachable"
✅ Solución:
1. Verifica tu conexión a internet
2. Comprueba si hay firewalls bloqueando Python
3. Algunas APIs pueden tener límites de región
4. Intenta reiniciar la aplicación
```

#### 💾 **Problemas de Instalación**
```
❌ Error: "Module not found" / "Import error"
✅ Solución:
1. Activa el entorno virtual antes de instalar
2. Ejecuta: pip install --upgrade pip
3. Reinstala dependencias: pip install -r requirements.txt --force-reinstall
4. Verifica la versión de Python (3.8+ requerido)
```

### 📊 **Herramientas de Diagnóstico Integradas**

#### 🔍 **Información de Sistema**
- **Estado de APIs**: Cada API muestra su estado de conexión
- **Voces disponibles**: Lista dinámica actualizada en tiempo real
- **Contador de caracteres**: Monitor de uso de ElevenLabs
- **Logs detallados**: Información completa en la consola

#### 🧪 **Modo Debug**
Para activar logs más detallados, ejecuta:
```bash
# Modo verbose (más información en consola)
python app.py --verbose

# O simplemente observa la consola durante el uso normal
```

### 📞 **Obtener Ayuda**

#### 🌐 **Recursos Útiles**
- **OpenAI**: [platform.openai.com](https://platform.openai.com)
- **Anthropic**: [console.anthropic.com](https://console.anthropic.com)
- **DeepSeek**: [platform.deepseek.com](https://platform.deepseek.com)
- **ElevenLabs**: [elevenlabs.io](https://elevenlabs.io)

#### 🐛 **Reportar Problemas**
Si encuentras un bug o necesitas ayuda:
1. **Revisa los logs** en la consola
2. **Usa las herramientas de diagnóstico** integradas
3. **Verifica la configuración** con el botón de prueba
4. **Incluye información** del sistema y errores específicos

---

## 🎯 Consejos y Mejores Prácticas

### 💡 **Optimización del Uso**
- **Para ElevenLabs gratuito**: Usa temas concisos para maximizar conversaciones
- **Para calidad de audio**: Permite que el corte inteligente preserve frases completas
- **Para debates interesantes**: Selecciona 2-3 LLMs con temas controversiales
- **Para análisis profundos**: Usa 1 LLM con muchos intercambios

### 🎨 **Temas Recomendados**
- **Temas específicos** funcionan mejor que generales
- **Preguntas abiertas** generan conversaciones más dinámicas
- **Dilemas éticos** crean debates interesantes entre múltiples IAs
- **Temas técnicos** permiten explorar diferentes perspectivas

### 🔊 **Mejores Resultados de Audio**
- **Prueba el audio** antes de conversaciones largas
- **Monitorea el contador** para no agotar la cuota
- **Usa el botón reset** al inicio de nuevas sesiones
- **Los reproductores integrados** ofrecen mejor experiencia que descargas

---

¡Disfruta experimentando con la conversación entre IAs! 🤖✨

> Optimizado para aprendizaje, experimentación y diversión 
