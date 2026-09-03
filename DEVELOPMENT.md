# odontoflow-planning — DEVELOPMENT

## Qué es este repo

**El control plane de OdontoFlow ("Repo 0").** No tiene código de producto.
Es la fuente de verdad sobre en qué estado está el proyecto, qué se decidió y
por qué, y hacia dónde va cada actividad. Si te unes al proyecto, este es el
repo que lees primero.

## Los 5 repos del workspace

| Repo | Rol |
|---|---|
| **odontoflow-planning** (este) | control plane — estado, decisiones, briefs |
| `odontoflow-backend` | FastAPI + PostgreSQL — el núcleo determinista (agenda, clínica, economía, inventario) |
| `odontoflow-frontend` | React/Vite — la SPA real (Agenda/Pacientes/Caja/Inventario) |
| `odontoflow-voice` | servicio de voz standalone — transcripción + parser, sin LLM en las decisiones |
| `odontoflow-sim` | simulador de clínica sintética — motor de verdad de referencia para medición futura |

Todos son hermanos bajo `~/AI-EdgeRunners/odontoflow/`. MediStock es legado,
solo lectura, fuera de este workspace.

## Qué archivo leer para qué

| Necesitas saber... | Lee |
|---|---|
| Estado verificado ahora mismo (heads, tests, bloqueos) | `STATUS.md` |
| Qué hitos están cerrados y cuál es el actual | `PLAN.md` |
| Por qué se tomó cada decisión, con su evidencia | `CAVELOG.md` (las filas más nuevas están arriba) |
| Índice de todos los handoffs técnicos | `HANDOFFS.md` |
| Quién escribió qué, con qué SHA exacto | `CONTRIBUTIONS.md` |
| El diagnóstico más honesto y completo del proyecto hoy | `docs/handoffs/discovery/ODONTOFLOW_CTO_DISCOVERY_VERIFICATION.md` |
| El plan vivo de una actividad en curso | `docs/handoffs/plans/*.md` (uno por actividad, se actualiza mientras se trabaja) |

## Cómo se "desarrolla" este repo

No se escribe código acá. Se documenta:

1. **Antes de tocar cualquier repo de producto**, se abre (o se reusa) un
   living brief en `docs/handoffs/plans/<fecha>-<slug>.md` — objetivo,
   qué se va a construir, qué no, y cómo se va a verificar.
2. **Mientras se trabaja**, ese mismo documento se actualiza — no se crean
   documentos paralelos.
3. **Al terminar**, la decisión se registra como una fila nueva (arriba del
   todo) en `CAVELOG.md`, y `STATUS.md`/`PLAN.md`/`HANDOFFS.md` se actualizan
   si el estado verificado cambió.

Si usas Claude Code, el protocolo completo está en
`.claude/skills/foreman-handoff/SKILL.md` (también espejado en
`.agents/skills/foreman-handoff/`).

## Regla de oro

**Nunca declares algo REAL sin haberlo verificado tú mismo** (correr los
tests, leer el schema vivo, no solo la documentación). Esa es la razón por la
que este proyecto distingue tan explícitamente entre REAL / PARCIAL /
SIMULADO / FALTANTE en cada documento — léelo en
`ODONTOFLOW_CTO_DISCOVERY_VERIFICATION.md` para ver ese estándar aplicado a
todo el proyecto de una vez.
