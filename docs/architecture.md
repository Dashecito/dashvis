# Dashvis — Architecture

> How the system is organized. Changes when the structure, protocols, or layer responsibilities change.  
> For the why behind decisions see `vision.md`. For the current state see `project-log.md`.

---

## 1. System layers

Hub-and-spoke architecture: the central brain orchestrates the five modules, each connected directly to it. Modules do not communicate with each other — all flow goes through the brain or, from Phase 7 onwards, through the event bus.

```
┌─────────────────────────────────────────────────────────────────┐
│                       CENTRAL BRAIN                             │
│  LLM · local heuristics · TTS · concurrent mode                │
│  own life · emotions · proactive behavior · long-term memory   │
└─────────────────────────────────────────────────────────────────┘
   ↑ input        ↓ output      ↕ control    ↕ control    ↕ service
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│PERCEPTION│  │  VISUAL  │  │AUTOMATION│  │  ROBOT   │  │   DATA   │
│          │  │  OUTPUT  │  │          │  │          │  │          │
│Voice     │  │Projectors│  │ESP32     │  │ROS2      │  │Sheets    │
│Vision+DMS│  │Touch     │  │HA + MQTT │  │WebRTC    │  │Vector DB │
│Telemetry │  │Avatar    │  │Actuators │  │Gamepad   │  │Tokens    │
└──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘

↑  input     module sends data to the brain (sensors, signals, telemetry)
↓  output    brain directs module unidirectionally; no relevant state returned
↕  control   brain sends commands; module returns real state
↕  service   DATA is not a peer module — it is transversal infrastructure.
             The brain reads and writes here; other modules also produce
             data stored here (logs, metrics, session context).
```

> **Current state:** the entire system is in the planning phase. No layer has real implementation yet. The sections below describe the target design, not what has been built.

---

### 1.1 Central brain

The system's core. Receives all perception, makes decisions, generates responses, and orchestrates actuators.

| Component | Responsibility | Status |
|-----------|---------------|--------|
| Intent router | Classifies each input: local heuristic or LLM | Planned |
| Local heuristics | Simple commands, regex, rules — no token cost | Planned |
| LLM API | Complex natural language, reasoning | Planned |
| TTS | Voice synthesis for output responses | Planned |
| Concurrent mode | Speaks while executing (asyncio / threads) | Planned |
| Own life | State machine: mood, energy, proactivity | Planned |
| Long-term memory | RAG over ChromaDB, semantic retrieval | Planned |

### 1.2 Perception

| Component | Detail | Status |
|-----------|--------|--------|
| Voice | Lavalier mic (shirt) or fixed array. Local wake word. STT via Whisper/cloud. | Planned |
| Vision + DMS | Cameras. MediaPipe Face Mesh. Metrics: PERCLOS, gaze score, head pose. Threshold: 30 s distraction → alert. | Planned |
| Telemetry | Screen time from laptop and phone via OS API. | Planned |

### 1.3 Visual output

| Component | Detail | Status |
|-----------|--------|--------|
| Mini projectors | XGIMI / Anker Capsule / BenQ. Distributed by zone. | Planned |
| Touch surface | Overlay on projection via IR frame or Ultraleap. | Planned |
| Avatar | Visual representation on TV or projector. Expresses emotional states. | Planned |

### 1.4 Automation

| Component | Detail | Status |
|-----------|--------|--------|
| Physical actuators | Servo + ESP32. Presses existing switch button. No electrical wiring. | Planned |
| Local orchestrator | Home Assistant on RPi. MQTT as message bus. | Planned |
| Ecosystem | Alexa as peripheral (mic/speaker). Zigbee/Z-Wave managed by HA. | Planned |

### 1.5 Robot

| Component | Detail | Status |
|-----------|--------|--------|
| Hardware | Mobile chassis. Modular arms. Designed to add components over time. | Planned |
| Control + camera | Bluetooth gamepad. FPV camera via WebRTC. Latency < 150 ms. | Planned |
| Software | ROS2 Humble. One node per joint. OTA plugins. | Planned |

### 1.6 Data

| Component | Detail | Status |
|-----------|--------|--------|
| External sources | Google Sheets and Excel via API. Read and write. | Planned |
| Persistent memory | Local ChromaDB. RAG. Semantic search over history and preferences. | Planned |
| Token management | Heuristics capture ~70-80% of commands. LLM context compressed. | Planned |

---

## 2. Technology stack

Each technology in this table is a working hypothesis, not a commitment. It is confirmed or replaced when the phase that requires it is actually worked on. Changing one tool does not break the project: layers communicate through explicit interfaces (MQTT topics, REST endpoints, ROS2 topics), not through direct tool dependencies.

