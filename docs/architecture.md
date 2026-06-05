# Dashvis — Arquitectura

> Cómo está organizado el sistema. Cambia cuando cambia la estructura, los protocolos o las responsabilidades de cada capa.  
> Para el porqué de las decisiones ver `vision.md`. Para el estado actual ver `project-log.md`.

---

## 1. Capas del sistema

Arquitectura **hub-and-spoke**: el cerebro central orquesta los cinco módulos, cada uno conectado directamente a él. Los módulos no se comunican entre sí — todo flujo pasa por el cerebro o, a partir de la fase 7, por el event bus.

```
┌─────────────────────────────────────────────────────────────────┐
│                     CEREBRO CENTRAL                             │
│  LLM · heurísticas locales · TTS · modo concurrente            │
│  vida propia · emociones · comportamiento proactivo · memoria  │
└─────────────────────────────────────────────────────────────────┘
   ↑ entrada      ↓ salida     ↕ control    ↕ control    ↕ servicio
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│PERCEPCIÓN│  │  SALIDA  │  │ DOMÓTICA │  │  ROBOT   │  │  DATOS   │
│          │  │  VISUAL  │  │          │  │          │  │          │
│Voz       │  │Proyect.  │  │ESP32     │  │ROS2      │  │Sheets    │
│Visión+DMS│  │Táctil    │  │HA + MQTT │  │WebRTC    │  │Vector DB │
│Telemetría│  │Avatar    │  │Actuadores│  │Gamepad   │  │Tokens    │
└──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘

↑  entrada   el módulo envía datos al cerebro (voz, imagen, telemetría)
↓  salida    el cerebro dirige el módulo; no hay retorno de estado relevante
↕  control   el cerebro envía comandos; el módulo devuelve estado real
↕  servicio  DATOS no es un módulo peer — es infraestructura transversal.
             El cerebro lee y escribe aquí; otros módulos también producen
             datos que se almacenan (logs, métricas, contexto de sesión).
```

> **Estado actual:** todo el sistema está en fase de planificación. Ninguna capa tiene implementación real todavía. Las secciones siguientes describen el diseño objetivo, no lo construido.

---

### 1.1 Cerebro central

El núcleo del sistema. Recibe toda la percepción, toma decisiones, genera respuestas y orquesta actuadores.

| Componente | Responsabilidad | Estado |
|------------|----------------|--------|
| Router de intenciones | Clasifica cada entrada: heurística local o LLM | Planificado |
| Heurísticas locales | Comandos simples, regex, reglas sin coste de tokens | Planificado |
| LLM API | Lenguaje natural complejo, razonamiento | Planificado |
| TTS | Síntesis de voz para la respuesta de salida | Planificado |
| Modo concurrente | Habla mientras ejecuta (asyncio / threads) | Planificado |
| Vida propia | Máquina de estados: ánimo, energía, proactividad | Planificado |
| Memoria LTP | RAG sobre ChromaDB, recuperación semántica | Planificado |

### 1.2 Percepción

| Componente | Detalle | Estado |
|------------|---------|--------|
| Voz | Micro lavalier (camiseta) o array fijo. Wake word local. STT Whisper/cloud. | Planificado |
| Visión + DMS | Cámaras. MediaPipe Face Mesh. Métricas: PERCLOS, gaze score, head pose. Umbral: 30 s distracción → alerta. | Planificado |
| Telemetría | Screen time de portátil y móvil via API del SO. | Planificado |

### 1.3 Salida visual

| Componente | Detalle | Estado |
|------------|---------|--------|
| Proyectores mini | XGIMI / Anker Capsule / BenQ. Distribuidos por zonas. | Planificado |
| Superficie táctil | Overlay sobre proyección via marco IR o Ultraleap. | Planificado |
| Avatar | Representación visual en TV o proyector. Expresa estados emocionales. | Planificado |

### 1.4 Domótica

