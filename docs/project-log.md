# Dashvis — Project log

> Operational notebook. Answers: "if I resume Dashvis today, exactly where am I?"  
> Updated constantly. For deep context see `vision.md` and `architecture.md`.

---

## Phase status

```
Phase 0 — Environment & fundamentals   [🔄] Brief generated — session in progress (incomplete)
Phase 1 — APIs & architecture          [ ] Pending
Phase 2 — Voice & signals              [ ] Pending
Phase 3 — IoT & ESP32                  [ ] Pending
Phase 4 — Computer vision              [ ] Pending
Phase 5 — Networks & protocols         [ ] Pending
Phase 6 — Robotics & ROS2              [ ] Pending
Phase 7 — Full integration             [ ] Pending
```

**Active phase:** Phase 0

---

## Active session

```
Phase in progress:   Phase 0 — Environment & fundamentals
Session objective:   Finish mini-challenge 2 and CS50P unit 6. 
Last point touched:  CSV files I/O; csv.writer subunit as checkpoint. Gemini conversation ongoing. 
                     Mini-challenge 2.
```

---

## Next steps

1. Complete Phase 0 with Gemini using the generated brief
  - Look for more stats to show in the raspberry and watch for gpu usage comptaibility. And future formatting. 
  - CS50P CSV files is useful now. Consider watching it before going on. 
2. Return to Claude with phase return (partial or complete) to update state

---

## Open questions

Maybe the documents are too defined. Not sure if there is early over-optimization or if they fall into the utopian concept of a "happy idea".

Keep in mind the differentiation between "core funcionality" and "potentially comercializable functionality". Keep the first open source, and the second reserved for comercial licences.  

Candidate *luxury* functions that would each open their own third-party door under `vision.md §7` — none open today, none required by the core: emotional tone analysis from raw audio, rich visual scene understanding from raw frames. Decide per function, if ever.

---

## Recent decisions

- 2026-06-10: Hybrid three-tier model + graceful degradation + three-rung brain
  (vision §4.13–4.14, architecture §1.7).
- 2026-06-10: Data-flow governance — two flows, minimization by need (vision §7).
- 2026-06-10: SDR scoped as external telemetry provider; project stays neutral (vision §6).
- 2026-06-10: MCU path — ESP32 + ESPHome over Arduino C++ / Pico W (vision §4.12, arch §3).
- 2026-06-10: Procurement batch placed; projector + table deferred (see Hardware).
  → Full rationale for all five in devlog (2026-06-10 entries).

- 2026-06-04: Phase 0 setup vs system development conflict — supposedly covered.
  Should be able to continue with Gemini now; it will know what goes to phase_0 and what doesn't based on the brief.

- 2026-06-04: Repo structure defined. Exercises → scratch/phase_N/,
  system modules → domain folders. See architecture.md §4.

Foundational design decisions are in `vision.md §4`.

---

## Hardware

### Core & nodes
Status: `[ ]` to acquire (not ordered) · `[~]` ordered, not yet arrived · `[x]` on hand. Tiers map to `architecture.md §1.7`.

```
Tier 1 — always-on core:
  [x] Raspberry Pi (main, in-room)
  [x] Alexa / Echo (peripheral mic + speaker)

Tier 2 — AI muscle:
  [x] Main PC / laptop

Tier 3 — remote nodes:
  [x] Smartphone — reused as WiFi/IP voice mic (Phase 2)
  [~] USB mic, mini (Phase 2)
  [~] RTL-SDR v5 NESDR SMArt — receive-only, 100 kHz–1.75 GHz, TCXO 0.5 ppm, 3 antennas
  [~] Raspberry Pi 3B+ — SDR host
  [~] Leicke ULL PSU 5V 2.5A — SDR power
  [~] Micro-USB OTG adapter — SDR connectivity
  [~] ESP32-S3 ×3 (1 bare + 2 with expansion/IPEX kit) — Phase 3
  [~] ESP-WROOM-32 ×4 — Phase 3
  [~] WROOM-32U / WROVER ×1, ext. 2.4G antenna — Phase 3
  [~] Camera AZDelivery 5 MP, OV5647, 15 cm flex — Phase 4 vision (architecture §1.2)

Actuation targets (non-destructive, per vision §4.5):
  [~] LED pull-cord lamp, battery — servo-press test target (confirm)

Visual output (architecture §1.3):
  [ ] Projector — deferred; output goes to the monitor for now
  [ ] Extra monitors · monitor arms

Robot (Phase 6):
  [ ] Chassis

Out-of-tree — neutral RF/networks project (couples to Dashvis only as link/telemetry):
  [~] Alfa AWUS036ACHM, 802.11ac long-range

Furniture / staging (not a system component):
  [ ] Folding table + V-groove wheels — may stage the outdoor radio node
```