```
Layer               Chosen technology          Rejected alternatives
──────────────────────────────────────────────────────────────────────
LLM                 Claude API / GPT-4o        Local Ollama (lower quality)
Heuristics          Python regex + rules       spaCy lightweight NLP
Wake word           openWakeWord               Porcupine (more accurate, paid)
STT                 Whisper local              Deepgram / Whisper API (cloud)
TTS                 edge-tts / ElevenLabs      Coqui (local, lower quality)
Vector DB           ChromaDB                   Pinecone (cloud), Qdrant
IoT hub             Home Assistant + RPi       OpenHAB, Node-RED
IoT protocol        MQTT (Mosquitto)           CoAP, HTTP polling
Microcontroller     ESP32                      Arduino Nano, RPi Pico
Vision              OpenCV + MediaPipe         dlib, InsightFace
Robot OS            ROS2 Humble (rclpy)        custom framework
Video stream        WebRTC                     RTSP, HLS
Event bus           Redis Pub/Sub              RabbitMQ, ZeroMQ
Containers          Docker + Compose           systemd units
Main hardware       Raspberry Pi 4/5           NVIDIA Jetson (high cost)
```

---

## 3. Phase roadmap

Phases 0–2 are sequential: everything else depends on them as foundation.  
From Phase 3 onwards, robot (Phase 6) can advance in parallel with automation (Phases 3–5).

| Phase | Title | Domain | Enables in the system |
|-------|-------|--------|-----------------------|
| 0 | Environment & fundamentals | Base | All infrastructure |
| 1 | APIs & architecture | AI / Backend | Central brain |
| 2 | Voice & signals | Audio | Voice input + TTS |
| 3 | IoT & ESP32 | Hardware / IoT | Automation: blinds, lights |
| 4 | Computer vision | Computer Vision | DMS: study monitoring |
| 5 | Networks & protocols | Networking | FPV robot + service integration |
| 6 | Robotics & ROS2 | Robotics | Robot with arms and camera |
| 7 | Full integration | Architecture | Complete Dashvis system |

### Phase reto structure

Retos are not fixed in advance. They are generated when creating each phase brief, calibrated to the owner's actual level at that point. The structure is always the same:

- **Mini-retos**: one per skill area of the phase. Calibrated after level questions at the start of the brief.
- **Integrator reto**: a functional artifact that combines all the phase's skills.
- **Extension reto** *(optional)*: to go deeper if the phase is completed ahead of schedule.

### Phase detail

**Phase 0 — Environment & fundamentals** *(2–3 weeks)*  
You'll learn: Linux CLI, Python, Git, basic networking (IP, ports, SSH, DNS, NAT).  
You'll build: RPi accessible via SSH, CPU/RAM monitoring script with CSV alerts.

**Phase 1 — APIs & architecture** *(3–4 weeks)*  
You'll learn: HTTP/REST, authentication (API keys, Bearer, OAuth), client-server architecture, async/await, rate limiting.  
You'll build: LLM API wrapper with heuristic/AI router, latency and cost measurement per route.

**Phase 2 — Voice & signals** *(3–4 weeks)*  
You'll learn: audio signals (PCM, sample rate, WAV), real-time streams, wake word, STT, TTS, WebSockets.  
You'll build: full pipeline wake word → STT → LLM/heuristic → TTS with latency < 2 s.

**Phase 3 — IoT & ESP32** *(4–5 weeks)*  
You'll learn: GPIO/ADC/PWM, Arduino C++, MQTT (pub/sub, QoS, retain), servos, Wi-Fi/OTA.  
You'll build: ESP32 + servo on blind switch, end-to-end voice control.

**Phase 4 — Computer vision** *(3–4 weeks)*  
You'll learn: OpenCV, MediaPipe Face Mesh (468 landmarks), gaze and pose estimation, DMS metrics.  
You'll build: active DMS system — alerts after 30 s of distraction while studying.

**Phase 5 — Networks & protocols** *(3–4 weeks)*  
You'll learn: TCP vs UDP, WebRTC (ICE/STUN/RTCPeerConnection), latency/jitter, TLS, pub/sub vs req-response.  
You'll build: WebRTC video stream to browser with visible latency and automatic reconnection.

**Phase 6 — Robotics & ROS2** *(6–8 weeks)*  
You'll learn: ROS2 (nodes/topics/services/actions), basic PID, kinematics, serial RPi↔MCU, joy package.  
You'll build: 3+ DOF arm controlled by gamepad + WebRTC camera, modular architecture.

