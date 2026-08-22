# 13 · Skills and Concepts

A mapping from claim to evidence. The purpose of this chapter is that anyone reading my resume
should be able to arrive here and check any line of it.

## Skills, with honest levels

I use three levels deliberately, and I am stating what each means so the table is not
decorative.

- **Working** — I can do this independently on a new problem.
- **Familiar** — I can do this with reference to documentation or an existing example.
- **Exposed** — I have been taught it and assessed on it, but cannot show my own artefact.

### Tools

| Skill | Level | Evidence |
| --- | --- | --- |
| Sentaurus Workbench: projects, tool flows, parameters, split trees, node management | Working | [04](04-workbench-and-doe.md); node IDs in [screenshots](../screenshots/) |
| Sentaurus Visual: 2D fields, cutlines, multi-node overlays, fixed colour ranges, curve styling | Working | [All own-work screenshots](../screenshots/) |
| Sentaurus Device: deck structure, model selection, bias schedules, convergence control | Working | [07](07-structure-device-and-meshing.md), [08](08-mixed-mode-simulation.md) |
| Sentaurus Process: implant/diffuse/deposit/etch/CMP/anneal flows, STI, refinement | Familiar | [06](06-process-simulation.md); [screenshots/01](../screenshots/01-process-simulation/) |
| Sentaurus Structure Editor: regions, materials, contacts, analytic doping, refinement | Familiar | [07](07-structure-device-and-meshing.md) |
| Sentaurus Mesh: refinement boxes, interface and gradient-driven criteria, remeshing | Familiar | [07](07-structure-device-and-meshing.md) |
| Mixed-mode device + circuit co-simulation | Working | [08](08-mixed-mode-simulation.md); [screenshots/04](../screenshots/04-mixed-mode-cmos-inverter/) |
| Small-signal AC / C-V analysis | Familiar | [09](09-ac-transient-and-thermal.md), [10](10-calibration-and-extraction.md) |
| Electro-thermal and TLP/ESD analysis | Familiar | [09](09-ac-transient-and-thermal.md) |
| RF small-signal extraction (f<sub>T</sub>, f<sub>max</sub>, S-parameters) | Exposed | Curriculum coverage on Advanced certificate; no own figure |
| 3D structure generation and 3D simulation strategy | Exposed | Curriculum coverage; my own captures are 2D |

### Scripting and automation

| Skill | Level | Evidence |
| --- | --- | --- |
| Reading and modifying TCL-based `sprocess` / `sdevice` decks | Working | [05](05-scripting-tcl-scheme-swb.md), [08](08-mixed-mode-simulation.md) |
| Writing and adapting `svisual` TCL: plots, datasets, curves, styling, extraction | Working | [05](05-scripting-tcl-scheme-swb.md), [10](10-calibration-and-extraction.md) |
| Reading and modifying Scheme-based `sde` structure scripts | Familiar | [05](05-scripting-tcl-scheme-swb.md), [07](07-structure-device-and-meshing.md) |
| SWB preprocessing: `@param@`, node references, `#if` / `#noexec`, split trees | Working | [04](04-workbench-and-doe.md) |
| Parameter extraction via the `extract` library (`ExtractRdiff`) | Familiar | [10](10-calibration-and-extraction.md) |
| Debugging across the preprocessor / interpreter / tool boundary | Working | [11](11-debugging-log.md) |

### Environment and platform

| Skill | Level | Evidence |
| --- | --- | --- |
| Linux (RedHat) for EDA workflows: paths, environment, tool roots, X11 GUI tools | Working | [03](03-environment-setup.md) |
| VMware virtualisation: provisioning, shared folders, snapshots, resource sizing | Working | [03](03-environment-setup.md) |
| Remote lab access over VNC on shared institutional compute | Working | [03](03-environment-setup.md) |
| Installing and configuring a licensed EDA toolchain end to end | Working | [03](03-environment-setup.md) |

### Engineering method

| Skill | Level | Evidence |
| --- | --- | --- |
| Designing a parameter sweep / DOE and interpreting the result | Working | [04](04-workbench-and-doe.md) |
| Model validation against reference data; localising a discrepancy | Working | [10](10-calibration-and-extraction.md) |
| Systematic debugging: classify, read diagnostics, isolate, change one variable | Working | [11](11-debugging-log.md) |
| Scientific visualisation choices that preserve comparability | Working | [screenshots/03](../screenshots/03-device-simulation/) |
| Technical documentation of a simulation workflow | Working | This repository |

