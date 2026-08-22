# 01 · Program Overview

> Facts in this chapter come from three primary sources: the official ISWDP program
> brochure, my eight certificates (in [`../certificates/`](../certificates/)), and the
> fellowship award letter. Where a figure is quoted, it is quoted from the document, not
> from memory.

## What ISWDP is

The **India Semiconductor Workforce Development Program (ISWDP)** is a joint
industry–academia training program created to address a specific bottleneck: India has
committed heavily to semiconductor manufacturing and design, and the constraint is not
capital or intent but the number of engineers who have actually touched production-grade
semiconductor tooling. Reading about MOSFET physics and having simulated a 28 nm MOSFET
you built yourself from a process deck are very different states of knowledge, and the
second one is what the industry needs.

The program is delivered by three parties, each contributing what it has:

- **Indian Institute of Science (IISc), Bengaluru** — academic ownership and delivery.
  The program is run out of IISc's Department of Electronic Systems Engineering, with
  **Prof. Mayank Shrivastava** as Program Director. IISc provides the curriculum, the
  instructors, and remote compute access for the earlier levels.
- **Synopsys Inc., USA** — the toolchain. Participants work in the real **Sentaurus
  TCAD** suite, not a teaching simulator, under academic licence. Synopsys's Academic &
  Research Alliances group (**Dr. Patrick Haspel**, Senior Director) co-signs the
  completion certificates.
- **Samsung Semiconductor India Research (SSIR)** — industry sponsorship, including the
  **Samsung Fellowship** that funds participation on merit. Certificates are co-signed
  by SSIR's Managing Director.

The program launched in **March 2024** and runs **four cohorts per year**. Across its
first three cohorts it trained over **1,500 participants**. I was in **Cohort 6**.

## The four levels

ISWDP is deliberately laddered. Each level assumes the previous one and adds a layer of
either capability or realism, and the assessment at each level gates the next.

**Level 1 — foundations (≈10 hours, one week).** Semiconductor device technology basics,
what Technology CAD is and why it exists, and the TCAD-based technology design workflow.
Practically: basic 2D device creation, device simulation and analysis. Tools introduced
are Sentaurus Structure Editor, Sentaurus Device, Sentaurus Workbench and Sentaurus
Visual. This level exists to make the tool stop being intimidating.

**Level 2 — scripting, meshing and physics (≈15 hours, three weekends).** Practical
device structure creation *through scripts* rather than through the GUI, advanced device
simulation and meshing strategies, real-time device analysis, and — the substantive part
— physical models and model parameters. Adds the Sentaurus Script Editor. This is where
the work becomes reproducible: a structure defined by a script can be regenerated,
parameterised and swept, and a structure drawn by hand cannot.

**Advanced — process, 3D, mixed-mode, AC/thermal, extraction, calibration (≈20 hours,
four weekends).** My certificate states the coverage precisely:

> *2D Process Simulations, 3D Device Simulations, Process Development, Mixed-mode
> Simulations, Frequency Dependence, AC and Thermal analysis, RF Device Simulations,
> Parameter Extraction, and Model Calibration Basics.*

The official module breakdown for this level is organised as **Process Design**,
**Advanced Emulations** (3D structures, simulation strategy, 3D doping, and handling
topologies, curves, edges and corners) and **Device Calibration** (bringing a simulated
structure close to a real fabricated device: calibration basics, model selection,
identifying the operating regime, and knowing which model parameters are the critical
ones). Adds **Sentaurus Process** and **scripting in Sentaurus Visual** to the toolset.

**Custom** — a fourth track offered to industry participants only, scoped per
organisation. Not applicable to me.

Each level is delivered as live virtual sessions, with an optional **hands-on** component
carrying additional assignments, and each ends in an assessed **final evaluation** that
produces both a percentage score and a percentile against the cohort.

## The pathway I took

I completed the full student pathway: **Level 1 → Level 2 with hands-on → Advanced**.

| Level | Start date | Score | Percentile |
| --- | --- | --- | --- |
| Level 1 | 8 October 2025 | 90% | 56.80 |
| Level 2 (with hands-on) | 1 November 2025 | 86% | 73.04 |
| **Advanced** | **22 November 2025** | **92%** | **93.06** |

The percentile column is the more informative one, and the trajectory across it is the
thing I would point to. A 90% at Level 1 placed me in the 56.8th percentile — that is,
Level 1 is a level almost everyone does well on, because it is largely definitional and
the cohort is motivated. Level 2 introduces scripting, meshing and model selection, and
the cohort spreads out: 86% — four points *lower* — moved me from the 57th to the 73rd
percentile. The Advanced level is where the material stops being learnable by reading, and
92% put me at the **93.06th percentile**. The absolute scores moved by six points; the
standing moved by thirty-six percentile points, because the questions got harder to answer
without having actually run the simulations.

## The Samsung Fellowship

The **Samsung Fellowship** is a merit-based award made from the ISWDP applicant pool. I
was awarded **Grade II**, covering the period **8 October 2025 to 28 December 2025** —
the full span of my three levels.

Grade II carries a **75% fee waiver** on the Level 1 + Level 2 + Advanced bundle, and a
75% waiver on the Level 2 hands-on and Advanced hands-on components, applied as a
discount code against the bundle package. In practical terms the fellowship is what made
taking all three levels including hands-on feasible; the hands-on components are the
expensive part and also the part that produced everything in this repository.

The award letter and the fellowship certificate are in
[`../certificates/08-samsung-fellowship-grade-ii.pdf`](../certificates/08-samsung-fellowship-grade-ii.pdf).

## Certificate signatories

Worth recording, because it indicates who stands behind the credential:

| Certificate | Signatories |
| --- | --- |
| Level 1 completion | Balajee Sowrirajan (Corporate EVP & MD, SSIR); Prof. Mayank Shrivastava (Program Director, IISc); Dr. Patrick Haspel (Senior Director, Synopsys Academic & Research Alliances) |
| Advanced completion | Rajesh Krishnan (SVP & MD, SSIR); Prof. Mayank Shrivastava (Program Director, IISc); Dr. Patrick Haspel (Senior Director, SARA, Synopsys) |

## Why this program is worth a repository

Two reasons, and they are different from each other.

The first is that TCAD is a genuinely gated skill. The software is expensive, the licences
are institutional, and the domain knowledge needed to get a meaningful answer out of it is
not something you can pick up from documentation alone. Most electronics graduates have
never opened a process simulator. Having built a 28 nm NMOS from an implant-and-anneal
sequence, simulated it, compared it against reference PDK data and understood why they
disagreed is a specific, checkable, uncommon thing.

The second is that the program teaches a *method*, and the method transfers. Define the
physical problem, choose a model set and justify the choice, control the discretisation,
solve in a numerically sensible order, compare against measurement, and iterate on the
discrepancy. That loop is the whole of computational engineering. TCAD is just where I
learned it.

---

**Next:** [02 · Tools and toolchain](02-tools-and-toolchain.md) —
every Sentaurus tool I used and what it is actually for.
