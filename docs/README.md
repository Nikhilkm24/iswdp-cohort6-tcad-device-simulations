# Documentation

Fifteen chapters, written to be read in order but each self-contained. Together they are the
detailed technical record behind the summary in [`../README.md`](../README.md).

## Chapters

| # | Chapter | What it covers |
| --- | --- | --- |
| 01 | [Program overview](01-program-overview.md) | What ISWDP is, the four levels, the pathway I took, the Samsung Fellowship, and how to read the score/percentile trajectory |
| 02 | [Tools and toolchain](02-tools-and-toolchain.md) | Every Sentaurus tool I used — Workbench, Process, Structure Editor, Mesh, Device, Visual — what each is for and what I did with it |
| 03 | [Environment setup](03-environment-setup.md) | The VMware/RedHat VM, the IISc remote hosts, tool roots and licensing, and the sanity checks that saved time |
| 04 | [Workbench and DOE](04-workbench-and-doe.md) | SWB projects, `@param@` substitution, node trees, `#if`/`#noexec`, and running a parameter study without wasting a weekend |
| 05 | [Scripting: TCL, Scheme and SWB](05-scripting-tcl-scheme-swb.md) | What each command file's language actually is, and an annotated `svisual` automation script |
| 06 | [Process simulation](06-process-simulation.md) | The 28 nm NMOS flow step by step: STI, wells, Vt and halo implants, gate stack, LDD, source/drain, spike anneal |
| 07 | [Structure, meshing and device simulation](07-structure-device-and-meshing.md) | Emulation vs. process simulation, why meshing decides everything, `sdevice` deck anatomy, and physics model selection |
| 08 | [Mixed-mode simulation](08-mixed-mode-simulation.md) | The CMOS inverter: two meshed devices in a circuit netlist, walked through line by line |
| 09 | [AC, transient and thermal](09-ac-transient-and-thermal.md) | Small-signal C-V and why it constrains a model, transient integration, electro-thermal coupling, TLP/ESD |
| 10 | [Calibration and extraction](10-calibration-and-extraction.md) | Pulling numbers out of curves, comparing against PDK reference data, and reading a discrepancy as a diagnosis |
| 11 | [Debugging log](11-debugging-log.md) | Real error messages, what each meant, and what I changed — including the silent-wrong-answer case |
| 12 | [Key learnings](12-key-learnings.md) | Physics, numerics and methodology, consolidated |
| 13 | [Skills and concepts](13-skills-and-concepts.md) | Every skill claimed, with an honest level and a link to its evidence |
| 14 | [Timeline](14-timeline.md) | Dated record, September 2025 to January 2026 |
| 15 | [Viva and interview notes](15-viva-and-interview-notes.md) | The questions I should be able to answer, and my answers |

## Suggested reading paths

**If you have ten minutes and want to judge the technical depth:**
[08 · Mixed-mode simulation](08-mixed-mode-simulation.md), then
[11 · Debugging log](11-debugging-log.md).

**If you want to know what I actually understand:**
[12 · Key learnings](12-key-learnings.md), then
[10 · Calibration and extraction](10-calibration-and-extraction.md).

**If you are checking claims:** [13 · Skills and concepts](13-skills-and-concepts.md) maps every
claim to its evidence, and [`../PROVENANCE.md`](../PROVENANCE.md) states what is mine and what is
course material.

**If you are new to TCAD entirely:** start at [02 · Tools and toolchain](02-tools-and-toolchain.md),
which is written for exactly that reader.

## A note on how these were written

Each chapter explains what I did, why that choice was made, and what I would do differently. Where
a claim rests on an artefact, it links to the artefact. Where something is curriculum I was assessed
on but cannot show my own figure for — full RF extraction, 3D work — it is marked as such rather
than blurred into the rest. That is the standard [`../PROVENANCE.md`](../PROVENANCE.md) sets and the
one these chapters try to hold to.
