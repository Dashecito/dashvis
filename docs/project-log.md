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

---

## Recent decisions

- 2026-06-10: MCU path decided — ESP32 + ESPHome (YAML) over manual Arduino C++
  and over the Pico W / MicroPython route. Arduino C++ kept only at reading level
  in Phase 3 (debug ESPHome output + occasional custom component). Pico W marked
  off critical path (profile-driven, not planned for repurchase). Learning-first
  philosophy unchanged; "understanding a tool" clarified as grasping what it
  abstracts, not reimplementing it. Full Freenove kit inventory added under
  Hardware. See vision.md §3 & §4.12, architecture.md §2 & §3 (Phase 3). Detailed
  rationale in devlog.md.

- 2026-06-04: Phase 0 setup vs system development conflict — supposedly covered.
  Should be able to continue with Gemini now; it will know what goes to phase_0 and what doesn't based on the brief.

- 2026-06-04: Repo structure defined. Exercises → scratch/phase_N/,
  system modules → domain folders. See architecture.md §4.

Foundational design decisions are in `vision.md §4`.

---

## Hardware

### System hardware
```
Raspberry Pi:     [ ] To acquire / [X] On hand
ESP32:            [X] To acquire / [ ] On hand   ← critical-path purchase for Phase 3 (runs ESPHome)
Microphones:      [X] To acquire / [ ] On hand
Cameras:          [X] To acquire / [ ] On hand
Mini projectors:  [X] To acquire / [ ] On hand   (not needed yet — prototyping output goes to the monitor)
Robot (chassis):  [X] To acquire / [ ] On hand
Alexa/Echo:       [ ] To acquire / [X] On hand
Extra monitors:   [X] To acquire / [ ] On hand
Monitor arms:     [X] To acquire / [ ] On hand
Etc.              (to be defined)
```

### Freenove Ultimate Starter Kit — ON HAND
Full component inventory below. These sensors and modules connect to the ESP32 for
Phase 3 prototyping. The kit originally shipped with a Raspberry Pi Pico W, now lost.

Pico W status: OFF the critical path, not planned for repurchase for now. Given the
profile (backend / async / architecture-first), the low-level Pico W + MicroPython
route adds little *transferable* value relative to this direction — the skills the
project is meant to build are async, distributed systems, and architecture, not
I2C/SPI timing. ESP32 + ESPHome is the chosen path. The Pico W remains an optional
detour if a low-level dive is ever wanted; the kit's sensors work with the ESP32
regardless.

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

---

## Technical debt

*No technical debt recorded.*

---

*Last update: founding session — Phase 0 started.*