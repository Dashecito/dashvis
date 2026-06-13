# Dashvis — Devlog

> Useful historical memory. Does not describe the current state (that is `project-log.md`) but how we got here.  
> Answers: "why did we drop that library?", "why did we split that layer?", "what broke the voice flow?".

Entry format:

```
## YYYY-MM-DD — [Phase N / Brief description]

**Context:** what was being attempted.
**What happened:** actual result (success, failure, unexpected discovery).
**Learning:** what is understood now that wasn't before.
**Decision made:** what changed as a consequence (if anything).
**Reversible:** yes / no / partially.
```
---
## 2026-06-12 — [Phase 0 / Finished Unit 6: File I/O CS50P course content]

**Context:** Finished Unit 6: File I/O CS50P course content, being these all the lectures. I still have to do (and once I do I will report it in the devlog as well) the Problem Set of this unit. Today is friday. I plan doing at least 1 tomorrow and the rest on Sunday. I will update once I finish this Unit 6. I've last like 2-3 days for this because I tend to disperse and learn about more stuff during this, like: 
- flushing
- memory management
- threading, and the python library that manages it: 
  - basic usage of these libraries: signal, threading, time.

**What happened:** learned about writing and reading and modifying CSV files, .txt files, and images with PIL library. Done tons of exercises and watched about 30 min of lectures. 
(basic usage of these libraries: signal, threading, time)
Basic flushing, memory management, threading... etc

**Learning:** Basic File I/O management and other stuff. 

**Decision made:** Finish the Problem Set before this week ends (last day being 2026/6/14 23:59PM UTC+2) and keep on going with the phase 0 with Gemini. 

**Reversible:** not applicable. It's learning. 

---

## 2026-06-11 — [Architecture / Tiers are roles, not devices + no-hardcoded-host rule]

**Context:** The graceful-degradation block read "RPi off → system down by design",
which grated: it ties the system's life to one specific box. Owner pushed on the
portability cases — swap the RPi for a laptop, demo at a friend's house, install
Dashvis on another device, and what happens to node data when a host disconnects.

**What happened / resolved:**
- Reframed Tier 1/2/3 as **roles**, with the device named only as the *current
  assignment*. Any always-on host can hold Tier 1; one capable host can hold several
  roles at once (laptop = Tier 1 + Tier 2 → a portable Dashvis to demo elsewhere
  without taking the home RPi). This dissolves the "PC on + RPi off" puzzle: whoever
  runs Tier 2 can also run Tier 1.
- "RPi off → system down" rewritten to "no always-on core present: the core guarantee
  pauses until some host takes the Tier-1 role; not a crash, Dashvis re-instantiates
  elsewhere." The *floor* concept stays (there must be an always-on core); what changed
  is that the floor is a role, not a box.
- Adopted the owner's rule of thumb as principle 8: no hardcoded host assumptions —
  device paths / IPs / hostnames go in `.env`, never in module code. This is the
  lightweight discipline that makes the role model real; nothing to implement now.
- Logged two deferred debts: node data continuity when a host is absent (buffer vs
  drop), and inter-tier auth / privilege-escalation surface (out of scope while single
  owner + home network — §7 "availability ≠ permission" already covers the principle).

**Learning:** Most of the owner's worry was framing, not a design flaw — the
architecture already supported host-mobility (derivability + "discovered not wired");
the docs just spoke in device names. Naming roles vs assignments fixed it without new
machinery. Building a permissions model now would be over-engineering; noting it as a
deferred surface is the right altitude.

**Decision made:** vision §4.13 (role note) + principle 8; architecture §1.7 (role
table, role-based degradation, `.env` rule in Mobility); project-log technical debt
(two items).

**Reversible:** Yes — framing + one rule + two logged debts; no implementation.

---

## 2026-06-10 — [Architecture / Hybrid compute tiers, graceful degradation, data-flow governance, node inventory]

**Context:** Came back from a long external-AI hardware-consultancy session with a
summary: a three-tier hybrid compute model, graceful degradation, and a batch of
newly acquired hardware (ESP32-S3 + WROOM-32 fleet, OV5647 camera, RTL-SDR + RPi
3B+, Alfa adapter, reused smartphone). The summary had to be processed *critically*,
not pasted in — the owner explicitly asked to flag conflicts with what was already
decided. Several real tensions surfaced and were worked through over the session.