| Componente | Detalle | Estado |
|------------|---------|--------|
| Actuadores físicos | Servo + ESP32. Presiona botón del interruptor existente. Sin cableado eléctrico. | Planificado |
| Orquestador local | Home Assistant en RPi. MQTT como bus de mensajes. | Planificado |
| Ecosistema | Alexa como periférico (micro/altavoz). Zigbee/Z-Wave gestionados por HA. | Planificado |

### 1.5 Robot

| Componente | Detalle | Estado |
|------------|---------|--------|
| Hardware | Chasis movible. Brazos modulares. Diseñado para añadir componentes. | Planificado |
| Control + cámara | Gamepad BT. Cámara FPV via WebRTC. Latencia < 150 ms. | Planificado |
| Software | ROS2 Humble. Un nodo por articulación. Plugins OTA. | Planificado |

### 1.6 Datos personales

| Componente | Detalle | Estado |
|------------|---------|--------|
| Fuentes externas | Google Sheets y Excel via API. Lectura y escritura. | Planificado |
| Memoria persistente | ChromaDB local. RAG. Búsqueda semántica sobre historial y preferencias. | Planificado |
| Gestión de tokens | Heurísticas capturan ~70-80% de comandos. Contexto del LLM comprimido. | Planificado |

---

## 2. Stack tecnológico

Cada tecnología en esta tabla es una hipótesis de trabajo, no un compromiso. Se confirma o se sustituye cuando realmente se trabaja la fase que la requiere. Cambiar una herramienta no rompe el proyecto: las capas se comunican por interfaces explícitas (MQTT topics, REST endpoints, ROS2 topics), no por dependencias directas entre herramientas.

```
Capa                Tecnología elegida         Alternativas descartadas
──────────────────────────────────────────────────────────────────────
LLM                 Claude API / GPT-4o        Ollama local (menor calidad)
Heurísticas         Python regex + reglas      spaCy NLP ligero
Wake word           openWakeWord               Porcupine (más preciso, pago)
STT                 Whisper local              Deepgram / Whisper API (nube)
TTS                 edge-tts / ElevenLabs      Coqui (local, menor calidad)
Vector DB           ChromaDB                   Pinecone (cloud), Qdrant
IoT hub             Home Assistant + RPi       OpenHAB, Node-RED
Protocolo IoT       MQTT (Mosquitto)           CoAP, HTTP polling
Microcontrolador    ESP32                      Arduino Nano, RPi Pico
Visión              OpenCV + MediaPipe         dlib, InsightFace
Robot OS            ROS2 Humble (rclpy)        framework custom
Video stream        WebRTC                     RTSP, HLS
Event bus           Redis Pub/Sub              RabbitMQ, ZeroMQ
Contenedores        Docker + Compose           systemd units
Hardware central    Raspberry Pi 4/5           NVIDIA Jetson (coste elevado)
```

---

## 3. Hoja de ruta de fases

Las fases 0–2 son secuenciales: todo lo demás las necesita como base.  
A partir de la fase 3, robot (fase 6) puede avanzar en paralelo con domótica (fases 3–5).

| Fase | Título | Dominio | Habilita en el sistema |
|------|--------|---------|------------------------|
| 0 | Entorno y fundamentos | Base | Toda la infraestructura |
| 1 | APIs y arquitectura | IA / Backend | Cerebro central |
| 2 | Voz y señales | Audio | Entrada de voz + TTS |
| 3 | IoT y ESP32 | Hardware / IoT | Domótica: persianas, luces |
| 4 | Visión artificial | Computer Vision | DMS: atención al estudiar |
| 5 | Redes y protocolos | Networking | FPV robot + integración |
| 6 | Robótica y ROS2 | Robótica | Robot con brazos y cámara |
| 7 | Integración total | Arquitectura | Sistema completo Dashvis |

### Estructura de retos por fase

Los retos no están fijados de antemano. Se generan al crear el brief de cada fase, calibrados al nivel de partida real del propietario en ese momento. La estructura es siempre la misma:

