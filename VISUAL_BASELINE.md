---
title: OdontoFlow — Visual Baseline
status: active
last_verified: 2026-09-02
authority: Repo 0 (planning) — design reference, NOT a canonical UI specification
---

# Visual Baseline

## Author

**Leonardo Panduro** (`leonardopanduro-rgb`, `leonardo.panduro@utec.edu.pe`).

These screenshots are his design work, committed in `8769f12`
("Implement ODONTO SMART frontend", 2026-08-14) in
[ODONTO-SMART-FRONT](https://github.com/leonardopanduro-rgb/ODONTO-SMART-FRONT/tree/main/screenshots).

That commit is also the **foundation the canonical OdontoFlow frontend is built
on** — every canonical frontend commit sits on top of his work, not in place of
it. His repository is preserved untouched as the `leonardo` remote and has
never been force-pushed.

## What this is, and what it is not

**It is** the visual and interaction record of the frontend as Leonardo
designed it: the reference for what OdontoFlow is *supposed to look and feel
like*, screen by screen.

**It is not** a canonical UI specification and **must not replace the canonical
UI.** Where the canonical frontend has since diverged — because screens were
rewired to the real backend during M3 and M4 — the *code* is the truth about
current behaviour and this baseline is the truth about **design intent**. When
the two disagree, that is a design conversation, not a bug report.

## Preserved assets

Extracted from `leonardo/main`'s git object store — the originals, not
re-downloads or re-encodings. Verified byte-identical to what GitHub serves.

Location: `~/projects/portfolio/_preservation/odontoflow-contributors-2026-09-02/leonardo-visual-baseline/`

| Screen | File | Size | git blob | sha256 (first 16) |
|---|---|---|---|---|
| Agenda | `agenda.png` | 163 297 B | `7042a181b960` | `d369e20ea22de39c` |
| Agenda (mobile) | `agenda-mobile.png` | 38 953 B | `230cde73c5eb` | `69f9fc24e921f101` |
| Agente IA | `agente.png` | 248 821 B | `82323a2f2e4f` | `234cb0d197972bf3` |
| Caja | `caja.png` | 232 052 B | `8d9a6cf288ca` | `f086722af9110673` |
| Chat | `chat.png` | 291 834 B | `5c4e087bc74a` | `861a81426ca5db33` |
| Inventario | `inventario.png` | 234 496 B | `fe5ee874dc3f` | `25b2d3b3aaec1a3f` |
| Pacientes | `pacientes.png` | 227 897 B | `4a7c8de05d65` | `a822af46ef4b7526` |

Full checksums in that directory's `SHA256SUMS.txt` (**20 of 20 verified OK**).
Verify any time with:

```bash
cd ~/projects/portfolio/_preservation/odontoflow-contributors-2026-09-02
sha256sum -c SHA256SUMS.txt
```

The `git blob` column is the authoritative original identity: it is the hash
Leonardo's own commit recorded, and it matches what the GitHub API reports for
each file. Nothing was re-compressed.

## Coverage, and the two gaps

| Canonical screen | Baseline exists? |
|---|---|
| Agenda | ✅ desktop **and** mobile |
| Pacientes | ✅ |
| Caja | ✅ |
| Inventario | ✅ |
| Chat | ✅ |
| Agente IA | ✅ |
| **Asistente de voz** | ❌ **no baseline** — postdates this set (Alejandro's contribution, ported in V1) |
| **Synthetic Lab / Scenario config** | ❌ **no baseline** — does not exist yet |

`agenda-mobile.png` is the only mobile capture. Mobile intent for the other six
screens is therefore **unrecorded**, which matters because Alejandro's
operations simulator states plainly that its own design was optimised for
desktop. If mobile fidelity becomes a requirement, that is a gap to fill with
Leonardo, not something to infer from the desktop captures.

## How to use it

- **Before changing a canonical screen**, look at the corresponding capture and
  understand what was intended before overriding it.
- **When adding a screen** (the voice assistant, and next the Synthetic Lab),
  match this system rather than inventing a parallel one — which is exactly
  what Alejandro's voice view did by reusing `Badge` / `DataTable` / `Button`.
- **Do not** treat a divergence as automatic licence to "fix" the design.
  Record it and decide deliberately.

## Related

- Provenance and exact SHAs: [CONTRIBUTIONS.md](CONTRIBUTIONS.md)
- Contributor repository map: [REPOSITORIES.md](REPOSITORIES.md)
- Alejandro's separate operations simulator, which carries its **own** design
  language (a dark-header workstation, monospace numerics) and is a *different*
  visual lineage from this one:
  [SYNTHETIC_CLINIC_CONTRIBUTION_MAP.md](SYNTHETIC_CLINIC_CONTRIBUTION_MAP.md)