**What happened / tensions resolved:**
- *Brain location vs always-on identity.* Moving the LLM + ChromaDB to the PC (Tier
  2) meant own-life and memory would die when the PC sleeps — a direct conflict with
  the "always-on, own life" vision. Resolved with the Jarvis-in-the-suit split:
  minimal identity + recent-context cache persist 24/7 on Tier 1; heavy capability
  lives on Tier 2; they reconcile on PC wake. Identity is the floor, capability scales.
- *Heuristics-only felt too dumb offline.* Introduced a third brain rung — an
  optional local SLM (~1–3 B) on Tier 1 — so degradation is a gradient of eloquence,
  not functional-vs-mute. SLM is optional; falls back to heuristics if the RPi can't.
- *The cloud/API contradiction (owner-spotted).* "Sensitive data never goes to a
  third party in clear" collided with sending voice/percepts to an LLM API. Resolved
  by separating two flows and the insight that local-first ≠ local-only: raw never
  crosses; only reduced text/metrics, explicitly, per function. The boundary is the
  *state of rawness* at egress, not where compute happens.
- *Who decides to use the cloud.* Settled: the router may choose local vs third-party
  *among already-authorised doors*, but cannot open new ones — availability ≠
  permission. Doors are opened by the owner at design time.
- *"Non-sensitive" telemetry isn't.* Owner correctly pushed back that telemetry leaks
  by combination. Dropped the sensitive/non-sensitive classification entirely;
  governance is by where-data-lives / how-it-travels (the two flows).
- *Where the SDR lives.* It risked being both "fundamental telemetry" and "out of
  tree". Resolved: device + raw capture out-of-tree (neutral RF project); only reduced
  telemetry enters via MQTT. Fundamental ≠ inside — Dashvis depends on a data flow,
  not the apparatus.
- *Offensive/defensive bias.* Kept the project and its derivatives neutral by
  construction so they can pivot under their own terms; the boundary on offensive
  *tooling* is about what gets built, not a label baked into the architecture.

**Learning:** The original "everything on the RPi" was a latent sizing debt, not a
real design — the tier model is the correction, so this added realism rather than
complexity. A privacy model survives contact with reality only if it governs the
*egress boundary in a reduced state*, not the existence of cloud calls. And most of
these were principle-level decisions whose *mechanism* is rightly deferred (logged as
conscious technical debt), so nothing here required writing implementation.

**Decision made:** vision.md — §4.3 & §4.10 retiered, new §4.13 (hybrid tiers) &
§4.14 (three-rung brain/SLM), principles 6 (graceful degradation) & 7 (data
sovereignty), §6 extended (SDR-as-external-provider + neutrality), new §7 (data
flows). architecture.md — §1.1 brain retiered, §1.2 & §1.6 nodes + egress, new §1.7
(deployment topology + degradation), stack table + Local SLM and out-of-tree note.
project-log.md — node inventory, system-hardware checklist, three decisions,
technical-debt section, open-question doors.

**Reversible:** Yes, at the design level. Tiers/flows are principles; the deferred
mechanisms (backup transport, egress logging, heartbeat sync) are still open and can
be chosen differently when their phase arrives.

---

## 2026-06-10 — [Docs / Terminology normalization + derivability principle]

**Context:** Review pass over the four docs after the MCU / learning-path update.
Three issues raised: (1) the MicroPython row in the stack table wrapped in narrow
viewers, orphaning "MicroPython" under the Layer column; (2) "reto/retos" (Spanish)
was still mixed into the otherwise-English docs — a confusion risk when these docs
are pasted as context into fresh (often English) sessions; (3) the project's
reusability / agnostic nature was implied but never stated as a principle.

**What happened:**
- Shortened the MCU firmware stack row ("Manual Arduino C++, MicroPython" →
  "Arduino C++, MicroPython") so it no longer wraps. "Manual" was filler —
  ESPHome auto-generating already implies the contrast.
