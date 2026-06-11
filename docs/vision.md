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

**Under the tier model (§4.13):** this state splits by what it costs to run. The *minimal identity* — current mood/energy, last interaction, who the user is, recent context thread — persists 24/7 on Tier 1 (the always-on RPi). The *heavy proactive reasoning* runs on Tier 2 (the PC). The analogy is Jarvis inside the suit versus the mansion: without the PC, Dashvis keeps its identity and continuity (it is still itself, recognises the user, holds its character) but loses heavy capability. Proactivity without the PC is minimal and rule- or SLM-driven (e.g. "it's 2 a.m., lower the lights?"), never large-model conversation. Identity is the floor; capability scales with whichever tiers are on.

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

**Under the tier model (§4.13):** the full semantic store lives on Tier 2 (the PC). A small *recent-context cache* persists on Tier 1 so the always-on core keeps short-term continuity offline; the two reconcile when the PC wakes. Memory therefore degrades gracefully — recent context is available without the PC, deep retrieval over the whole history needs Tier 2. The store stays local-first; any replication of it follows the data-flow rules in §7 (owner-controlled destinations only).

### 4.11 MediaPipe Face Mesh for DMS (not cloud camera)

**Chosen:** MediaPipe locally, without sending video to any service.  
**Reason:** critical privacy. Room video never leaves the device. MediaPipe runs in real time on modest CPU. The 468 facial landmarks are sufficient to calculate PERCLOS, gaze score, and head pose deviation.

### 4.12 Python as the main language

Python for everything except the ESP32 layer, which is declared in ESPHome's YAML config rather than written in code — ESPHome generates the underlying Arduino C++, with hand-written C++ reserved only for the occasional custom component. ROS2 supports Python via rclpy. The AI/ML, audio, vision, and networking ecosystem is the best available in Python. Prototyping speed compensates for the performance difference vs other languages for this use case.

### 4.13 Hybrid compute tiers (not single host)

**Chosen:** three compute tiers connected only by MQTT/sockets — an always-on core (Tier 1, currently an in-room RPi), heavy AI on demand (Tier 2, PC), and remote single-task nodes (Tier 3).  
**Rejected:** running everything on one host. A single RPi cannot run Whisper + MediaPipe + an LLM at once while still guaranteeing 24/7 basic operation; a PC-only design loses the always-on floor whenever the PC sleeps.  
**Reason:** separates the *always-on guarantee* (cheap, local, on Tier 1) from *heavy capability* (expensive, on-demand, on Tier 2). Because tiers talk only through clean network interfaces, any layer can move host without code changes — principle 3 / §6 (derivability) applied to deployment. This also corrects a latent sizing debt in the original design, which implicitly placed the whole brain on the RPi before anyone measured that it could not carry that load. **Tiers are *roles*, not fixed devices:** the RPi is the current Tier-1 assignment for the primary use case, but any always-on host can hold the role, and one capable host can hold several roles at once (a laptop running Tier 1 + Tier 2 = a portable Dashvis for a demo elsewhere). What must never happen is a module hard-coding a host (principle 8). The full host mapping and the degradation behaviour live in `architecture.md §1.7`.

### 4.14 Three-rung brain with an optional local SLM (not heuristics-only, not always-LLM)

**Chosen:** the intent router (§4.1) escalates across three rungs — local heuristics → a small local model (SLM, ~1–3 B params) → a large LLM — choosing by query complexity *and* by which tier is currently alive.  
**Rejected:** heuristics-only (too rigid the moment the PC is off) and always-large-LLM (cost, latency, hard cloud dependence even for trivial commands).  
**Reason:** turns graceful degradation into a gradient of *eloquence* rather than an on/off of capability. The SLM is *optional* — if Tier 1 hardware can't host it, the system falls back to heuristics and nothing breaks. The large LLM (external API or heavy local model) runs only on Tier 2. The chosen rung also interacts with the data-flow rules (§7): heuristics and the local SLM are local flow; the large LLM may be third-party flow.

---

## 5. Non-negotiable constraints and principles

1. **No touching electrical wiring.** All physical actuators interact with devices in a non-destructive and reversible way.
2. **Local-first.** Processing of voice, vision, and sensitive data happens on local hardware. The cloud is optional and activated explicitly.
3. **Modular by design.** Each component can be replaced without affecting the rest. Interfaces between layers are explicit: MQTT topics, REST endpoints, ROS2 topics. The same decoupling lets a component *leave* the system, not just be swapped inside it — see §6 (derivability).
4. **The owner understands what they build.** No advancing without understanding. Learning speed takes priority over build speed.
5. **Privacy.** Camera video and microphone audio never leave the local system unless explicitly required and accepted.
6. **Graceful degradation.** The room never depends on the PC or the cloud to keep working. Capability scales with whichever compute tiers are on, and the always-on core (Tier 1) is the floor — below it the system is down by design. See §4.13 and `architecture.md §1.7`.
7. **Data sovereignty and minimization.** Two egress flows: *local* (anything staying on hardware the owner controls — open, the floor) and *third-party* (anything crossing to something the owner does not control — closed by default). The third-party flow opens only per function, carrying the minimum necessary, in the most reduced form, and it is logged. Raw audio and video never cross; only their reduced derivatives, and only when a function justifies it. See §7 (data flows).
8. **No hardcoded host assumptions.** Tiers are roles; hosts are assignments. Device paths, IPs and hostnames live in config (`.env`), never in module code. Rule of thumb: if you're about to type a device path or literal IP into a module, stop and put it in config. This is what keeps the system portable across devices (`architecture.md §1.7`).

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