- **Mini-retos**: uno por área de skill de la fase. Calibrados tras preguntas de nivel al inicio del brief.
- **Reto integrador**: un artefacto funcional que combina todos los skills de la fase.
- **Reto de extensión** *(opcional)*: para profundizar si la fase se completa antes de lo previsto.

### Detalle por fase

**Fase 0 — Entorno y fundamentos** *(2–3 semanas)*  
Aprenderás: Linux CLI, Python, Git, redes básicas (IP, puertos, SSH, DNS, NAT).  
Construirás: RPi accesible por SSH, script de monitorización CPU/RAM con alertas en CSV.

**Fase 1 — APIs y arquitectura** *(3–4 semanas)*  
Aprenderás: HTTP/REST, autenticación (API keys, Bearer, OAuth), arquitectura cliente-servidor, async/await, rate limiting.  
Construirás: wrapper LLM con router heurística/IA, medición de latencia y coste de cada ruta.

**Fase 2 — Voz y señales** *(3–4 semanas)*  
Aprenderás: señales de audio (PCM, sample rate, WAV), streams en tiempo real, wake word, STT, TTS, WebSockets.  
Construirás: pipeline completo wake word → STT → LLM/heurística → TTS con latencia < 2 s.

**Fase 3 — IoT y ESP32** *(4–5 semanas)*  
Aprenderás: GPIO/ADC/PWM, C++ Arduino, MQTT (pub/sub, QoS, retain), servomotores, Wi-Fi/OTA.  
Construirás: ESP32 + servo sobre interruptor de persiana, control por voz de extremo a extremo.

**Fase 4 — Visión artificial** *(3–4 semanas)*  
Aprenderás: OpenCV, MediaPipe Face Mesh (468 landmarks), estimación de mirada y pose, métricas DMS.  
Construirás: sistema DMS activo — avisa si 30 s de distracción al estudiar.

**Fase 5 — Redes y protocolos** *(3–4 semanas)*  
Aprenderás: TCP vs UDP, WebRTC (ICE/STUN/RTCPeerConnection), latencia/jitter, TLS, pub/sub vs req-response.  
Construirás: stream WebRTC al navegador con latencia visible y reconexión automática.

**Fase 6 — Robótica y ROS2** *(6–8 semanas)*  
Aprenderás: ROS2 (nodos/topics/services/actions), PID básico, cinemática, serial RPi↔MCU, joy package.  
Construirás: brazo 3+ DOF controlado por gamepad + cámara WebRTC, arquitectura modular.

**Fase 7 — Integración total** *(4–6 semanas)*  
Aprenderás: event-driven (Redis Pub/Sub), service discovery (mDNS), fallbacks, Docker/Compose, logging estructurado.  
Construirás: sistema completo integrado con event bus central.

---

## 4. Estructura del repositorio

El repositorio organiza el código por **qué hace**, no por cuándo se aprendió. Las fases son una estructura de aprendizaje; el repo es una estructura de sistema.

```
dashvis/
├── docs/             ← vision.md, architecture.md, project-log.md, devlog.md
├── scratch/          ← ejercicios de aprendizaje por fase, nunca van a producción
│   ├── phase_0/
│   ├── phase_1/
│   └── ...
├── cerebro/          ← router LLM + heurísticas (aparece en Phase 1)
├── percepcion/       ← voz, visión, DMS, telemetría (Phases 2 y 4)
├── domotica/         ← ESP32, HA, MQTT, actuadores (Phase 3)
├── robot/            ← ROS2, WebRTC, gamepad (Phases 5 y 6)
└── datos/            ← ChromaDB, Sheets, memoria (Phase 1 en adelante)
```

### Reglas

- `scratch/phase_N/` existe desde el inicio de cada fase y se archiva al terminarla.
- Las carpetas del sistema se crean al construir ese módulo, no antes.
- Los docs viven en raíz del repo y se versionan junto al código.

### Cómo pasa el código a producción

La pregunta que determina dónde va el código es una sola: **¿es este código un componente de Dashvis, o es un ejercicio para aprender a construirlo?**