- Normalized all "reto/retos" → "challenge/challenges" across architecture.md and
  devlog.md (project-log.md already used "challenge"; vision.md never used the
  term). Terminology is now consistent across all four docs.
- Added a Derivable-and-portable principle. Full detail lives in a new
  **vision.md §6** (Derivability and portability), with a one-line pointer from §5
  principle 3 (modularity) and a cross-reference in architecture.md §4. Kept out of
  the §5 principles list on purpose — a 12-line item breaks the one-liner format, so
  the detail was relocated rather than shortened. Framed as a structural property,
  not a feature list.

**Learning:** Checked the derivability claim before stating it — the architecture
genuinely supports lifting modules out (explicit interfaces + function-organized
repo). Leaf modules (perception, automation, data) extract cleanly; the brain
carries more Dashvis-specific state, so derivatives from it inherit more identity.
Stated that honest scope in the principle rather than overselling it.

**Decision made:** vision.md (new §6 + pointer from principle 3), architecture.md
(§2 row shortened, §4 cross-ref, terminology), devlog.md (terminology). No phase
work — doc consistency plus one new principle.

**Reversible:** Yes. Terminology and principle are localized; revertible per file.

---

## 2026-06-10 — [Docs / Learning-path calibration: ESPHome over manual Arduino C++ & the Pico W route]

**Context:** Evaluated whether to add a low-level learning detour (Raspberry Pi
Pico W + Freenove sensor kit, MicroPython, hand-written GPIO/MQTT) before the ESP32
work, and whether the learning-first philosophy in vision.md needed softening to
protect motivation. Trigger: a long discussion about projectors, the Freenove kit
(on hand, Pico W lost), and how much hardware depth is worth it given the owner
profile (backend / async Python / architecture-first).

**What happened:**
- Confirmed the learning-first philosophy stays. "Learning over build speed" is the
  real value; it does not change. Earlier instinct to soften it was wrong.
- Identified the actual tension: ESPHome abstracts the low-level code, which looked
  like a conflict with "no tools as black boxes". Resolved by clarifying that
  "understanding a tool internally" means grasping the concepts it abstracts (what
  MQTT guarantees, what a GPIO pin is, what a sensor measures), not reimplementing
  its internals.
- Decided ESP32 + ESPHome (YAML) is the MCU path. The Pico W / MicroPython low-level
  route is OFF the critical path — for this profile it adds little transferable value
  (the transferable skills are async, distributed systems, architecture, not I2C/SPI
  timing). Pico W stays an optional detour, not a prerequisite; not planned for
  repurchase.
- Recalibrated Arduino C++ in Phase 3: not a primary skill to develop, but a
  reading-level competence — enough to read what ESPHome generates, debug it, and
  write the occasional custom component.
- Catalogued the full Freenove kit inventory in project-log.md (sensors reused with
  the ESP32 regardless of the Pico W decision).

**Learning:** A tool that hides low-level code (ESPHome) is compatible with a
learning-first philosophy as long as the goal is comprehension of the abstracted
concepts, not manual reimplementation. Depth should be calibrated to the profile
direction, not maximised uniformly across every layer — chasing I2C/SPI mastery
would disperse effort away from the skills the project is actually meant to build.

**Decision made:** Four docs updated — vision.md (§3 clarified, §4.12 ESP32 now
ESPHome YAML), architecture.md (§1.4 actuator note, §2 stack adds MCU firmware =
ESPHome, §3 Phase 3 recalibrated), project-log.md (full kit inventory + Pico W
off-path + recent-decisions entry). No phase work done; this is a planning /
calibration change only.

**Reversible:** Yes. The Pico W detour can be re-added if a low-level dive is ever
wanted; Phase 3 depth can be deepened; all doc edits are localized.

---

## 2026-06-10 — [Phase 1 / ALT LEARNING / Graceful Shutdowns, Threading Concepts, & OS-Level Bottlenecks]

