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
| Intent router | Classifies each input across three rungs: heuristic → local SLM → large LLM, by complexity and by which tier is live | Planned |
| Local heuristics | Simple commands, regex, rules — no token cost (local flow) | Planned |
| Local SLM | Small model (~1–3 B) on Tier 1 for offline linguistic continuity — optional | Planned |
| LLM (API / heavy) | Complex natural language, reasoning — Tier 2 only; may be third-party flow | Planned |
| TTS | Voice synthesis for output responses | Planned |
| Concurrent mode | Speaks while executing (asyncio / threads) | Planned |
| Own life | State machine: mood, energy, proactivity. Minimal identity persists 24/7 on Tier 1; heavy proactivity on Tier 2 | Planned |
| Long-term memory | RAG over ChromaDB on Tier 2; recent-context cache on Tier 1; reconcile on PC wake | Planned |

### 1.2 Perception

| Component | Detail | Status |
|-----------|--------|--------|
| Voice | Lavalier mic (shirt) or fixed array. Local wake word. STT via Whisper (Tier 2). | Planned |
| Voice satellite | Reused old smartphone as WiFi/IP mic — Phase 2, zero-cost test rig before dedicated hardware. | Planned |
| Vision + DMS | Cameras. MediaPipe Face Mesh (Tier 2). Metrics: PERCLOS, gaze score, head pose. Threshold: 30 s distraction → alert. | Planned |
| Radio telemetry | RTL-SDR on RPi 3B+, **receive-only**. SpyServer streams spectrum over WiFi 5 GHz to Tier 2. Public signals (NOAA APT weather, ADS-B). The device is a neutral RF project outside the tree; only its reduced telemetry enters Dashvis via MQTT (see `vision.md §6`). | Planned |
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
| Physical actuators | Servo + ESP32 (flashed with ESPHome). Presses existing switch button. No electrical wiring. | Planned |
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
| Persistent memory | Local ChromaDB (Tier 2). RAG. Semantic search over history and preferences. | Planned |
| External telemetry | Receive-only nodes (e.g. SDR) publish reduced readings via MQTT. Captured raw, interpreted downstream, reusable/reinterpretable. | Planned |
| Egress governance | Two flows: local (open) / third-party (closed by default, opened per function, minimum, logged). Sovereign backup only to owner-controlled targets. See `vision.md §7`. | Planned |
| Token management | Heuristics capture ~70-80% of commands. LLM context compressed. | Planned |

### 1.7 Deployment topology (three compute tiers)

The logical hub-and-spoke (§1) is unchanged; this maps those layers onto physical hosts. The mapping is loose by design — tiers talk only through MQTT/sockets, so any layer can move host without code changes (see `vision.md §4.13` and `vision.md §6`). **Tiers below are roles; the device named is the current assignment, swappable (see Mobility).**

```
Tier 1 — Autonomous core      always-on (role)     now: in-room RPi
  Home Assistant · Mosquitto (MQTT) · fast local heuristics · optional local SLM
  · minimal own-life identity · recent-context cache.
  Guarantee: the room stays functional with no PC and no internet.

Tier 2 — AI muscle            on-demand (role)     now: main PC / laptop
  Vision/DMS (MediaPipe) · local STT (Whisper) · vector memory (ChromaDB)
  · large-LLM side of the brain. Publishes percepts/decisions to Tier 1 via MQTT.

Tier 3 — Remote perception    single-task          satellite devices
  · Voice satellite: reused smartphone as WiFi/IP mic (Phase 2).
  · Radio/telemetry node: RTL-SDR on RPi 3B+, receive-only, SpyServer → Tier 2.
  · ESP32 actuator/sensor nodes, flashed with ESPHome (Phase 3).
```

**Mobility — nodes are discovered, not wired.** Tiers are *roles*, hosts are *assignments*: the RPi holds Tier 1 today, but any always-on host can, and one capable host can hold several roles at once (a laptop as Tier 1 + Tier 2 = a portable Dashvis to demo elsewhere, without taking the home RPi). No hostname or path is hard-coded; a node announces itself on the bus and is consumed by topic, not by address. **Rule of thumb:** if you're about to write a device path or literal IP in a module, stop and put it in config (`.env`). Moving the SDR, swapping the RPi for a laptop, or re-hosting a layer is plug-in-and-appear, not reconfigure — the deployment face of derivability (`vision.md §6`, principle 8). What stays fixed is the *interface*, not the *box*.

**Graceful degradation** — behaviour is defined by which tier *roles* are filled, never assuming all are:

```
Tier 1 up + Tier 2 up   →  full Dashvis: voice, vision/DMS, deep memory, large-LLM
                           reasoning, proactive own-life.
Tier 1 up + Tier 2 down →  autonomous room: HA automations, MQTT, heuristic/SLM
                           voice→action, minimal identity continuity. No heavy AI,
                           no vision, no deep retrieval.
Tier 1 down             →  no always-on core present: the room's core guarantee pauses
                           until some host takes the Tier-1 role again. Not a crash —
                           Dashvis is portable and re-instantiates on another host.
```

