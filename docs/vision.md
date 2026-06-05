# Dashvis — Visión

> El ADN del proyecto. Cambia poco — solo cuando cambia la dirección, las prioridades o la identidad de Dashvis.  
> Para el estado operativo del proyecto consultar `project-log.md`. Para la arquitectura técnica, `architecture.md`.

---

## 1. El proyecto

Construir un asistente domótico avanzado para una habitación en Benidorm (Valencia, España). El objetivo es doble: crear el sistema **y** aprender en el proceso. No es un proyecto donde un modelo programa todo — es un proyecto de ingeniería donde el propietario adquiere conocimientos reales de arquitectura de sistemas, IoT, redes, señales y programación construyendo cada componente.

### En una frase

> Sistema domótico con IA central que controla la habitación, tiene personalidad propia y aprende del usuario, construido con hardware real y software propio.

---

## 2. Intención del asistente

Dashvis no es Alexa ni Siri. Las diferencias son deliberadas y definen la dirección de todo el proyecto.

**Lo que Dashvis es:**
- Un asistente con vida propia — estado interno, emociones, comportamiento proactivo entre interacciones
- Un sistema que converge voz, visión, domótica y robótica en una arquitectura coherente, no módulos inconexos
- Una presencia visual real en la habitación, no solo backend invisible
- Un sistema que aprende del usuario con el tiempo y lo recuerda entre sesiones
- Un proyecto que el propietario entiende porque lo construyó pieza a pieza

**Lo que Dashvis no es:**
- Un wrapper de voz sobre una API cloud sin control propio
- Un sistema donde la IA toma todas las decisiones (hay heurísticas locales para lo predecible)
- Un proyecto cerrado — es modular y ampliable por diseño
- Un sistema que depende de internet para funcionar en lo esencial

**Las intenciones originales en palabras del propietario:**
- "Quiero un asistente domótico estilo Jarvis, pero modular y ampliable"
- "No quiero depender de la IA para programarlo todo; quiero aprender mientras construyo"
- "El sistema debe permitir heurísticas locales para ahorrar tokens y escalar el uso de IA solo cuando haga falta"
- "La representación visual del asistente es importante, no es solo backend"
- "Quiero que el robot, la domótica, la voz y la visión converjan en una arquitectura coherente"

---

## 3. Filosofía de aprendizaje

**Regla fundamental:** el propietario implementa antes de recibir la solución.

El proceso siempre sigue este orden:

1. Claude explica el concepto y el porqué
2. El propietario lo implementa
3. Claude revisa y da feedback
4. Si hay bloqueo: pista mínima, no solución completa

**Lo que nunca se hace:**
- Dar código terminado sin comprensión previa
- Saltar pasos "para avanzar más rápido"
- Usar herramientas sin entender qué hacen internamente

**Por qué funciona este enfoque:**  
Cada bloque que el propietario construye enseña un dominio diferente. Un ESP32 enseña señales y hardware. Una API REST enseña redes y protocolos. ROS2 enseña sistemas distribuidos. Al terminar el proyecto, el propietario puede mantener, depurar y extender el sistema sin dependencia de nadie.

---

## 4. Decisiones de arquitectura y razonamiento

Cada decisión incluye la alternativa considerada y la razón de la elección. Cambiar cualquiera requiere actualizar este archivo.

### 4.1 Router LLM + heurísticas locales (no LLM puro)

Los comandos simples ("enciende la luz", "sube la persiana") no necesitan un modelo de cientos de miles de millones de parámetros. El router clasifica primero con reglas locales y solo escala al LLM cuando la confianza es baja o la consulta es compleja. Reduce coste, latencia y dependencia de internet simultáneamente.

### 4.2 Modo concurrente como decisión de arquitectura temprana

Dashvis no dice "ejecutando..." y se queda en silencio. Responde de inmediato y ejecuta en paralelo. Esto requiere diseño async desde la fase 1 — no se puede añadir como capa posterior sin reescribir la lógica de control.

### 4.3 Vida propia como máquina de estados, no como prompt

El asistente tiene un estado interno (ánimo, nivel de energía, modo activo/pasivo) que cambia en función del tiempo, los eventos y las interacciones. Esto va más allá de incluir "sé amigable" en el system prompt — es un estado persistente que afecta cómo responde y qué hace proactivamente entre interacciones.

### 4.4 Wake word local (no cloud)