**Context:** I am building IoT project and wanted to understand why Python programs hang when pressing `Ctrl+C`. I started by analyzing a py4u.org blog post about Python threads ignoring `SIGINT`. To test graceful shutdowns in practice, I applied the concepts to a simpler, single-threaded CSV logging script, but encountered a frustrating issue where the terminal would freeze for 2-3 seconds every time I pressed `Ctrl+C`.

**What happened:** 
1. **Understanding Threads:** I learned that Python threads are cooperative. Worker threads don't "hear" `Ctrl+C` natively; they need a pager system (`threading.Event`) to know when to safely exit. I also learned that `daemon=True` forces abrupt exits, which is dangerous for IoT (leaves motors running or corrupts files).
2. **Testing Graceful Exits:** I wrote a CSV writer script to test `KeyboardInterrupt` and `sys.exit(0)`. However, the script kept hanging my terminal for a few seconds on exit. 
3. **Timing the Code:** I suspected the size of my log file (120MB) was causing Python to struggle. I wrapped `file.flush()` in a `time.time()` stopwatch. The flush took only 0.0002 seconds. Python was lightning-fast; the hang was happening *after* my code finished.
4. **The "Tiny Test" (Isolating Variables):** I changed the code to write to a brand-new, empty `tiny_test.csv` file. When I pressed `Ctrl+C`, it exited instantly with zero hang. This proved the file size was a factor, but not because of Python.
5. **Visual Proof (Resource Monitor):** I opened Windows *Monitor de recursos* side-by-side with VS Code. By filtering the disk activity, I watched what happened the exact millisecond I pressed `Ctrl+C`. I caught `MsMpEng.exe` (Windows Defender) suddenly spiking and hijacking my `01csvfile.csv` file.

**Learning:** 
* **Theory:** Hardware and network connections need time to close safely, which is why we must catch signals and politely ask loops to stop rather than forcefully killing them.
* **OS Mechanics:** A terminal hang isn't always bad code. The moment a script gracefully closes a file, the OS "bouncer" (Antivirus) intercepts it to scan for threats. 
* **The Root Cause:** Scanning a 120MB CSV takes 2-3 seconds of physical disk read time. During this time, the OS locks the file and freezes the IDE/terminal. 
* **Scientific Debugging:** I learned to isolate variables (changing file size) and use OS tools to definitively prove external bottlenecks rather than guessing.

**Decision made:** Concluded that my Python code and graceful shutdown logic are perfectly optimized. The root cause of the hang is definitively the Windows Antivirus scanning the large file on exit. It was recommended to add my IoT project folder to the Windows Defender "Exclusions" list to prevent this in the future, though I have not applied this setting yet.

**Reversible:** Yes (Exclusions can be added or removed in Windows Settings if I choose to apply the fix later).

---

## 2026-06-09 — Phase 0 / File I/O fundamentals: iteration vs readlines(), CSV parsing

**Context:** Working through CS50P Topic 6 (File I/O) as prerequisite groundwork
before tackling the Python mini-challenge from Phase 0 (psutil + CSV logger with
error handling, stdlib only). Created test_fileio.py to experiment hands-on and
csvfile.csv as the working dataset. Used CS50P Topic 6 documentation as reference
reinforcement throughout. Goal: finish Topic 6 before or in parallel with the
mini-challenge.

**What happened:** Two separate sessions covering adjacent File I/O concepts.

Session 1 — file object iteration vs readlines():
Started from a CS50P code example that used readlines() then iterated over the
result, which could be simplified to iterating the file object directly. That
raised the question of whether readlines() was pointless. Discovered that file
objects are iterators, not sequences — so file[0], len(file), and slicing don't
work. Also discovered the course notes contained an inaccuracy: they claimed you
"can't sort something you're reading line by line", but sorted(file) works fine
because Python consumes the iterator internally. The actual limitation is more
specific: you can't sort while processing lines as they arrive — you need all
lines collected first.

Session 2 — CSV parsing and dict vs list structure:
Explored two approaches to reading a CSV into memory and sorting it. The
commented-out approach (unpacking each row into named variables, building an
explicit dict, appending that dict) worked correctly with key-based access in
sorted(). Switching to appending the raw row directly silently changed the data
structure from dict to list, breaking the lambda in sorted() at runtime with a
TypeError. No syntax error, no warning — the inconsistency only surfaced at the
sort step.