**Phase 7 — Full integration** *(4–6 weeks)*  
You'll learn: event-driven (Redis Pub/Sub), service discovery (mDNS), fallbacks, Docker/Compose, structured logging.  
You'll build: complete integrated system with central event bus.

---

## 4. Repository structure

The repository organizes code by **what it does**, not by when it was learned. Phases are a learning structure; the repo is a system structure.

```
dashvis/
├── docs/             ← vision.md, architecture.md, project-log.md, devlog.md
├── scratch/          ← learning exercises per phase, never go to production
│   ├── phase_0/
│   ├── phase_1/
│   └── ...
├── brain/            ← LLM router + heuristics (appears in Phase 1)
├── perception/       ← voice, vision, DMS, telemetry (Phases 2 and 4)
├── automation/       ← ESP32, HA, MQTT, actuators (Phase 3)
├── robot/            ← ROS2, WebRTC, gamepad (Phases 5 and 6)
└── data/             ← ChromaDB, Sheets, memory (Phase 1 onwards)
```

### Rules

- `scratch/phase_N/` exists from the start of each phase and is archived when it ends.
- System folders are created when that module is built, not before.
- Docs live at repo root and are versioned alongside code.

### How code moves to production

The single question that determines where code goes: **is this code a Dashvis component, or is it an exercise to learn how to build it?**

- Dashvis component → architectural folder
- Learning exercise → `scratch/phase_N/`

Applied to the output types of each phase:

**Mini-retos** → always to `scratch/phase_N/`. They are calibrated exercises to acquire domain skills. Historical reference, never production.

**Integrator reto** → the culmination of the mini-retos, combining all phase skills into a functional artifact. For Phases 1–7, that artifact IS the Dashvis component described by "You'll build" — it goes to its architectural folder. For Phase 0, even the integrator reto is an exercise (the TCP server is not a Dashvis component) — it goes to scratch.

**Phase 0 is the full exception**: nothing built in this phase is a Dashvis component. Everything goes to `scratch/phase_0/`.

```
Phase 1 example:
  scratch/phase_1/
    http_basics.py     ← mini-reto: learning HTTP
    auth_test.py       ← mini-reto: learning authentication

  brain/
    router.py          ← integrator reto = You'll build: LLM wrapper + heuristic/AI router
```

> This structure must be included in all briefs so any working session knows exactly where to put code.

---

## 5. Portable context system

To work on a phase in a separate conversation and come back with the output, two templates are used. At any time, ask "give me the brief for Phase N" and it will be generated ready to paste.

### 5.1 Session brief

Generated in the main conversation and pasted as the first message in the working session.

```
DASHVIS PROJECT BRIEF — Phase N: [Name]
════════════════════════════════════════════════════════════════
PROJECT
Home automation assistant with central AI. Hub-and-spoke
architecture: central brain (LLM + heuristics + own life)
connected to 5 modules — perception (voice/vision/telemetry),
visual output (projectors/touch/avatar), automation (ESP32/HA/MQTT),
robot (ROS2/WebRTC/gamepad), data (VectorDB/Sheets).
Stack: Python · Raspberry Pi · ESP32 · Home Assistant · MQTT.
Philosophy: explain the concept, I implement, minimum hint if
I get stuck. No finished code without prior understanding.

PROJECT STATE
[Paste current content of project-log.md]

REPO STRUCTURE
dashvis/
├── docs/
├── scratch/
│   └── phase_N/      ← exercises for this phase (not production)
[existing system folders — only those already created]
Rule: exercises → scratch/phase_N/ · Dashvis components → architectural folder
Integrator reto of each phase IS the component — goes to its architectural folder.
Phase 0: everything goes to scratch, nothing is a Dashvis component yet.

THIS SESSION — Phase N: [Name]
You'll learn: [phase skill list]
You'll build: [build target]
Mini-retos: [generated in this brief after level calibration]
Integrator reto: [generated in this brief]

TODAY'S TASK
[What you want to work on specifically in this session]
════════════════════════════════════════════════════════════════
```

### 5.2 Session return

Pasted in the main conversation when coming back, to update `project-log.md`.

```
RETURN PHASE N: [Name]
Status: ✅ Completed / 🔄 In progress / 🚧 Blocked at [point]

Decisions made:
- Chose X over Y because [brief reason]

Artifacts produced:
- file.py: [what it does in one line]

Concepts I understand well: [list]
Open questions: [if any]
Next logical step: [what follows]
```

---

*Generated in the founding session. Update when the system structure changes.*