### Freenove Ultimate Starter Kit  `[x]` on hand
Sensors/modules used with the ESP32 for Phase 3. Pico W (shipped with the kit) lost
and off the critical path — rationale in devlog (2026-06-10, MCU path).

```
Microcontroller (missing):
  Raspberry Pi Pico W ......................... x1   (lost — not planned for repurchase)

Sensors:
  Temperature & Humidity Sensor (DHT) ......... x1
  Thermistor .................................. x1
  Photoresistor ............................... x1
  Infrared Motion Sensor (PIR) ................ x1
  Ultrasonic Ranging Module ................... x1
  Accelerometer Module ........................ x1
  RFID Module ................................. x1

Actuators & motors:
  Servo ....................................... x1
  Stepping Motor .............................. x1
  Stepping Motor Driver ....................... x1
  Motor ....................................... x1
  Relay ....................................... x1
  Motor Driver Chip ........................... x1

Audio:
  Speaker ..................................... x1
  Audio Converter & Amplifier ................. x1
  Passive Buzzer .............................. x1
  Active Buzzer ............................... x1

Displays & visual:
  LCD Module (16x2) ........................... x1
  4-Digit 7-Segment Display ................... x1
  7-Segment Display ........................... x1
  8x8 LED Matrix .............................. x1
  LED Bar Graph ............................... x1
  8 RGB LED Module ............................ x1
  RGB LED ..................................... x1
  Red LED ..................................... x10
  Green LED ................................... x4
  Blue LED .................................... x4
  Yellow LED .................................. x4

Physical input:
  Push Button ................................. x4
  Big Push Button ............................. x4
  Push Button Caps (red/green/blue/yellow) .... x1 each
  Switch ...................................... x2
  Vibration Switch ............................ x1
  Keypad (4x4) ................................ x1
  Joystick .................................... x1
  Infrared Remote ............................. x1
  Potentiometer ............................... x3

Passive electronics:
  Resistor 220 ohm ............................ x20
  Resistor 1K ohm ............................. x10
  Resistor 10K ohm ............................ x10
  Capacitor 0.1uF ............................. x2
  Capacitor 10uF .............................. x2
  Rectifier Diode ............................. x2
  Switch Diode ................................ x2
  NPN Transistor .............................. x2
  PNP Transistor .............................. x2
  Serial-to-Parallel Chip ..................... x2

Wiring & connectors:
  65 Jump Wire M-M ............................ x1
  10 Jump Wire F-F ............................ x1
  10 Jump Wire F-M ............................ x1
  40 Pin Header ............................... x1
  Female 40 Pin Header ........................ x1
  USB Cable ................................... x1
  9V Battery Cable ............................ x1
  Crowbar ..................................... x1

Power:
  2xAA Battery Holder ......................... x1
  Breadboard Power Module ..................... x1

Boards & misc:
  Project Board (breadboard) .................. x1
  General Board ............................... x3
  Resistor Color Code Card .................... x1
  Pinout Card ................................. x1
  Pinout Sticker .............................. x1
  Plastic Box ................................. x1
```

### Planned acquisitions (not ordered)
Folded into **Core & nodes** above, marked `[ ]` — projector, extra monitors, monitor arms, robot chassis, folding table.

*Excluded from this inventory: a Chinese writing-practice book bought in the same order — personal study material, unrelated to Dashvis.*

---

## Technical debt

Conscious design debt — deferred on purpose, to be resolved when the relevant function is built, not before:

- **Sovereign-backup mechanism (undecided).** The *rule* is set (owner-controlled targets, encrypted transport, no third-party-in-clear — `vision.md §7`). The *how* — SSH-on-arrival vs NAS vs a configured phone — is open. Decide when the first sensitive data needs to survive a device being off.
- **Egress logging (not built).** §7 requires recording which function opened which third-party door, carrying what. No logging exists yet; build it with the first function that opens a door.
- **Fine telemetry processing (unclear).** How presence/telemetry gets reduced before it may feed a feature is not designed. Treat all of it as sensitive until that reduction is defined.
- **Own-life heartbeat ↔ ChromaDB sync (sketch only).** The Tier-1 minimal identity / recent-context cache and its reconciliation with the Tier-2 store on PC wake are decided in principle (`vision.md §4.3`, §4.10) but not specified.
- **Node data continuity when the Tier-1 host is absent (undecided).** A node whose broker/host is away can buffer (MQTT QoS/retain + local store-and-forward) or drop. Choose per node when it matters; today nothing buffers. Relevant if the Tier-1 host is ever moved/swapped while nodes keep running.
- **Inter-tier auth / permissions on heterogeneous hosts (out of scope now).** Single owner + home network, so deferred. The §7 "availability ≠ permission" rule already forbids self-granted access; revisit only if Dashvis runs on shared or foreign devices (privilege-escalation surface).

---

*Last update: 2026-06-10 — hardware consultancy session (hybrid tiers, data flows, node inventory) + procurement batch logged. Phase 0 still active.*