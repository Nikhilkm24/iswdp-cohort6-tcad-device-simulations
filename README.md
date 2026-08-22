# ISWDP Cohort 6 — Advanced Level (TCAD / Semiconductor Device Simulation)

**India Semiconductor Workforce Development Program** · Indian Institute of Science (IISc) ·
Synopsys Inc., USA · Samsung Semiconductor India Research (SSIR)

![Advanced Level](https://img.shields.io/badge/Advanced%20Level-92%25%20%C2%B7%2093.06th%20percentile-0b7285)
![Level 2](https://img.shields.io/badge/Level%202-86%25%20%C2%B7%2073.04th%20percentile-1864ab)
![Level 1](https://img.shields.io/badge/Level%201-90%25%20%C2%B7%2056.80th%20percentile-1864ab)
![Samsung Fellowship](https://img.shields.io/badge/Samsung%20Fellowship-Grade%20II-1428a0)
![Toolchain](https://img.shields.io/badge/Synopsys%20Sentaurus%20TCAD-N--2017.09%20%2F%20R--2020.09--SP1-e8590c)

A technical record of my work through all three levels of ISWDP Cohort 6
(8 October – 28 December 2025), culminating in the **Advanced Level**: 2D process
simulation, 3D device simulation, mixed-mode circuit/device co-simulation, AC and
thermal analysis, parameter extraction and model calibration in the **Synopsys Sentaurus
TCAD** suite.

**Name on all certificates:** Nikhil KM · **Category:** Student ·
**Fellowship:** Samsung Fellowship, Grade II (merit-based fee waiver)

> **Read [`PROVENANCE.md`](PROVENANCE.md) first.** It states exactly which artefacts in
> this repository are my own work and which are instructor-supplied course material. The
> distinction is maintained consistently throughout, and no claim here is made without
> an artefact behind it.

---

## Contents

| | |
| --- | --- |
| [What ISWDP is](#what-iswdp-is) | The program, the partners, the four levels |
| [Verified outcome](#verified-outcome) | Scores, percentiles, dates, fellowship |
| [Tools I used](#tools-i-used) | Every Sentaurus tool, one line each |
| [Environment I built](#environment-i-built) | VM, remote hosts, tool versions |
| [What I actually did](#what-i-actually-did) | The flows I ran, level by level |
| [Screenshot gallery](#screenshot-gallery) | My own tool sessions, grouped and captioned |
| [Scripting](#scripting-what-the-languages-actually-are) | TCL vs Scheme, SWB parameterisation |
| [Key learnings](#key-learnings) | Physics, numerics, methodology |
| [Repository structure](#repository-structure) | Where everything lives |
| [Full documentation](#full-documentation) | The `docs/` chapters |

---

## What ISWDP is

The India Semiconductor Workforce Development Program is a joint industry–academia
training program run by the **Indian Institute of Science (IISc)** together with
**Synopsys Inc., USA** and **Samsung Semiconductor India Research (SSIR)**. It was
launched in March 2024 to build a trained talent pool for India's semiconductor
industry, and it teaches semiconductor technology through hands-on Technology CAD
(TCAD) rather than through theory alone: participants get licensed access to the
Synopsys Sentaurus suite and work directly with process and device simulation decks.

The program runs four cohorts a year and had over 1,500 participants across its first
three cohorts. It is structured as four levels:

- **Level 1** — semiconductor device technology basics, what TCAD is, the TCAD-based
  technology design workflow, basic 2D device creation, device simulation and analysis.
- **Level 2** — practical device structure creation through scripts, advanced device
  simulation and meshing strategies, real-time device analysis, physical models and
  model parameters.
- **Advanced** — 2D process simulation, 3D device simulation, process development,
  mixed-mode simulation, frequency dependence, AC and thermal analysis, RF device
  simulation, parameter extraction and model calibration basics.
- **Custom** — bespoke tracks for industry participants.

Each level has a live virtual component and an optional hands-on component with
assignments and an assessed final evaluation. I took **Level 1, Level 2 (with hands-on)
and Advanced**, which is the full student pathway.

Official program site: **<https://iisc-iswdp.org>**
*(sourced from the program's own brochure and registration material — see
[`PROVENANCE.md`](PROVENANCE.md#known-gaps-flagged-rather-than-filled))*

## Verified outcome

Every figure below is taken verbatim from a certificate in
[`certificates/`](certificates/), so each claim can be checked against its source
document without leaving this repository.

| Level | Started | Result | Percentile | Certificate |
| --- | --- | --- | --- | --- |
| Level 1 | 8 October 2025 | **90%** | 56.80 | [participation](certificates/01-level-1-participation.pdf) · [completion](certificates/02-level-1-completion-90pct.pdf) |
| Level 2 (+ hands-on) | 1 November 2025 | **86%** | 73.04 | [participation](certificates/03-level-2-participation.pdf) · [completion](certificates/04-level-2-completion-86pct.pdf) · [hands-on](certificates/05-level-2-hands-on-completion.pdf) |
| **Advanced** | **22 November 2025** | **92%** | **93.06** | [participation](certificates/06-advanced-participation.pdf) · [completion](certificates/07-advanced-completion-92pct.pdf) |
| Samsung Fellowship | 8 Oct – 28 Dec 2025 | **Grade II** | — | [award](certificates/08-samsung-fellowship-grade-ii.pdf) |

The Advanced completion certificate is signed by **Rajesh Krishnan** (Senior Vice
President & Managing Director, Samsung Semiconductor India Research), **Prof. Mayank
Shrivastava** (Program Director, IISc) and **Dr. Patrick Haspel** (Senior Director,
Synopsys Academic & Research Alliances).

The **Samsung Fellowship** is awarded on merit from the applicant pool and carries a
75% fee waiver across the Level 1 + Level 2 + Advanced bundle and a 75% waiver on the
Level 2 and Advanced hands-on components. Grade II is the second of the fellowship
grades.

## Tools I used

Every tool listed here is one I ran myself; each appears in the coursework I executed or
in a screenshot in this repository.

| Tool | Executable | What I used it for |
| --- | --- | --- |
| **Sentaurus Workbench** | `swb` | The framework that ties the flow together: project trees, tool sequences, `@param@` substitution, DOE split trees, per-node run management and status. Everything else runs underneath it. |
| **Sentaurus Process** | `sprocess` | Physical process simulation — implantation, diffusion, oxidation, deposition, etch, CMP, anneal — building a device structure the way a fab would, step by step, rather than drawing it. |
| **Sentaurus Structure Editor** | `sde` | Geometric structure creation and editing, region/material/contact definition, and mesh-refinement setup. Driven by a Scheme command file, not TCL. |
| **Sentaurus Mesh** | `snmesh` | Meshing/remeshing the structure — refinement boxes, interface refinement, doping-gradient-driven element sizing. Invoked from `sde` or as its own SWB tool. |
| **Sentaurus Device** | `sdevice` | The electrical solver: drift-diffusion with quantum correction, mobility/recombination model selection, DC sweeps, small-signal AC and C-V, transient and electro-thermal analysis, and mixed-mode device+circuit solves. |
| **Sentaurus Visual** | `svisual` | Post-processing: 2D field plots, cutlines, I-V and C-V curves, multi-node overlays, and TCL-scripted automatic plotting and parameter extraction. |
| **Sentaurus Script Editor / jEdit** | — | Editing command files with Sentaurus syntax awareness; where I read and modified the decks. |

Each tool has its own chapter in [`docs/02-tools-and-toolchain.md`](docs/02-tools-and-toolchain.md).

## Environment I built

Two environments, because the program uses both:

**IISc remote compute (Levels 1–2).** Sentaurus **R-2020.09-SP1** on IISc's
`ancl2` / `ancl3.dese.iisc.ernet.in` hosts, accessed over VNC. Licensed, pre-configured,
shared — the constraint here is that you are one user among many on a scheduled resource,
so you learn to plan runs rather than poke at them.

**Local VM (Advanced).** For the Advanced level the program distributes a full
pre-built simulation appliance:

- VMware Player 17.5.2 (build 23775571) on Windows, with VMware Workstation 15 as the
  fallback path
- Guest: **RedHat Advanced Server 6.6**
- Guest toolchain: Synopsys Sentaurus TCAD **N-2017.09 / N-2017.09-SP2** under
  `/opt/STROOT/TCAD2017/`
- Project database: `/home/sentaurus/STDB/projects/`

Getting this working end to end — importing the appliance, mounting the shared folder to
move the project bundle into the guest, resolving the licence path, and confirming that
`sprocess`, `sde`, `sdevice` and `svisual` all launched — was the first real task of the
Advanced level and is written up in
[`docs/03-environment-setup.md`](docs/03-environment-setup.md).

## What I actually did

The short version, in the order it happened. The long version, with commands, physics and
failure modes, is in [`docs/`](docs/).

**Level 1 — 2D device creation and simulation.** Build a simple 2D structure, define
contacts, run a drift-diffusion solve, sweep a terminal, look at the I-V curve, and
understand what each block of an `sdevice` command file is for (`Electrode`, `File`,
`Physics`, `Plot`, `Math`, `Solve`). This is where the mental model forms: a TCAD run is
a geometry, a doping profile, a physics model set, a numerical method and a bias
schedule, and every one of those five is something you choose.

**Level 2 — scripted structures, meshing, model parameters.** Move from clicking to
scripting: create structures from `sde` command files, control the mesh deliberately
(refinement windows, interface refinement, doping-gradient criteria), and start
selecting physical models on purpose — doping-dependent mobility, high-field saturation,
normal-field degradation at the interface, SRH with doping dependence, Auger,
band-gap narrowing. Also where meshing stops being a formality: a structure that
converges and a structure that does not often differ only in their mesh.

**Advanced — process simulation, 3D, mixed-mode, AC/transient, extraction, calibration.**

- **Process simulation (`sprocess`)** of an N-well diode and a 28 nm NMOS capacitor
  flow: STI formation (trapezoidal etch, liner, fill, CMP), well implants, Vt and halo
  implants, screening oxide, gate stack and poly patterning, LDD and N+/P+ source/drain,
  spike anneal, with Monte-Carlo implant and `AdvancedCalibration` in play, and
  `refinebox`/`remesh` used to keep the grid honest as the structure changes.
- **3D structures and emulation**: 3D doping, topology, curved and cornered geometry,
  and the simulation-strategy question of when 3D is worth its cost.
- **Device simulation**: DC transfer and output characteristics with quantum-corrected
  drift-diffusion, current-density and carrier-density field analysis, vertical cutlines
  through the channel.
- **Mixed-mode**: a CMOS inverter built as two `sdevice` device instances wired into a
  netlist with sources and a load capacitor, DC-ramped to V<sub>DD</sub> and then run as
  a transient with `TurningPoints` refinement around the switching edges.
- **AC / C-V**: small-signal `ACCoupled` analysis at 1 MHz to get capacitance versus
  bias, which is the measurement that actually constrains a calibration.
- **Transient / thermal**: `Transient(BE)` electro-thermal solves with a thermode and
  surface resistance for TLP/ESD-style stress.
- **Parameter extraction**: `svisual` TCL using the `extract` library — for example
  on-resistance from an I<sub>d</sub>-V<sub>d</sub> curve via `ext::ExtractRdiff` at a
  fixed drain bias.
- **Calibration**: comparing simulated transfer, output and C-V characteristics against
  reference PDK data and understanding which model parameters are the ones that move the
  discrepancy.

A day-by-day timeline is in [`docs/14-timeline.md`](docs/14-timeline.md).

## Screenshot gallery

These are captures of **my own** tool sessions, grouped by what they show. Full-size
images and per-image notes are in each folder's README; the folder pages carry the
detailed commentary.

### 1 · Process simulation — N-well diode

[`screenshots/01-process-simulation/`](screenshots/01-process-simulation/)

| | |
| --- | --- |
| <a href="screenshots/01-process-simulation/nwell-diode-current-density-node-array.png"><img src="screenshots/01-process-simulation/nwell-diode-current-density-node-array.png" width="380"></a> | <a href="screenshots/01-process-simulation/nwell-diode-current-density-vector-field.png"><img src="screenshots/01-process-simulation/nwell-diode-current-density-vector-field.png" width="380"></a> |
| **Node array, current density.** Several nodes of the N-well diode split laid out side by side in Sentaurus Visual so the effect of the process split can be compared at a glance instead of one plot at a time. | **Current density as a vector field.** The same structure rendered with direction as well as magnitude, which is what shows you *where* the conduction path actually runs through the well. |

### 2 · Device structures — 28 nm NMOS / PMOS

[`screenshots/02-device-structures/`](screenshots/02-device-structures/)

| | |
| --- | --- |
| <a href="screenshots/02-device-structures/nmos-28nm-doping-concentration-structure.png"><img src="screenshots/02-device-structures/nmos-28nm-doping-concentration-structure.png" width="380"></a> | <a href="screenshots/02-device-structures/pmos-28nm-doping-concentration-structure.png"><img src="screenshots/02-device-structures/pmos-28nm-doping-concentration-structure.png" width="380"></a> |
| **28 nm NMOS, doping concentration.** The structure I used for the inverter work, shown on the signed doping scale so wells, halo, LDD and source/drain are all readable in one view. | **28 nm PMOS, doping concentration.** The complementary device. Comparing the two side by side is how the inverter's asymmetry — and hence the `AreaFactor` ratio — stops being an abstraction. |

### 3 · Device simulation — fields under bias

[`screenshots/03-device-simulation/`](screenshots/03-device-simulation/)

| | |
| --- | --- |
| <a href="screenshots/03-device-simulation/nmos-28nm-edensity-gate-bias-sweep.png"><img src="screenshots/03-device-simulation/nmos-28nm-edensity-gate-bias-sweep.png" width="250"></a> | <a href="screenshots/03-device-simulation/nmos-28nm-edensity-fixed-colour-range.png"><img src="screenshots/03-device-simulation/nmos-28nm-edensity-fixed-colour-range.png" width="250"></a> | <a href="screenshots/03-device-simulation/nmos-28nm-edensity-vertical-cutline-log.png"><img src="screenshots/03-device-simulation/nmos-28nm-edensity-vertical-cutline-log.png" width="250"></a> |
| **Electron density across a gate-bias sweep.** Channel inversion forming, panel by panel. | **Same sweep, colour range pinned.** Auto-scaling makes every panel look the same; fixing the range is what makes the comparison mean something. | **Vertical cutline, log scale.** Carrier density from the oxide down into the bulk — the inversion layer as a profile rather than a picture. |

A fourth figure in this group shows conduction current density over the same sweep.

### 4 · Mixed-mode — CMOS inverter

[`screenshots/04-mixed-mode-cmos-inverter/`](screenshots/04-mixed-mode-cmos-inverter/)

| | |
| --- | --- |
| <a href="screenshots/04-mixed-mode-cmos-inverter/sdevice-inverter-nmos-pmos-device-blocks.png"><img src="screenshots/04-mixed-mode-cmos-inverter/sdevice-inverter-nmos-pmos-device-blocks.png" width="250"></a> | <a href="screenshots/04-mixed-mode-cmos-inverter/sdevice-inverter-math-system-netlist.png"><img src="screenshots/04-mixed-mode-cmos-inverter/sdevice-inverter-math-system-netlist.png" width="250"></a> | <a href="screenshots/04-mixed-mode-cmos-inverter/sdevice-inverter-solve-transient-turningpoints.png"><img src="screenshots/04-mixed-mode-cmos-inverter/sdevice-inverter-solve-transient-turningpoints.png" width="250"></a> |
| **Two `Device` blocks.** NMOS and PMOS declared as separate device instances, each with its own grid, workfunction parameter and `AreaFactor`. | **`Math` and `System`.** The netlist: pulse source, supply, load capacitor, and the instances wired `in`→gates, `out`→drains. | **`Solve` with `TurningPoints`.** DC ramp to V<sub>DD</sub> first, then a transient with the timestep tightened around the switching edges. |

The full deck is walked through line by line in
[`docs/08-mixed-mode-simulation.md`](docs/08-mixed-mode-simulation.md).

### Reference figures (course material, not mine)

[`reference/`](reference/) holds four figures shipped with the course project bundle: the
2D NMOS process cross-section, and the transfer, output and C-V calibration comparisons
against reference PDK data. They are here because they are the clearest illustration of
what calibration means in practice, and they are labelled as course material wherever
they appear.

## Scripting: what the languages actually are

This is worth being precise about, because it is a common thing to get wrong on a resume.

**Sentaurus command files are not all one language.** `sprocess` and `sdevice` command
files are interpreted by an embedded **TCL** interpreter, so a process deck can use
`set`, `expr`, `if`, `foreach` and procedures alongside the tool's own commands. Sentaurus
Structure Editor command files (`sde_dvs.cmd`) are **Scheme**, not TCL. Sentaurus Visual
scripts (`svisual_vis.tcl`) are genuine TCL.

**What I can do with it:** read and modify process/device decks; use TCL control flow and
variables to parameterise a deck; write and adapt `svisual` TCL to build plots
programmatically, assign colours by node index, load `.plt` datasets, set axis and legend
properties, and call the `extract` library to pull a parameter out of a curve. For
example, the on-resistance extraction pattern the course teaches is:

```tcl
load_library extract
set Vds [get_variable_data "Drain OuterVoltage" -dataset PLT_IdVd($N)]
set Ids [get_variable_data "Drain TotalCurrent"  -dataset PLT_IdVd($N)]
ext::ExtractRdiff out= Ron name= "Ron" v= $Vds i= $Ids vo= 0.3
```

*(excerpt from the course-supplied `svisual_vis.tcl`; see [`PROVENANCE.md`](PROVENANCE.md))*

**On top of TCL, Sentaurus Workbench has its own preprocessing layer**, which is the part
that makes parameter studies tractable: `@param@` placeholders substituted per node,
`@node@` and `@node:index@` for node identity, `@previous@` and `@node|-1@` to reach the
preceding node's outputs, `@tdr|nmos@`-style scoped references into a split tree, and
`#if @CV@ == 0 / #noexec / #endif` conditionals that switch whole blocks or skip a tool
for a given node. A design-of-experiments tree in `gtree.dat` then expands into hundreds
of nodes, each with its own generated command file.

Understanding the *order* here matters: SWB preprocesses the file, then TCL interprets the
result, then the tool acts on the commands. Most confusing errors in a deck come from
getting that layering wrong.

Full treatment: [`docs/05-scripting-tcl-scheme-swb.md`](docs/05-scripting-tcl-scheme-swb.md).

## Key learnings

**Process determines device.** The single biggest shift from Level 1 to Advanced is that
you stop drawing a device and start manufacturing it. A halo implant's dose, energy, tilt
and rotation are not annotations on a structure — they are the reason the short-channel
behaviour comes out the way it does. Once you have run the same device through a process
split tree and watched the electrical characteristics move, "process/device co-design"
stops being a phrase.

**Model selection is an engineering decision, not a checkbox.** `Mobility(DopingDep
HighFieldSaturation Enormal)` is three separate physical statements about your device.
Adding `eQuantumPotential` because the inversion layer in a 28 nm device is thin enough
that classical density is wrong is a decision you justify. And the tool will silently
substitute defaults for models undefined in a material unless you ask it not to — which
is why `-CheckUndefinedModels` exists and why I now read the `.err` file before the
`.plt` file.

**Convergence is part of the physics.** `Coupled` versus `Plugin`, `Method=Blocked` with
`SubMethod=ParDiSo` for a multi-device system, `ILS` for large problems, damping and
iteration limits, ramping in stages instead of jumping to the target bias, and
`TurningPoints` to spend timesteps where the transient is actually moving. A solve that
does not converge is usually telling you something about the mesh or the bias schedule,
not about the solver.

**Meshing is where most simulations are won or lost.** Refinement boxes at junctions and
interfaces, `MaxLenInt` at material boundaries, doping-gradient-driven sizing, and
remeshing after structural change. Too coarse and the answer is wrong; too fine and it
never finishes.

**Calibration is the point of all of it.** A simulation that does not match measured data
is a hypothesis. Lining up simulated I<sub>d</sub>-V<sub>g</sub>, I<sub>d</sub>-V<sub>d</sub>
and C-V against reference data, and knowing which parameter to move to close which gap,
is the difference between running a tool and doing TCAD.

**Read the error file.** Almost every hour I lost, I lost to something that was written
plainly in an `.err` or `.log` file I had not opened. That habit — check status, open the
node's error output, read the actual warning, then form a theory — was probably the most
transferable thing the Advanced level taught me.

More, with specifics: [`docs/12-key-learnings.md`](docs/12-key-learnings.md) and
[`docs/11-debugging-log.md`](docs/11-debugging-log.md).

## Repository structure

```
iswdp-cohort6-tcad-device-simulations/
├── README.md                     ← you are here
├── PROVENANCE.md                 ← what is mine vs. course material (read this)
├── LICENSE                       ← CC BY 4.0, my documentation only
├── docs/
│   ├── 01-program-overview.md            The program, levels, fellowship
│   ├── 02-tools-and-toolchain.md         Every Sentaurus tool, in detail
│   ├── 03-environment-setup.md           VM, remote hosts, licensing, first launch
│   ├── 04-workbench-and-doe.md           SWB projects, parameters, split trees
│   ├── 05-scripting-tcl-scheme-swb.md    TCL vs Scheme vs SWB preprocessing
│   ├── 06-process-simulation.md          sprocess flows, step by step
│   ├── 07-structure-device-and-meshing.md  sde / snmesh / sdevice; models, mesh
│   ├── 08-mixed-mode-simulation.md       CMOS inverter device+circuit co-simulation
│   ├── 09-ac-transient-and-thermal.md    C-V, small-signal AC, electro-thermal
│   ├── 10-calibration-and-extraction.md  PDK comparison, Ron extraction
│   ├── 11-debugging-log.md               Real errors, real diagnoses, real fixes
│   ├── 12-key-learnings.md               Physics and methodology, consolidated
│   ├── 13-skills-and-concepts.md         Skills gained, mapped to evidence
│   ├── 14-timeline.md                    Chronological record, Oct–Dec 2025
│   └── 15-viva-and-interview-notes.md    Q&A prep on everything above
├── screenshots/                  ← my own tool sessions, grouped + captioned
│   ├── 01-process-simulation/
│   ├── 02-device-structures/
│   ├── 03-device-simulation/
│   └── 04-mixed-mode-cmos-inverter/
├── reference/                    ← course-supplied figures, clearly labelled
└── certificates/                 ← all 8 credential PDFs
```

## Full documentation

If you have five minutes, read this README and skim
[`docs/12-key-learnings.md`](docs/12-key-learnings.md).

If you are evaluating depth, the three chapters that carry the most technical weight are
[`docs/06-process-simulation.md`](docs/06-process-simulation.md),
[`docs/08-mixed-mode-simulation.md`](docs/08-mixed-mode-simulation.md) and
[`docs/11-debugging-log.md`](docs/11-debugging-log.md).

If you are checking credentials, everything in
[Verified outcome](#verified-outcome) links to the PDF it came from.

To read it offline:

```bash
git clone https://github.com/Nikhilkm24/iswdp-cohort6-tcad-device-simulations.git
```

---

## Licence and attribution

My documentation, captions and analysis in this repository are released under
[CC BY 4.0](LICENSE).

The Synopsys Sentaurus TCAD suite is commercial software; I used it under the academic
licence provided through the program. Sentaurus, Synopsys and the course materials are
the property of Synopsys, Inc. The ISWDP curriculum and its reference project database
are the property of IISc / Synopsys / Samsung Semiconductor India Research. Nothing in
this repository redistributes their software, their slides or their project files — see
[`PROVENANCE.md`](PROVENANCE.md).
