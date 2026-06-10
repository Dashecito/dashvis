# Dashvis — Vision

> The DNA of the project. Changes rarely — only when the direction, priorities, or identity of Dashvis changes.  
> For the project's operational state, see `project-log.md`. For the technical architecture, see `architecture.md`.

---

## 1. The project

Building an advanced home automation assistant for a room in Benidorm (Valencia, Spain). The goal is twofold: build the system **and** learn in the process. This is not a project where a model programs everything — it is an engineering project where the owner gains real knowledge of systems architecture, IoT, networks, signals, and programming by building each component.

### In one sentence

> A home automation system with a central AI that controls the room, has its own personality, and learns from the user — built with real hardware and custom software.

---

## 2. Dashvis intent

Dashvis is not Alexa or Siri. The differences are deliberate and define the direction of the entire project.

**What Dashvis is:**
- An assistant with a life of its own — internal state, emotions, proactive behavior between interactions
- A system that converges voice, vision, home automation, and robotics into a coherent architecture, not disconnected modules
- A real visual presence in the room, not just invisible backend
- A system that learns from the user over time and remembers between sessions
- A project the owner understands because they built it piece by piece

**What Dashvis is not:**
- A voice wrapper over a cloud API with no real control
- A system where AI makes all the decisions (local heuristics handle the predictable)
- A closed project — it is modular and expandable by design
- A system that depends on internet to function in its essential capabilities

**The original intentions in the owner's words:**
- "I want a Jarvis-style home assistant, but modular and expandable"
- "I don't want to depend on AI to program everything; I want to learn while building"
- "The system should use local heuristics to save tokens and scale AI use only when needed"
- "The visual representation of the assistant matters — it's not just backend"
- "I want the robot, home automation, voice, and vision to converge into a coherent architecture"

---

## 3. Learning philosophy

**Core rule:** the owner implements before receiving the solution.

The process always follows this order:

1. Claude explains the concept and the why
2. The owner implements it
3. Claude reviews and gives feedback
4. If blocked: minimum hint, not the full solution

**What never happens:**
- Giving finished code without prior understanding
- Skipping steps "to move faster"
- Using tools as black boxes — without grasping the concepts they abstract

> Clarification: "understanding what a tool does internally" means understanding *what* it does and *why* — what MQTT guarantees, what a GPIO pin is, what a sensor measures — not reimplementing its internals. A tool like ESPHome that generates the low-level code is fully compatible with this rule, as long as the concepts underneath it are understood. The goal is comprehension, not manual reimplementation.

**Why this approach works:**  
Every block the owner builds teaches a different domain. An ESP32 teaches signals and hardware. A REST API teaches networks and protocols. ROS2 teaches distributed systems. By the end of the project, the owner can maintain, debug, and extend the system without depending on anyone.

---

## 4. Architecture decisions and reasoning

Each decision includes the alternative considered and the reason for the choice. Changing any of them requires updating this file.

### 4.1 LLM + local heuristics router (not pure LLM)

Simple commands ("turn on the light", "raise the blind") don't need a model with hundreds of billions of parameters. The router classifies first with local rules and only escalates to the LLM when confidence is low or the query is complex. Reduces cost, latency, and internet dependency simultaneously.

### 4.2 Concurrent mode as an early architecture decision

Dashvis doesn't say "executing..." and go silent. It responds immediately and executes in parallel. This requires async design from Phase 1 — it cannot be added as a later layer without rewriting the control logic.

### 4.3 Own life as a state machine, not as a prompt

The assistant has an internal state (mood, energy level, active/passive mode) that changes based on time, events, and interactions. This goes beyond including "be friendly" in the system prompt — it is a persistent state that affects how it responds and what it does proactively between interactions.

### 4.4 Local wake word (not cloud)

