# Dashvis — Devlog

> Memoria histórica útil. No describe el estado actual (eso es `project-log.md`) sino cómo se llegó hasta él.  
> Responde a: "¿por qué descartamos esa librería?", "¿por qué separamos esa capa?", "¿qué rompió el flujo de voz?".

Formato de entrada:

```
## YYYY-MM-DD — [Fase N / Descripción breve]

**Contexto:** qué se estaba intentando hacer.
**Qué pasó:** resultado real (éxito, fallo, descubrimiento inesperado).
**Aprendizaje:** qué se entiende ahora que no se entendía antes.
**Decisión tomada:** qué cambió como consecuencia (si algo cambió).
**Reversible:** sí / no / parcialmente.
```
---

## 2026-06-04 — [Fase 0 / git inicios]

**Contexto:** seguí con gemini 
**Qué pasó:** entendi sintaxis de .gitignore basica, e hice el git init. 
**Aprendizaje:** sintaxis .gitignore y introductory cli linux commands
**Decisión tomada:** .gitignore y .gitinit. falta branch de fase 0 y entender por que se hace. ver brief para ello.
**Reversible:** sí 

---

## 2026-04-06 — [Fase 0 / Aprendiendo con gemini]

**Contexto:** aprendiendo con gemini antes de empezar con la fase 0 
**Qué pasó:** aprendizaje granulado
**Aprendizaje:** 
desgranado la gestión de paquetes, compiladores y binarios: cómo se escribe, cómo se empaqueta, cómo se distribuye y cómo se instalan paquetes

archivos precompilados (.whl) y lo que ofrecen (.dll, .py, metadatos... u otros archivos si son librerias complejas)

estos de arriba pip los instala segun el procesador y sis operativo. Hay un .whl para cada combinacion.

el sistema operativo son las normas del edificio, el procesador es el trabajador que habla un idioma. El binario (.dll/.so) instrucciones escritas en x idioma.

**Decisión tomada:** ninguna 
**Reversible:** es aprendizaje. No toma este atributo.

---

## 2026-06-04 — Estructura de repositorio definida

**Contexto:** Al inicializar git en la carpeta Dashvis con Gemini, surgió la pregunta de dónde poner el código de Phase 0 y cómo evolucionaría el repo con las fases.

**Qué pasó:** La estructura `phases/phase_0/`, `phases/phase_1/`... organiza el código por cuándo se aprendió, no por qué hace. Los ejercicios de Phase 0 (monitor.py, servidor TCP) no son componentes de Dashvis — son artefactos de aprendizaje que no van a producción. Mezclarlos con carpetas del sistema haría el repo un diario en vez de un proyecto.

**Aprendizaje:** Las fases son una estructura de aprendizaje. El repositorio debe ser una estructura de sistema. `scratch/phase_N/` para ejercicios; carpetas arquitectónicas (`cerebro/`, `percepcion/`, etc.) para código real que crece con el proyecto.

**Decisión tomada:** Estructura definida en `architecture.md §4`. Las carpetas del sistema aparecen al construir ese módulo, no antes. Phase 0 solo produce `scratch/phase_0/`. Esta estructura se incluye en todos los briefs como sección fija.

**Reversible:** Sí. Si un ejercicio resulta ser directamente reutilizable como componente real, se mueve a su carpeta arquitectónica.

---

## 2026-06-04 — Brief de Fase 0 generado

**Contexto:** Primera sesión de trabajo real del proyecto. Calibración de nivel antes de generar el brief.

**Qué pasó:** Calibración: terminal básico (cd, ls, cp), Python entre básico y módulos, Git básico (commits/push), redes ninguna. Brief generado con 4 mini-retos calibrados a ese nivel + reto integrador (servidor TCP desde documentación sin copiar ejemplos). Sesión de aprendizaje iniciada con Gemini usando el brief. Sin completar al cerrar esta sesión.

**Aprendizaje:** La calibración previa cambia significativamente los retos. El mismo reto integrador (servidor TCP) tiene distinto punto de partida según si el usuario ya entiende qué es un puerto o no.

**Decisión tomada:** Ninguna arquitectónica. Trabajo de Fase 0 se realiza con Gemini usando el brief generado.

**Reversible:** —

---

## 2026-06-04 — Sistema de retos: de fijos a dinámicos

**Contexto:** Cada fase tenía un único reto hardcodeado en `architecture.md`.

**Qué pasó:** Análisis reveló que un solo reto cubre ~25% de los skills de una fase. La Fase 0 tiene 4 dominios (Linux, Python, Git, redes) y el reto único solo tocaba Python + redes. Para un usuario sin experiencia en Git, ese reto no valida nada de Git. Para alguien que ya sabe redes, el reto no aporta. Era simbólico, no representativo.