**Learning:**
- A file object is an iterator: supports forward-only one-at-a-time reading,
  for loops, sorted(), and list(). Does not support file[0], len(file), or
  slicing — not because Python refuses arbitrarily, but because the file object
  holds only a cursor and has no knowledge of total line count without reading
  the whole file first.
- readlines() loads everything into memory as a real list, unlocking indexing,
  len(), slicing, and multiple passes — at the cost of memory. The right choice
  depends on what you need to do downstream.
- sorted(file) works: Python consumes the iterator line by line internally and
  sorts the result. The CS50P notes claiming otherwise were imprecise. The correct
  constraint is: you can't sort lines while processing them as they arrive — you
  need them all collected first, which sorted() handles automatically.
- csv.reader yields list rows, not dicts. Key-based access only works if you
  explicitly construct the dict yourself, or use csv.DictReader, which does it
  automatically from the header row.
- Appending row directly vs appending a constructed dict is not interchangeable:
  it changes the type of every element in the list, and downstream code assuming
  dict structure breaks silently until a key access is attempted.
- For CSVs with more than 2–3 columns, index-based access (p[0], p[1]) is fragile
  — any column reorder silently corrupts the data. Key-based access (p["name"])
  is robust to that.

**Decision made:** Use direct file object iteration as the default for single-pass
reading. Use readlines() only when indexing, length, slicing, or multiple passes
are needed. Use csv.DictReader as the default for any CSV with a header row —
eliminates the manual unpack-and-build step and makes code self-documenting.
Both sessions are direct prerequisites to the mini-challenge: writing the psutil
CSV logger requires understanding how csv.writer produces rows, what the stdlib
csv module can and cannot do, and how file iterators behave — all covered here.

**Reversible:** Yes.

---

## 2026-06-07 — [Phase 0 / Python RAM, Timestamps & IDE Taming]

**Context:** Continuing Python mini-challenge (hardware tracking). Expanding the `test_cpu.py` script to include RAM and Timestamps, while fixing IDE distractions.
**What happened:** Disabled VS Code's aggressive autocomplete via `settings.json`. Fetched RAM data using `psutil.virtual_memory()` and current time using the native `datetime` module. Discussed the pros and cons of tuple unpacking.
**Learning:** - Taming VS Code requires diving into `settings.json` (`editor.inlineSuggest.enabled`, etc.) to truly disable ghost text and auto-closing brackets for pure coding focus.
- `psutil` returns "named tuples" for complex data like RAM. Extracting data via dot notation (`mem.percent`, `mem.free`) is fundamentally safer and cleaner than unpacking all variables blindly (`a, b, c, d, e = ...`).
- Python's native way to get the exact time is redundantly named: `datetime.datetime.now()`.
- Real-world programming relies on searching by "intent" (e.g., "Python get current timestamp") rather than memorizing function names.
**Decision made:** Use dot notation for hardware data extraction. Code is prepped with CPU, RAM, and timestamp variables.
**Reversible:** N/A (learning).

---

## 2026-06-05 — [Phase 0 / Mini-Challenge 2 & Env Epiphanies]

**Context:** mini-challenge 2 regarding python venv  and native hardware tracking with gemini.
**What happened:** Created a virtual environment (`.venv`), activated it, upgraded `pip`, installed `psutil`, and ran `test_cpu.py` to fetch real-time CPU stats (~3% usage).
**Learning:** - A virtual env is not just an empty directory made with `mkdir`; it requires `python -m venv` to clone the core language interpreter.
- Being physically inside the project folder doesn't mean dependencies are isolated automatically. The terminal pointer itself needs to be hijacked via `source`, visually tracked by the `(.venv)` prefix.
- Connected this to my LOLDLE project: understood that `node_modules` and `.venv` serve the exact same purpose (the "app store" for dependencies).
- Massive realization about `dist/` and Firebase: `npm run build` squashes everything for the browser sandbox, and `firebase deploy` updates code structure, whereas live database connections stream data independently without needing a code redeploy.
- New environments inherit a frozen (sometimes outdated) backup version of `pip` stored in Python's core directory, which needs an explicit upgrade.
**Decision made:** Native isolated backend ecosystem is officially running. Ready to scale.
**Reversible:** N/A (learning).

