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
**Learning:**  
Broke down package management, compilers and binaries: how code is written, packaged, distributed and how packages are installed.

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

**What happened:** Calibration: basic terminal (cd, ls, cp), Python between basic and modules, basic Git (commits/push), no networking. Brief generated with 4 mini-retos calibrated to that level + integrator reto (TCP server from documentation without copying examples). Learning session started with Gemini using the brief. Incomplete when closing this session.

**Learning:** Prior calibration significantly changes the retos. The same integrator reto (TCP server) has a different starting point depending on whether the user already understands what a port is or not.

**Decision made:** No architectural decision. Phase 0 work is done with Gemini using the generated brief.

**Reversible:** —

---

## 2026-06-04 — Reto system: from fixed to dynamic

**Context:** Each phase had a single hardcoded reto in `architecture.md`.

**What happened:** Analysis revealed that a single reto covers ~25% of a phase's skills. Phase 0 has 4 domains (Linux, Python, Git, networking) and the single reto only touched Python + networking. For a user with no Git experience, that reto validates nothing about Git. For someone who already knows networking, the reto adds nothing. It was symbolic, not representative.

**Learning:** A single reto per phase implies there is a test for the whole phase. There isn't — there is only one integrating artifact. The domain mini-retos are what validate real learning, and they depend on the starting level.

**Decision made:** Retos are generated at brief creation time with prior level calibration. `architecture.md` documents only the structure (mini-retos + integrator reto + optional extension), not the specific content.

**Reversible:** Yes. If fixed reference retos are preferred, they can be added as examples in `architecture.md` without eliminating dynamic generation.

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