**Aprendizaje:** Un reto único por fase implica que existe una prueba de toda la fase. No la hay — solo hay un artefacto integrador. Los mini-retos por dominio son los que validan el aprendizaje real, y dependen del nivel de partida.

**Decisión tomada:** Los retos se generan en el momento del brief con calibración previa. `architecture.md` documenta solo la estructura (mini-retos + reto integrador + extensión opcional), no el contenido concreto.

**Reversible:** Sí. Si se prefiere tener retos de referencia fijos, se pueden añadir como ejemplo orientativo en `architecture.md` sin eliminar la generación dinámica.

---

## 2026-06-04 — Diagrama de arquitectura: tres iteraciones

**Contexto:** `architecture.md` necesitaba un diagrama del sistema. El SVG interactivo existe pero es un artefacto de navegación, no de documentación en texto.

**Qué pasó:**
- **Iteración 1 (error):** cuadrícula 3×2 sin etiquetas de sección. Dos filas anónimas de tres módulos cada una. El layout implicaba que PERCEPCIÓN → DOMÓTICA y SALIDA VISUAL → ROBOT tenían dependencia vertical. Falso.
- **Iteración 2 (overcorrección):** hub-and-spoke con 5 cajas planas y flechas ▼ iguales para todos. Eliminó las dependencias falsas pero colapsó 15 bloques en 5 resúmenes y perdió las agrupaciones de sub-módulos, que sí son reales (ESP32 + HA + Alexa son la capa domótica, no equivalentes individuales al robot).
- **Iteración 3 (actual):** hub-and-spoke plano mantenido, pero flechas diferenciadas por tipo de relación: ↑ entrada (PERCEPCIÓN envía datos al cerebro), ↓ salida (cerebro dirige SALIDA VISUAL sin retorno), ↕ control (DOMÓTICA/ROBOT: comandos + estado de vuelta), ↕ servicio (DATOS: infraestructura transversal, no módulo peer).

**Aprendizaje:** Los diagramas en texto necesitan anotaciones explícitas que los diagramas visuales reciben gratis del color y las etiquetas de sección. El SVG interactivo usa colores por sección y etiquetas — eso elimina la ambigüedad que el texto requiere resolver con símbolos. DATOS es cualitativamente diferente al resto: el cerebro lee y escribe allí, pero también otros módulos producen datos que se almacenan. No es un módulo orquestado, es infraestructura compartida.

**Decisión tomada:** Diagrama hub-and-spoke con anotaciones de flujo. DATOS marcado como ↕ servicio con nota explícita en la leyenda. Párrafo introductorio de la sección actualizado: ya no dice "6 capas verticales" sino "hub-and-spoke".

**Reversible:** Sí — si en fases posteriores el sistema crece y aparecen relaciones directas entre módulos (por ejemplo, PERCEPCIÓN alimentando directamente a DATOS sin pasar por el cerebro), el diagrama necesitará actualización.

---

## 2026-06-04 — Sistema de documentación: 4 archivos

**Contexto:** El proyecto comenzó con un único `vision.md` que mezclaba identidad, arquitectura, estado operativo e historial.

**Qué pasó:** Se separó en 4 archivos con responsabilidades distintas. Se renombró el proyecto de "Jarvis" a "Dashvis". Se añadió una sección de "Intención del asistente" a `vision.md` que no existía en el original — captura el alma del proyecto en primera persona, distingue Dashvis de Alexa/Siri, y preserva las intenciones originales como citas literales.

**Aprendizaje:** Un solo archivo que mezcla "por qué existe el proyecto", "cómo está organizado" y "en qué punto estamos" es difícil de mantener y difícil de usar como contexto en sesiones nuevas. La separación hace que cada archivo responda a una pregunta distinta y tenga una frecuencia de cambio diferente: `vision.md` casi nunca cambia, `project-log.md` cambia constantemente.

**Decisión tomada:**
- `vision.md` — identidad, filosofía, porqué de las decisiones
- `architecture.md` — estructura del sistema, stack, fases, plantillas de brief/retorno
- `project-log.md` — estado operativo actual
- `devlog.md` — historial de cambios y aprendizajes útiles

**Reversible:** La estructura de archivos sí. Fusionar dos archivos si resultan redundantes es trivial. El nombre Dashvis: pendiente de confirmar definitivamente.

---

*Las entradas se añaden en orden cronológico inverso (más reciente arriba).*