## Technical concepts I can explain

Grouped as I would want to be questioned on them. Each of these I can define, explain the
physical mechanism behind, and say why it matters in a simulation.

**Devices and physics.** MOS capacitor operation across accumulation, depletion and inversion ·
threshold voltage and what sets it · inversion layer formation · drift and diffusion transport ·
mobility degradation mechanisms and their regimes · velocity saturation · short-channel effects
(threshold roll-off, DIBL, punch-through) · the role of the halo implant · LDD and the field-peak
trade-off · series and contact resistance · SRH, Auger and radiative recombination · impact
ionisation and avalanche · bandgap narrowing under heavy doping · quantum confinement in thin
inversion layers · junction built-in potential and depletion width · CMOS inverter operation,
switching threshold, short-circuit current and dynamic power · parasitic bipolar action and
snapback · self-heating and thermal runaway.

**Process technology.** Ion implantation: dose, energy, tilt, rotation, channelling, straggle ·
analytic versus Monte-Carlo implant modelling · masking, and the difference between a layout mask
and a physical resist mask · diffusion and thermal budget · spike anneal and the
activation-versus-diffusion trade-off · thermal oxide growth versus deposition, and surface
consumption · STI: trench profile, liner, fill, CMP · well formation and multi-energy implants ·
well taps and substrate contacts · self-aligned gate patterning · spacer formation and its effect
on series resistance and overlap capacitance.

**Simulation and numerics.** Finite-element discretisation of the semiconductor equations · mesh
refinement strategy and gradient-driven criteria · why mesh quality determines convergence ·
Newton iteration, damping and convergence criteria · direct versus iterative linear solvers ·
block-structured systems · quasi-stationary bias ramping · backward-Euler transient integration ·
adaptive timestep control and forced refinement · coupled versus decoupled (Gummel) solution
schemes · mixed-mode device–circuit coupling · small-signal linearisation about an operating
point · calibration versus curve-fitting, and validation on held-out data.

## The three things I would want a reviewer to take away

**I can operate a professional TCAD flow end to end.** Environment from scratch, process
simulation, structure and mesh, device simulation, scripted post-processing, parameter
extraction. Not one tool — the chain.

**I understand what I am simulating.** Every model in a deck I ran, I can say what physical
mechanism it represents and why it belongs there. That is the difference between running a
simulation and doing one.

**I am careful about what I claim.** This repository separates my work from course material
explicitly, marks curriculum coverage separately from demonstrated work, and includes a
[debugging chapter](11-debugging-log.md) documenting things that went wrong. That is a
deliberate choice, and I would rather be checkable than impressive.

## Suggested resume phrasings

Statements I can defend line by line, at three lengths.

**One line.**

> Completed ISWDP Cohort 6 Advanced Level (IISc · Synopsys · Samsung), 92% / 93.06th
> percentile — Sentaurus TCAD process and device simulation, mixed-mode co-simulation, and model
> calibration. Samsung Fellowship, Grade II.

**Three lines.**

> **ISWDP Cohort 6 — Advanced Level** · IISc × Synopsys × Samsung Semiconductor India Research ·
> Oct–Dec 2025
> Semiconductor device and process simulation in the Synopsys Sentaurus TCAD suite: 28 nm CMOS
> process flows (`sprocess`), structure generation and meshing (`sde`/`snmesh`), device
> simulation with quantum-corrected drift-diffusion, mixed-mode device–circuit co-simulation of a
> CMOS inverter, small-signal C-V, electro-thermal transient analysis, and TCL-scripted
> post-processing and parameter extraction (`svisual`).
> Advanced Level 92% (93.06th percentile) · Level 2 86% · Level 1 90% · Samsung Fellowship,
> Grade II.

**What not to write.** I would avoid "developed TCAD simulation decks" — I modified and ran
instructor-supplied decks and wrote post-processing scripts, and that is what
[`../PROVENANCE.md`](../PROVENANCE.md) says. "Ran, modified, analysed and debugged" is accurate
and, for anyone who knows the tools, no less impressive.

---

**Next:** [14 · Timeline](14-timeline.md).