---

## 2026-06-05 — [Phase 0 / Web Sandbox vs Native OS]

**Context:** understanding modern web architecture vs native backend through my LOLDLE project.

**What happened:** mapped JS/React concepts (`node_modules`, `dist`, Firebase) to Python (`.venv`, native execution).

**Learning:** Web frontends run in a browser sandbox (Client-side) and cannot access physical hardware. Serverless apps use BaaS (Firebase) for data storage, but Dashvis requires a native Python backend running directly on the OS to bypass the browser sandbox and read CPU/RAM data. Also, `.venv` is Python's `node_modules` but includes a cloned interpreter, not just libraries.

**Decision made:** proceed to create `.venv` to build the native Dashvis backend.

**Reversible:** N/A (learning).

---

## 2026-06-05 — [Phase 0 / mini-challenge 1]

**Context:** mini-challenge 1 with gemini.

**What happened:** repository done. public and open core. local-online connection thanks to .git. So far everything
will be done in "phase-0" branch. Later on, when I know more about the project, we'll start with the main branch.

**Learning:** .git relevance and autocrlf for file compatibility between linux (rpi) & windows  

**Decision made:** open core

**Reversible:** partially

---

## 2026-06-05 — [Phase 0 / Language swap]

**Context:** spansish to english

**What happened:** change all the documentation from spanish to english

**Learning:** nothing.

**Decision made:** from now on I'll be working on a fully english basis so there's no name inconsistency

**Reversible:** yes, with AI. 

---

## 2026-06-04 — [Phase 0 / git beginnings]

**Context:** continued with Gemini.  
**What happened:** understood basic .gitignore syntax and did git init.  
**Learning:** .gitignore syntax and introductory Linux CLI commands.  
**Decision made:** .gitignore and git init done. Still need to create phase-0 branch and understand why it's done. See brief.  
**Reversible:** yes

---

## 2026-06-04 — [Phase 0 / Learning with Gemini]

**Context:** learning with Gemini before starting Phase 0 work.  

**What happened:** granular learning session.  

**Learning:** Broke down package management, compilers and binaries: how code is written, packaged, distributed and how packages are installed.

Precompiled files (.whl) and what they contain (.dll, .py, metadata... or other files for complex libraries).

pip installs these based on processor and OS. There is a .whl for each combination.

The OS is the building's rules, the processor is the worker who speaks a language. The binary (.dll/.so) are instructions written in that language.

**Decision made:** none.  

**Reversible:** this is learning, attribute does not apply.

---

## 2026-06-04 — Repository structure defined

**Context:** When initializing git in the Dashvis folder with Gemini, the question arose of where to put Phase 0 code and how the repo would evolve with phases.

**What happened:** The structure `phases/phase_0/`, `phases/phase_1/`... organizes code by when it was learned, not by what it does. Phase 0 exercises (monitor.py, TCP server) are not Dashvis components — they are learning artifacts that don't go to production. Mixing them with system folders would make the repo a diary instead of a project.

**Learning:** Phases are a learning structure. The repository must be a system structure. `scratch/phase_N/` for exercises; architectural folders (`brain/`, `perception/`, etc.) for real code that grows with the project.

**Decision made:** Structure defined in `architecture.md §4`. System folders appear when that module is built, not before. Phase 0 only produces `scratch/phase_0/`. This structure is included in all briefs as a fixed section.

**Reversible:** Yes. If an exercise turns out to be directly reusable as a real component, it is moved to its architectural folder.

---

## 2026-06-04 — Phase 0 brief generated

**Context:** First real working session of the project. Level calibration before generating the brief.

**What happened:** Calibration: basic terminal (cd, ls, cp), Python between basic and modules, basic Git (commits/push), no networking. Brief generated with 4 mini-challenges calibrated to that level + integrator challenge (TCP server from documentation without copying examples). Learning session started with Gemini using the brief. Incomplete when closing this session.