**Neutral by construction.** A seed carries no purpose-label from Dashvis. The same primitives — capturing signals, raising interfaces, moving data — are neither defensive nor offensive in themselves; a derivative can pivot to whatever its own terms require without Dashvis having pre-marked it. Concretely, the RTL-SDR radio node is a separate, neutral RF project: the *device* and its raw spectrum capture live outside the Dashvis tree, while the *telemetry it produces* (timestamped, reduced readings) enters Dashvis through the data layer like any other percept. Dashvis consumes the telemetry; it does not own the SDR. Being fundamental to a feature ("close the blind, a storm is coming") does not pull the device inside — what Dashvis depends on is a data flow on an interface, not the apparatus. Swap the SDR for a weather API and Dashvis never notices. The node captures raw and lets interpretation happen downstream, so the same recording can be reinterpreted later for a different purpose without recapturing.

**Coupling in is the mirror of deriving out.** The same decoupling that lets a module *leave* also bounds how a new source or tool *joins*, in three bands:
- **Connect / ingest — automatic.** A new node publishes on a topic and is discovered (`architecture.md §1.7`); its data lands in the data layer, timestamped and reusable. Nothing is restructured to *receive* it.
- **Extend / interpret — a bounded, authored act (not a rewrite).** Giving that data meaning is a new *consumer* behind the same interface, plus, if it crosses to a third party, opening its door under §7. Whatever you add — an SDR feed, a tool Dashvis reasons over as a "companion", a new sensor — the shape is always the same: write a consumer, authorise the flow. You extend uniformly; you never re-architect.
- **Auto-understand anything — out of scope, on purpose.** A brain that absorbs and interprets any source with no authoring is the over-engineering to avoid, and it would break §7 (availability ≠ permission). The system is prepared for the *act* of coupling, not to perform it unbidden.

Graceful degradation falls out of the same property: because consumers subscribe to topics rather than calling sources directly, a vanished source is *silence on a topic*, not a failed call — there is no hard dependency to throw. A consumer written to treat missing or stale data as a valid state (last-known value, or a clean "can't do that right now") lets the dependent feature go quiet while everything else runs. The plumbing makes this natural; each consumer must honour it. In one line: **connecting is generic, meaning is authored.**

---

## 7. Data flows and sovereignty

This section governs what may leave the owner's hardware and in what form. It refines principles 2 (local-first), 5 (privacy) and 7 (sovereignty/minimization) into one model.

**Two flows, one gate.** The moment any data would leave a device it is on one of two paths:
- **Local flow** — stays on hardware the owner controls (Tier 1/2/3, a NAS, a phone). Open by default, no limit. This is the floor.
- **Third-party flow** — crosses to something the owner does not control (an AI API, a cloud backup). Closed by default.

The decision is made at a single point — the egress boundary — not scattered across every layer. Data moves freely *inside* the system; only when something would cross to a third party does it pass the gate, which asks: which function opens this, and what is the minimum it must carry?

**Minimization by need.** The third-party flow is neither forbidden forever nor allowed wholesale. It opens *per function*: when a concrete feature genuinely requires it, the gate lets through the minimum amount, in the most reduced form, and records which function opened it. By default nothing sensitive crosses — not to a third-party backup, not to an API.

**Reduction before egress.** Raw audio and video never cross the gate. They are reduced to the minimum interpretable form *locally first* — voice transcribed (Whisper, Tier 2), vision turned into metrics (MediaPipe → PERCLOS / gaze, never the face itself), a speaker reduced to a numeric voiceprint rather than a recording. The camera and microphone never touch the cloud; the *numbers* they produce might, under the rules above. The boundary is not *where* something is computed but *in what state of rawness* it crosses.

**Local-first is not local-only (the API tension).** Reasoning and personality may need a large model, and that may be an external API. This is allowed — explicitly, reduced, opt-in — and is not a contradiction with local-first: what goes out is already-reduced text and metrics, never raw capture, never the whole memory store, only the minimal fragment a given query needs. The cloud is an opt-in ceiling, not a default. For the Dashvis core as designed (voice as commands, vision as study-DMS) nothing raw needs to leave at all; raw-to-API is reserved for future *luxury* functions — emotional tone analysis, rich visual scene understanding — each of which would open its own door under minimization-by-need. None are open today.

**Dynamic routing, fixed ceiling.** The brain/router *may* choose local vs third-party flow in the moment, optimising cost, privacy and quality — but only *among doors already authorised*. It decides *when* to use an open door, never *whether* a door exists. The system cannot grant itself a new third-party channel because the tool happens to be present: **availability is not permission** (the same logic the project studies elsewhere — proximity ≠ authentication, encryption ≠ authorization). Doors are opened by the owner, at design time, when a function is built and enabled.

**Sovereign backup.** Replication of sensitive data goes only to destinations the owner controls — physically or by key — over encrypted transport, never to a third party that could read it in clear. The *mechanism* is deliberately left open (SSH-on-arrival, a NAS, a configured phone); the excluded *category* is "third party reading in clear". This is why a private GitHub or Dropbox is out as a backup target: the data would still sit, readable, on someone else's infrastructure.

**No data is "non-sensitive".** Presence and telemetry leak by combination — *when* a light turns on reveals sleep; the spectrum a radio node hears reveals which devices are home and when. So data is not classified by a sensitive / non-sensitive label (the line moves, and almost everything falls to the sensitive side once combined); it is governed by *where it lives and how it travels* — which is exactly what the two flows above encode.

---

*Generated in the founding session. Next revision: if the project direction changes.*