The brain's three rungs (`vision.md §4.14`) make the middle row a gradient, not a cliff: without a Tier-2 host, heuristics still act and the optional local SLM still speaks — less eloquent, not mute. (A single powerful host holding both roles collapses the first two rows into one: the "Tier 2 up, Tier 1 down" case isn't a state — whoever runs Tier 2 can also run Tier 1.)

---

## 2. Technology stack

Each technology in this table is a working hypothesis, not a commitment. It is confirmed or replaced when the phase that requires it is actually worked on. Changing one tool does not break the project: layers communicate through explicit interfaces (MQTT topics, REST endpoints, ROS2 topics), not through direct tool dependencies.

```
Layer               Chosen technology          Rejected alternatives
──────────────────────────────────────────────────────────────────────
LLM                 Claude API / GPT-4o        Local Ollama (lower quality)
Local SLM           Llama 3.2 3B / Phi-3       (optional Tier-1 rung)
Heuristics          Python regex + rules       spaCy lightweight NLP
Wake word           openWakeWord               Porcupine (more accurate, paid)
STT                 Whisper local              Deepgram / Whisper API (cloud)
TTS                 edge-tts / ElevenLabs      Coqui (local, lower quality)
Vector DB           ChromaDB                   Pinecone (cloud), Qdrant
IoT hub             Home Assistant + RPi       OpenHAB, Node-RED
IoT protocol        MQTT (Mosquitto)           CoAP, HTTP polling
Microcontroller     ESP32                      Arduino Nano, RPi Pico
MCU firmware        ESPHome (YAML)             Arduino C++, MicroPython
Vision              OpenCV + MediaPipe         dlib, InsightFace
Robot OS            ROS2 Humble (rclpy)        custom framework
Video stream        WebRTC                     RTSP, HLS
Event bus           Redis Pub/Sub              RabbitMQ, ZeroMQ
Containers          Docker + Compose           systemd units
Main hardware       Raspberry Pi 4/5           NVIDIA Jetson (high cost)
```

> Out-of-tree tooling — RTL-SDR + SpyServer for the radio node, and the Alfa adapter used by the separate RF/networks learning project — is **not** part of the Dashvis core stack. Only the reduced telemetry such nodes publish enters Dashvis, via MQTT (see §1.2, §1.6 and `vision.md §6`).

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

### Phase challenge structure

Challenges are not fixed in advance. They are generated when creating each phase brief, calibrated to the owner's actual level at that point. The structure is always the same:

- **Mini-challenges**: one per skill area of the phase. Calibrated after level questions at the start of the brief.
- **Integrator challenge**: a functional artifact that combines all the phase's skills.
- **Extension challenge** *(optional)*: to go deeper if the phase is completed ahead of schedule.

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
You'll learn: GPIO/ADC/PWM (conceptual), ESPHome (YAML config) as the primary flow, MQTT (pub/sub, QoS, retain), servos, Wi-Fi/OTA. Arduino C++ at reading level only — enough to understand what ESPHome generates, debug it, and write the occasional custom component, not a primary skill to develop.  
You'll build: ESP32 (flashed with ESPHome) + servo on blind switch, end-to-end voice control.

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

This function-first layout is also what makes the system **derivable** (`vision.md §6`): because each module lives in its own folder behind an explicit interface, it can be lifted out as a standalone tool or copied into a separate project without dragging the rest of Dashvis with it. The repo structure is the enabler; the principle is the intent.

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

**Mini-challenges** → always to `scratch/phase_N/`. They are calibrated exercises to acquire domain skills. Historical reference, never production.

**Integrator challenge** → the culmination of the mini-challenges, combining all phase skills into a functional artifact. For Phases 1–7, that artifact IS the Dashvis component described by "You'll build" — it goes to its architectural folder. For Phase 0, even the integrator challenge is an exercise (the TCP server is not a Dashvis component) — it goes to scratch.

**Phase 0 is the full exception**: nothing built in this phase is a Dashvis component. Everything goes to `scratch/phase_0/`.

```
Phase 1 example:
  scratch/phase_1/
    http_basics.py     ← mini-challenge: learning HTTP
    auth_test.py       ← mini-challenge: learning authentication

  brain/
    router.py          ← integrator challenge = You'll build: LLM wrapper + heuristic/AI router
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
Integrator challenge of each phase IS the component — goes to its architectural folder.
Phase 0: everything goes to scratch, nothing is a Dashvis component yet.

THIS SESSION — Phase N: [Name]
You'll learn: [phase skill list]
You'll build: [build target]
Mini-challenges: [generated in this brief after level calibration]
Integrator challenge: [generated in this brief]

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