- Componente de Dashvis → carpeta arquitectónica
- Ejercicio de aprendizaje → `scratch/phase_N/`

Aplicado a los tipos de output de cada fase:

**Mini-retos** → siempre a `scratch/phase_N/`. Son ejercicios calibrados para adquirir los skills del dominio. Referencia histórica, nunca producción.

**Reto integrador** → es la culminación de los mini-retos y combina todos los skills de la fase en un artefacto funcional. Para Phases 1–7, ese artefacto ES el componente de Dashvis que describe el "Construirás" — va a su carpeta arquitectónica. Para Phase 0, incluso el reto integrador es un ejercicio (el servidor TCP no es un componente de Dashvis) — va a scratch.

**Phase 0 es la excepción completa**: nada de lo que se construye en esta fase es un componente de Dashvis. Todo va a `scratch/phase_0/`.

```
Ejemplo Phase 1:
  scratch/phase_1/
    http_basics.py     ← mini-reto: aprender HTTP
    auth_test.py       ← mini-reto: aprender autenticación

  cerebro/
    router.py          ← reto integrador = Construirás: wrapper LLM + router heurística/IA
```

> Esta estructura debe incluirse en todos los briefs para que cualquier sesión sepa exactamente dónde poner el código.

---

## 5. Sistema de contexto portátil

Para trabajar una fase en una conversación separada y volver con el output, se usan dos plantillas. En cualquier momento se puede pedir "dame el brief de la Fase N" y se genera listo para pegar.

### 5.1 Brief de sesión

Se genera en la conversación principal y se pega como primer mensaje en la sesión de trabajo.

```
DASHVIS PROJECT BRIEF — Fase N: [Nombre]
════════════════════════════════════════════════════════════════
PROYECTO
Asistente domótico con IA central para habitación. Arquitectura
hub-and-spoke: cerebro central (LLM + heurísticas + vida propia)
conectado a 5 módulos — percepción (voz/visión/telemetría), salida
visual (proyectores/táctil/avatar), domótica (ESP32/HA/MQTT),
robot (ROS2/WebRTC/gamepad), datos (VectorDB/Sheets).
Stack: Python · Raspberry Pi · ESP32 · Home Assistant · MQTT.
Filosofía: explica el concepto, yo implemento, pista mínima si
me bloqueo. No código terminado sin comprensión previa.

ESTADO DEL PROYECTO
[Pegar contenido actual de project-log.md]

ESTRUCTURA DEL REPO
dashvis/
├── docs/
├── scratch/
│   └── phase_N/      ← mini-retos y ejercicios, nunca van a producción
[carpetas del sistema existentes — solo las ya creadas, ej.:]
├── cerebro/           ← desde Phase 1
├── percepcion/        ← desde Phase 2
└── ...
Regla: ejercicios → scratch/phase_N/ · componentes de Dashvis → carpeta arquitectónica
El reto integrador de cada fase ES el componente — va a su carpeta arquitectónica.
Phase 0: todo va a scratch, nada es componente de Dashvis todavía.

ESTA SESIÓN — Fase N: [Nombre]
Aprenderás: [lista de skills de esa fase]
Construirás: [build target]
Mini-retos: [generados en este brief tras calibración de nivel]
Reto integrador: [generado en este brief]

TAREA DE HOY
[Lo que se quiere trabajar específicamente en esta sesión]
════════════════════════════════════════════════════════════════
```

### 5.2 Retorno de sesión

Se pega en la conversación principal al volver, para actualizar `project-log.md`.

```
RETORNO FASE N: [Nombre]
Estado: ✅ Completado / 🔄 En progreso / 🚧 Bloqueado en [punto]

Decisiones tomadas:
- Elegí X sobre Y porque [razón breve]

Artefactos producidos:
- archivo.py: [qué hace en una línea]

Conceptos que entiendo bien: [lista]
Dudas que quedaron abiertas: [si las hay]
Próximo paso lógico: [qué sigue]
```

---

*Generado en la sesión fundacional. Actualizar cuando cambie la estructura del sistema.*