**Elegido:** openWakeWord o Porcupine, ejecutado en RPi.  
**Descartado:** wake word de Alexa o cualquier servicio cloud.  
**Razón:** privacidad (el audio no sale de la habitación hasta que el wake word activa), latencia (instantánea), funcionamiento offline total.

### 4.5 Servo sobre interruptor físico (no smart switch)

**Elegido:** servo motor que presiona el botón del interruptor existente, controlado por ESP32.  
**Descartado:** reemplazar el interruptor por uno inteligente (Shelly, Sonoff, etc.).  
**Razón:** no requiere trabajo eléctrico, es reversible al 100%, elimina riesgo de manipular instalación. El prototipo en cartón permite probar la mecánica antes de instalar en producción.

### 4.6 Home Assistant como orquestador de domótica (no custom)

**Elegido:** Home Assistant en RPi como hub de dispositivos.  
**Descartado:** código propio para gestionar todos los dispositivos.  
**Razón:** HA tiene soporte nativo para Zigbee/Z-Wave/MQTT, interfaz web, automatizaciones, integración con Alexa y una comunidad enorme. El asistente IA custom se conecta a HA via API/MQTT — no lo reemplaza.

### 4.7 Alexa como periférico, no como cerebro

Los dispositivos Echo se usan como micrófonos de calidad y altavoces en zonas de la habitación. El LLM custom decide y responde. Esto preserva la inversión en hardware sin ceder el control a Amazon. El usuario habla a Alexa; Dashvis responde.

### 4.8 ROS2 para el robot (no framework custom)

**Elegido:** ROS2 Humble + rclpy (Python).  
**Razón:** estándar de la industria, ecosistema de drivers y paquetes maduro, arquitectura de nodos que encaja con el diseño modular requerido. La curva de aprendizaje es real pero el conocimiento es completamente transferible a otros proyectos de robótica.

### 4.9 WebRTC para vídeo FPV (no RTSP ni HLS)

| Protocolo  | Latencia típica |
|------------|-----------------|
| WebRTC     | 50–150 ms       |
| RTSP       | 2–5 s           |
| HTTP MJPEG | > 1 s           |
| HLS        | > 5 s           |

WebRTC es la única opción con latencia sub-150 ms real. Funciona nativamente en cualquier navegador. El conocimiento adquirido es reutilizable para streaming de audio, datachannel y futuros casos de uso.

### 4.10 ChromaDB para memoria (no base de datos relacional)

La memoria del asistente debe ser recuperable por significado ("¿cuándo fue la última vez que estudié más de 3 horas seguidas?"), no por clave exacta. Los embeddings permiten búsqueda semántica. ChromaDB es local, Python-nativo y no requiere servidor externo.

### 4.11 MediaPipe Face Mesh para DMS (no cámara cloud)

**Elegido:** MediaPipe en local, sin enviar vídeo a ningún servicio.  
**Razón:** privacidad crítica. El vídeo de la habitación nunca sale del dispositivo. MediaPipe corre en tiempo real en CPU modesta. Los 468 landmarks faciales son suficientes para calcular PERCLOS, gaze score y head pose deviation.

### 4.12 Python como lenguaje principal

Python para todo excepto ESP32 (C++ requerido por Arduino). ROS2 soporta Python via rclpy. El ecosistema de IA/ML, audio, visión y networking es el mejor disponible en Python. La velocidad de prototipado compensa la diferencia de rendimiento frente a otros lenguajes para este caso de uso.

---

## 5. Restricciones y principios no negociables

1. **Sin tocar el cableado eléctrico.** Todos los actuadores físicos interactúan con los dispositivos de forma no destructiva y reversible.
2. **Local-first.** El procesamiento de voz, visión y datos sensibles ocurre en hardware local. La nube es opcional y se activa explícitamente.
3. **Modular por diseño.** Cada componente puede reemplazarse sin afectar al resto. Las interfaces entre capas son explícitas: MQTT topics, REST endpoints, ROS2 topics.
4. **El propietario entiende lo que construye.** No se avanza sin comprensión. La velocidad de aprendizaje manda sobre la velocidad de construcción.
5. **Privacidad.** El vídeo de las cámaras y el audio de los micrófonos nunca salen del sistema local salvo cuando es explícitamente requerido y aceptado.

---

*Generado en la sesión fundacional. Próxima revisión: si cambia la dirección del proyecto.*