**Learning:** Prior calibration significantly changes the challenges. The same integrator challenge (TCP server) has a different starting point depending on whether the user already understands what a port is or not.

**Decision made:** No architectural decision. Phase 0 work is done with Gemini using the generated brief.

**Reversible:** —

---

## 2026-06-04 — Challenge system: from fixed to dynamic

**Context:** Each phase had a single hardcoded challenge in `architecture.md`.

**What happened:** Analysis revealed that a single challenge covers ~25% of a phase's skills. Phase 0 has 4 domains (Linux, Python, Git, networking) and the single challenge only touched Python + networking. For a user with no Git experience, that challenge validates nothing about Git. For someone who already knows networking, the challenge adds nothing. It was symbolic, not representative.

**Learning:** A single challenge per phase implies there is a test for the whole phase. There isn't — there is only one integrating artifact. The domain mini-challenges are what validate real learning, and they depend on the starting level.

**Decision made:** Challenges are generated at brief creation time with prior level calibration. `architecture.md` documents only the structure (mini-challenges + integrator challenge + optional extension), not the specific content.

**Reversible:** Yes. If fixed reference challenges are preferred, they can be added as examples in `architecture.md` without eliminating dynamic generation.

---

## 2026-06-04 — Architecture diagram: three iterations

**Context:** `architecture.md` needed a system diagram. The interactive SVG exists but is a navigation artifact, not text documentation.

**What happened:**
- **Iteration 1 (error):** 3×2 grid without section labels. Two anonymous rows of three modules each. The layout implied PERCEPTION → AUTOMATION and VISUAL OUTPUT → ROBOT had vertical dependency. False.
- **Iteration 2 (overcorrection):** hub-and-spoke with 5 flat boxes and identical ▼ arrows for all. Eliminated false dependencies but collapsed 15 detailed blocks into 5 summaries and lost the sub-module groupings, which are real (ESP32 + HA + Alexa are the automation layer, not individually equivalent to the whole robot).
- **Iteration 3 (current):** flat hub-and-spoke maintained, but arrows differentiated by relationship type: ↑ input (PERCEPTION sends data to brain), ↓ output (brain directs VISUAL OUTPUT without return), ↕ control (AUTOMATION/ROBOT: commands + state back), ↕ service (DATA: transversal infrastructure, not a peer module).

**Learning:** Text diagrams need explicit annotations that visual diagrams get for free from color and section labels. The interactive SVG uses color per section and labels — that eliminates the ambiguity that text needs to resolve with symbols. DATA is qualitatively different from the rest: the brain reads and writes there, but other modules also produce data stored there. It is not an orchestrated module, it is shared infrastructure.

**Decision made:** Hub-and-spoke diagram with flow annotations. DATA marked as ↕ service with explicit note in the legend. Introductory paragraph updated: no longer says "6 vertical layers" but "hub-and-spoke".

**Reversible:** Yes — if in later phases the system grows and direct relationships appear between modules (e.g. PERCEPTION feeding directly to DATA without going through the brain), the diagram will need updating.

---

## 2026-06-04 — Documentation system: 4 files

**Context:** The project started with a single `vision.md` that mixed identity, architecture, operational state, and history.

**What happened:** Split into 4 files with distinct responsibilities. Project renamed from "Jarvis" to "Dashvis". A "Dashvis intent" section was added to `vision.md` that didn't exist in the original — it captures the soul of the project in first person, distinguishes Dashvis from Alexa/Siri, and preserves the original intentions as literal quotes.

**Learning:** A single file mixing "why the project exists", "how it is organized" and "where we are" is hard to maintain and hard to use as context in new sessions. The separation makes each file answer a distinct question with a different change frequency: `vision.md` almost never changes, `project-log.md` changes constantly.

**Decision made:**
- `vision.md` — identity, philosophy, reasoning behind decisions
- `architecture.md` — system structure, stack, phases, brief/return templates
- `project-log.md` — current operational state
- `devlog.md` — history of useful changes and learnings

**Reversible:** The file structure yes. Merging two files if they become redundant is trivial. The name Dashvis: pending final confirmation.

---

*Entries are added in reverse chronological order (most recent first).*