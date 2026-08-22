# 14 · Timeline

A dated record, October–December 2025, reconstructed from certificate dates, file
timestamps and the capture times on my own screenshots. Where a date is inferred rather
than documented, I say so.

## Overview

```
 2025
 SEP  ──●── 15  Samsung Fellowship / shortlisting confirmed
        ●── 20  Registration and payment completed
 OCT  ──●── 04  Orientation session
        ●── 08  ══════ LEVEL 1 begins ══════
        ●── 26  Level 1 assessment preparation
        ●── 30  Level 1 certificates issued — 90%, 56.80th percentile
 NOV  ──●── 01  ══════ LEVEL 2 (+ hands-on) begins ══════
        ●── 06  TCAD environment setup guide issued
        ●── 22  ══════ ADVANCED LEVEL begins ══════
        ●── 23  First Advanced work session — 28 nm NMOS/PMOS structures, N-well diode
 DEC  ──●── 02  Main analysis session — device fields, cutlines, mixed-mode inverter
        ●── 11  Advanced project bundle staged for the local VM
        ●── 28  ══════ Program ends ══════  Level 2: 86% · Advanced: 92%, 93.06th pct
 2026
 JAN  ──●── 23  Advanced certificates issued
```

## Before the program

**15 September 2025 — fellowship confirmation.** Shortlisting and Samsung Fellowship award
confirmed by email. The fellowship is merit-based from the applicant pool; Grade II carries a
75% fee waiver across the Level 1 + Level 2 + Advanced bundle and the hands-on components.
This is what made taking the full pathway including hands-on viable, and the hands-on
components are where everything in this repository came from.

**20 September 2025 — registration completed.** Bundle registration and payment, with the
fellowship discount applied. *(The invoice is excluded from this repository — it contains
personal contact and transaction data. See [`../PROVENANCE.md`](../PROVENANCE.md).)*

**4 October 2025 — orientation.** Program orientation session covering structure, schedule,
tool access, assessment format and participation guidelines. Same date, I started collecting
background reading on semiconductor device physics — sensible preparation, given that Level 1
assumes the fundamentals and moves quickly.

## Level 1 — from 8 October 2025

**Foundations, on remote IISc compute.** Semiconductor device technology basics, what TCAD is,
and the TCAD-based technology design workflow. Practically: 2D device creation, a device
simulation, a bias sweep, an I-V curve. Tools introduced were Sentaurus Structure Editor,
Sentaurus Device, Sentaurus Workbench and Sentaurus Visual, running R-2020.09-SP1 on
`ancl2`/`ancl3.dese.iisc.ernet.in` over VNC.

The real content of this level is a mental model: a TCAD run is a geometry, a doping profile, a
model set, a numerical method and a bias schedule — and all five are choices. Nothing after
this makes sense without that.

**26 October 2025 — assessment preparation.** Revision ahead of the Level 1 evaluation,
working back through the concepts and the deck structure.

**30 October 2025 — Level 1 certificates issued.** **90%, 56.80th percentile.** As discussed in
[01 · Program overview](01-program-overview.md), a high mark at a modest percentile is what
Level 1 looks like: the material is largely definitional and the cohort is motivated.

## Level 2 (with hands-on) — from 1 November 2025

**Scripting, meshing, and physical models.** The certificate describes this level as covering
practical device structure creation through scripts, advanced device simulation and meshing
strategies, real-time device analysis, and physical models and model parameters. The Sentaurus
Script Editor is introduced here.

This is the level where the work becomes reproducible. A structure defined by a script can be
regenerated, parameterised and swept; a structure drawn by hand cannot. It is also where
meshing stops being a formality — two structures that differ only in their mesh can differ in
whether they converge at all, and one of them can be quantitatively wrong while looking fine.
Model selection starts being deliberate here too: doping-dependent mobility, high-field
saturation, transverse-field degradation, SRH with doping dependence, Auger, bandgap narrowing.

**6 November 2025 — TCAD environment setup guide issued.** The document that walks through
standing up the local toolchain. This is the point at which the program starts moving
participants off shared remote compute and onto their own machines, in preparation for the
Advanced level's process simulations.

## Advanced Level — from 22 November 2025

**23 November 2025 — first Advanced work session.** The earliest of my own captures, and a
sensible order to have worked in:

- `23:32` — the 28 nm **NMOS** structure on doping concentration
- `23:32` — the 28 nm **PMOS** structure, same scale for comparison
- `23:54` — **N-well diode** current density across a node array

Structures first, then the process-simulation output. Getting the structures up and confirming
they look physically right — wells where they should be, gate where it should be, source/drain
symmetric — before running any electrical analysis is the correct order, and it is the habit
that catches region-naming problems early (see [11 · Debugging log](11-debugging-log.md)).

**2 December 2025 — the main analysis session.** The densest evening in the record, and the
progression through it is the substance of the Advanced level:

| Time | What I was doing |
| --- | --- |
| `19:39` | Electron density across a gate-bias sweep — inversion layer forming |
| `19:39` | Same sweep with the **colour range pinned** so panels are comparable |
| `19:41` | **Conduction current density** over the same sweep |
| `19:55` | **Vertical cutline**, log scale — the inversion layer as a measurable profile |
| `20:01` | Mixed-mode inverter: the two `Device` blocks, NMOS and PMOS |
| `20:01` | The `Math` and `System` netlist — sources, load capacitor, instance wiring |
| `20:02` | The `Solve` schedule — DC ramp, then transient with `TurningPoints` |
| `21:28` | N-well diode current density as a **vector field** |

Read in order this is a coherent piece of work rather than a sequence of screenshots. Field
plots to see *where* things are, then a cutline to *measure* them, then up a level of
abstraction into circuit behaviour, then back to a field visualisation with a different
question in mind. The gap between the colour-range capture at `19:39` and the one immediately
before it is the moment I noticed that auto-scaled panels were not comparable — which is a
small methodological lesson with a timestamp on it.

**11 December 2025 — Advanced project bundle staged.** The Advanced course project database and
the VMware folder-import instructions carry this date on my machine, corresponding to preparing
the full local process-simulation environment. *(Timestamps place this after the sessions above;
I have not tried to reconstruct which environment each earlier session ran in, and I would
rather leave that open than guess.)*

**Through December — process simulation, calibration, and assessment.** The remainder of the
level covered the material listed on the certificate: 2D process simulations, 3D device
simulations, process development, mixed-mode simulation, frequency dependence, AC and thermal
analysis, RF device simulation, parameter extraction and model calibration basics — with
assignments through the hands-on component and a final evaluation.

**28 December 2025 — program ends.** The Samsung Fellowship award letter records the period as
8 October to 28 December 2025.

**Results.** Level 2: **86%, 73.04th percentile.** Advanced: **92%, 93.06th percentile.**

**23 January 2026 — Advanced certificates issued.** Participation and completion certificates
for the Advanced Level, signed by Samsung Semiconductor India Research, IISc and Synopsys.

## Reading the trajectory

The scores are 90 → 86 → 92. The percentiles are 56.80 → 73.04 → 93.06.

That divergence is the most informative thing in this timeline. A four-point *drop* in absolute
score from Level 1 to Level 2 corresponded to a sixteen-point *rise* in standing, because the
cohort spread out once the material required doing rather than reading. By the Advanced level —
process simulation, mixed-mode, calibration — the questions were no longer answerable from
lecture notes, and 92% placed at the 93rd percentile.

Six points of absolute score; thirty-six points of standing. The gap is the part that had to be
earned in front of the tool.

---

**Next:** [15 · Viva and interview notes](15-viva-and-interview-notes.md).