**Chosen:** openWakeWord or Porcupine, running on RPi.  
**Rejected:** Alexa's wake word or any cloud service.  
**Reason:** privacy (audio doesn't leave the room until the wake word activates), latency (instantaneous), full offline operation.

### 4.5 Servo on physical switch (not smart switch)

**Chosen:** servo motor pressing the existing switch button, controlled by ESP32.  
**Rejected:** replacing the switch with a smart one (Shelly, Sonoff, etc.).  
**Reason:** no electrical work required, 100% reversible, eliminates risk of tampering with wiring. Cardboard prototype allows testing mechanics before installing in production.

### 4.6 Home Assistant as home automation orchestrator (not custom)

**Chosen:** Home Assistant on RPi as the device hub.  
**Rejected:** custom code to manage all devices.  
**Reason:** HA has native support for Zigbee/Z-Wave/MQTT, web UI, automations, Alexa integration, and a large community. The custom AI assistant connects to HA via API/MQTT — it does not replace it.

### 4.7 Alexa as peripheral, not as brain

Echo devices are used as quality microphones and speakers throughout the room. The custom LLM decides and responds. This preserves the hardware investment without giving control to Amazon. The user speaks to Alexa; Dashvis responds.

### 4.8 ROS2 for the robot (not custom framework)

**Chosen:** ROS2 Humble + rclpy (Python).  
**Reason:** industry standard, mature driver and package ecosystem, node architecture that fits the required modular design. The learning curve is real but knowledge is fully transferable to other robotics projects.

### 4.9 WebRTC for FPV video (not RTSP or HLS)

| Protocol   | Typical latency |
|------------|-----------------|
| WebRTC     | 50–150 ms       |
| RTSP       | 2–5 s           |
| HTTP MJPEG | > 1 s           |
| HLS        | > 5 s           |

WebRTC is the only option with realistic sub-150 ms latency. Works natively in any browser. Knowledge gained is reusable for audio streaming, datachannel, and future use cases.

### 4.10 ChromaDB for memory (not relational database)

The assistant's memory must be retrievable by meaning ("when was the last time I studied for more than 3 hours straight?"), not by exact key. Embeddings allow semantic search. ChromaDB is local, Python-native, and requires no external server.

### 4.11 MediaPipe Face Mesh for DMS (not cloud camera)

**Chosen:** MediaPipe locally, without sending video to any service.  
**Reason:** critical privacy. Room video never leaves the device. MediaPipe runs in real time on modest CPU. The 468 facial landmarks are sufficient to calculate PERCLOS, gaze score, and head pose deviation.

### 4.12 Python as the main language

Python for everything except the ESP32 layer, which is declared in ESPHome's YAML config rather than written in code — ESPHome generates the underlying Arduino C++, with hand-written C++ reserved only for the occasional custom component. ROS2 supports Python via rclpy. The AI/ML, audio, vision, and networking ecosystem is the best available in Python. Prototyping speed compensates for the performance difference vs other languages for this use case.

---

## 5. Non-negotiable constraints and principles

1. **No touching electrical wiring.** All physical actuators interact with devices in a non-destructive and reversible way.
2. **Local-first.** Processing of voice, vision, and sensitive data happens on local hardware. The cloud is optional and activated explicitly.
3. **Modular by design.** Each component can be replaced without affecting the rest. Interfaces between layers are explicit: MQTT topics, REST endpoints, ROS2 topics. The same decoupling lets a component *leave* the system, not just be swapped inside it — see §6.
4. **The owner understands what they build.** No advancing without understanding. Learning speed takes priority over build speed.
5. **Privacy.** Camera video and microphone audio never leave the local system unless explicitly required and accepted.

---

## 6. Derivability and portability

Principle 3 (modularity) is internal: any layer can be swapped without breaking the rest. Derivability extends that outward — the same explicit interfaces (MQTT topics, REST endpoints, ROS2 topics) plus the function-organized repo (`architecture.md §4`) mean a component can *leave* Dashvis without being rewired.

This is a property of the structure, **not a fixed list of things Dashvis must do**. It holds as long as two conditions stay true: modules keep talking through their interfaces instead of reaching into each other's internals, and no future tool is hard-wired in as a dependency (see the stack table's "working hypothesis" note in `architecture.md §2`). Nothing below has to be anticipated or built in advance — these are directions the structure leaves open, not commitments.

Three directions it enables:
- **Extract** — lift one module out and run it as a standalone tool.
- **Compose** — combine a minimal subset into a smaller "portable Dashvis".
- **Seed** — use any component as the starting point of a separate project.

Illustratively, not prescriptively: the perception + data layers could become a standalone study-analytics tool (attention / PERCLOS metrics logged over time), the voice pipeline could be reused in another project, or the automation layer could run on its own.

**Honest scope.** Leaf modules (perception, automation, data) extract most cleanly. The brain carries more Dashvis-specific state — own life, memory orchestration, concurrent mode — so anything derived from it inherits more of Dashvis's identity. That is expected, not a defect: the further a component sits from the brain, the more cleanly it travels.

---

*Generated in the founding session. Next revision: if the project direction changes.*