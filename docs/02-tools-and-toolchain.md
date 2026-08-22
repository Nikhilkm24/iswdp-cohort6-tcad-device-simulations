# 02 · Tools and Toolchain

Every tool documented here is one I ran myself. This chapter is written for a reader who
knows electronics but has never opened a TCAD tool, because that is the most common gap —
people know what a MOSFET is and have no picture of how one gets simulated.

## The mental model first

A TCAD flow answers one question: *given a manufacturing recipe, what will the resulting
device do electrically?* Answering it takes four stages, and the Sentaurus tools map onto
those stages almost one to one.

```
     RECIPE                 STRUCTURE              PHYSICS               MEANING
  ┌────────────┐         ┌────────────┐        ┌────────────┐        ┌────────────┐
  │  implant   │         │ geometry + │        │  Poisson + │        │  I-V, C-V, │
  │  diffuse   │  ────▶  │  doping +  │ ────▶  │  continuity│ ────▶  │  fields,   │
  │  oxidise   │         │  mesh      │        │  solved    │        │  extracted │
  │  etch      │         │            │        │  on mesh   │        │  parameters│
  └────────────┘         └────────────┘        └────────────┘        └────────────┘
    sprocess              sde + snmesh            sdevice               svisual
                                                                        
  ══════════════════ all orchestrated by Sentaurus Workbench (swb) ═══════════════
```

Two routes exist into the structure stage, and knowing when to use which is part of the
skill. **Process simulation** (`sprocess`) derives the structure physically from the
recipe — slow, but it predicts things you did not put in, like the actual junction depth
after thermal budget. **Structure editing / emulation** (`sde`) constructs the structure
geometrically with analytic doping profiles — fast, controllable, and the right choice
when you care about electrical behaviour rather than about the process itself. The
Advanced level teaches both and, more importantly, teaches the trade-off.

---

## Sentaurus Workbench (`swb`)

**What it is.** The framework everything else runs inside. A project in SWB is a *tool
flow* (an ordered chain such as `sprocess → sde → sdevice → svisual`) plus a *parameter
set*, and SWB's job is to expand that into a tree of concrete runs, execute them, and
track the state of each one.

**Why it matters more than it looks.** Without SWB, a parameter study means hand-editing a
deck, renaming output files, and remembering which run was which — which is how results
get mixed up. SWB replaces that with structure: you declare a parameter, give it a list of
values, and SWB generates one *node* per combination, each with its own preprocessed
command file and its own output namespace. The bookkeeping stops being your problem, which
means you can afford to ask bigger questions.

**What I used it for.** Running the Advanced flows; launching and re-launching individual
nodes after failures; reading per-node status; navigating the split tree to compare
outcomes across a design of experiments. The node identifiers visible in my screenshots
(`n15038`, `n15046`, `n15083`, `n3586`, `n3715`) are SWB node numbers from my own project
database.

**Key concepts I had to internalise:** `@param@` substitution, `@node@` and
`@node:index@`, `@previous@` and `@node|-1@` for reaching backwards in the flow, scoped
references like `@tdr|nmos@` into a branch of the tree, `#if`/`#noexec`/`#endif`
preprocessor conditionals that let one deck serve several purposes, and `gtree.dat` as the
file that actually encodes the split tree. Detail in
[04 · Workbench and DOE](04-workbench-and-doe.md).

---

## Sentaurus Process (`sprocess`)

**What it is.** A physical process simulator. You give it a sequence of fabrication steps
— implant, diffuse, deposit, etch, oxidise, polish, anneal — and it solves the
corresponding physics on an evolving mesh to produce the structure that recipe would
actually create.

**What "actually" buys you.** If you deposit a screening oxide you get a flat layer of
known thickness. If you *grow* it with `gas_flow` and `diffuse`, you consume silicon,
change the surface, and get a slightly different geometry — and later implants land
differently as a result. Similarly, an implant followed by a spike anneal does not stay
where you put it: dopant diffuses, and the junction depth you end up with is an *output*,
not an input. Process simulation is how you find that out before committing to a mask set.

**What I used it for.** Two flows in the Advanced level: an **N-well diode**, and a
**28 nm NMOS capacitor / MOSFET** flow. Between them these covered STI formation
(trapezoidal trench etch, nitride/oxide liner, fill, CMP planarisation), well implants,
threshold-adjust and halo implants, screening oxide, gate stack formation and poly
patterning, LDD and N+/P+ source/drain implants, and spike anneal.

**Features that mattered:**

- `AdvancedCalibration` — loads the calibrated model coefficient set rather than raw
  defaults. Turning it on is close to mandatory for anything you intend to compare against
  data.
- **Monte-Carlo implantation** (`sentaurus.mc`) — statistical ion trajectories instead of
  analytic profiles. Slower, but it captures channelling and lateral straggle, which
  matter for halo and LDD.
- **Four-rotation implants** with tilt — implanting at 0°/90°/180°/270° to get a symmetric
  profile despite a non-zero tilt angle, exactly as a real tool would.
- `refinebox` and `remesh` — declaring where the grid must be fine and forcing a remesh
  after the structure changes, because a mesh appropriate to the pre-etch structure is not
  appropriate to the post-etch one.
- `struct tdr` for saving structures, and `WritePlx`/`SetPlxList` for writing 1D profile
  data out for plotting.

Detail: [06 · Process simulation](06-process-simulation.md).

---

## Sentaurus Structure Editor (`sde`)

**What it is.** The geometry and structure tool. It builds regions, assigns materials,
places contacts, defines analytic or read-in doping profiles, and sets up mesh refinement
— either interactively or, far more usefully, from a command file.

**The language trap.** `sde` command files (`*_dvs.cmd`) are written in **Scheme**, not
TCL. This surprises people, including me, and it is worth stating flatly because
misdescribing it is an easy way to look careless. Commands look like
`(sde:build-mesh "snmesh" "-a -c conforming" "n@node@_msh")` — parenthesised prefix
notation, Scheme semantics. `sprocess` and `sdevice` decks, by contrast, are TCL. See
[05 · Scripting](05-scripting-tcl-scheme-swb.md).

**What I used it for.** Structure creation and editing for the device-level work, contact
and region definition, refinement setup, and invoking the mesher. The N-well diode and the
28 nm device work both pass through `sde`.

**Why emulation rather than full process.** For the mixed-mode inverter and the device
analysis work, what I needed was a correct, controllable structure — not a prediction of
what a fab would produce. Building it in `sde` runs in seconds instead of hours and lets
me change one doping parameter without re-simulating twenty process steps. Choosing
emulation over process simulation here is a legitimate engineering decision, not a
shortcut, and being able to say why is part of what the Advanced level was teaching.

---

## Sentaurus Mesh (`snmesh`)

**What it is.** The mesh generator. It turns a geometric structure into the finite-element
grid the solver actually works on, either as a standalone SWB tool or invoked from within
`sde`.

**Why it gets its own section.** Because in practice this is where simulations fail. The
solver discretises the semiconductor equations on this grid; if the grid is too coarse
where the fields and carrier densities vary rapidly — at junctions, at the gate oxide
interface, in the inversion layer — the answer is quantitatively wrong and can be
qualitatively wrong. If the grid is fine everywhere, the run does not finish. Meshing is
the act of spending elements where they buy accuracy.

**What I worked with:** refinement windows (`refinebox`) placed at junctions and under the
gate; `MaxLenInt` to force fine spacing across material interfaces;
`DopingConcentration` / `MaxGradient` criteria so the mesh automatically follows the doping
profile; `MaxTransDiff` to limit how fast element size may change; and remeshing after
structural modification. The practical rule I came away with: refine on *gradients*, not on
regions — the mesh should be fine where something is changing, and the doping profile
already knows where that is.

---

## Sentaurus Device (`sdevice`)

**What it is.** The electrical solver, and the centre of gravity of the whole suite. It
takes a meshed, doped structure and solves the semiconductor transport equations on it
under a bias schedule you specify.

**The structure of a deck.** Every `sdevice` command file is the same six blocks, and once
you see that, the tool becomes legible:

| Block | Answers the question |
| --- | --- |
| `Electrode` | What are the terminals, what are they biased to, what is the gate workfunction? |
| `File` | Which grid comes in, where do plots, current data and parameters go? |
| `Physics` | Which physical models apply — mobility, recombination, quantum correction, thermal? |
| `Plot` | Which internal quantities do I want saved for post-processing? |
| `Math` | How is this solved — coupling, method, damping, iteration limits, threads? |
| `Solve` | In what order, and through what bias/time schedule? |

**Analysis types I ran.**

- **DC / quasi-stationary** — `Quasistationary` with a `Goal`, ramping a terminal to a
  target voltage in controlled increments to get I<sub>d</sub>-V<sub>g</sub> and
  I<sub>d</sub>-V<sub>d</sub> characteristics.
- **Small-signal AC** — `ACCoupled` at a specified frequency (1 MHz in the C-V work) to
  extract capacitance versus bias. This is the analysis that produces the data a real
  calibration is checked against.
- **Transient** — `Transient(BE)`, backward Euler, for switching behaviour and for
  TLP/ESD-style stress.
- **Electro-thermal** — the `Thermodynamic` model with a `Thermode` boundary and
  `SurfaceResistance`, solving lattice temperature alongside carrier transport. Necessary
  the moment self-heating changes the answer, which under ESD stress it certainly does.
- **Mixed-mode** — multiple `Device` instances wired into a `System` netlist with
  lumped sources and passives, solved together with the circuit equations. Covered in
  [08 · Mixed-mode simulation](08-mixed-mode-simulation.md).

**Physics I selected and why.** Drift-diffusion as the transport model, with
`eQuantumPotential(density)` for quantum correction of carrier density in thin inversion
layers; mobility as a stack of `DopingDependence`, `HighFieldSaturation(GradQuasiFermi)`,
`Enormal(IALMob)` for transverse-field degradation at the interface, and
`CarrierCarrierScattering` where relevant; recombination as `SRH(DopingDep)`, `Auger` and
`Avalanche(UniBo2)` for impact ionisation; and `BandGapNarrowing(OldSlotboom)` /
`EffectiveIntrinsicDensity(oldSlotboom)` for heavy doping. Each of those is a claim about
the device, and [12 · Key learnings](12-key-learnings.md) explains what each one is
correcting for.

**The flag I now always use.** `-CheckUndefinedModels`. Without it, if you invoke a model
that has no parameter set for the material in question, `sdevice` quietly falls back to
silicon defaults and tells you only in the `.err` file. That is a silent-wrong-answer
failure mode, which is the worst kind. See
[11 · Debugging log](11-debugging-log.md).

---

## Sentaurus Visual (`svisual`)

**What it is.** The post-processor: 2D and 3D field visualisation, 1D curve plotting,
cutlines, and — the part that matters at Advanced level — a full **TCL** scripting
interface so that plotting and parameter extraction happen automatically as part of the
flow rather than by hand afterwards.

**What I used it for.** Everything in [`../screenshots/`](../screenshots/) is an `svisual`
session except the three editor captures. Specifically: 2D scalar field plots of doping,
electron density and current density; overlaying many SWB nodes in one plot so a sweep
reads as a family of curves; **pinning the colour range** so that panels across a bias
sweep are actually comparable rather than each auto-scaled to its own maximum; vertical
**cutlines** to turn a 2D field into a 1D profile on a log axis; and rendering current
density as a **vector field** rather than a magnitude contour when the question is where
the current flows rather than how much.

**Scripting it.** A `svisual_vis.tcl` script can create plots, load `.plt` datasets, build
curves from named variables, set axis/legend/title properties, assign colours
deterministically from the node index so a family of curves is readable, and call the
`extract` library to pull parameters out of curves. The on-resistance extraction I worked
with is in [10 · Calibration and extraction](10-calibration-and-extraction.md).

**Why automating this is the whole point.** A DOE with 120 nodes produces 120 curves. Any
plotting you do by hand, you will do 120 times and then again after you change one process
parameter. Scripted post-processing means the analysis is regenerated with the data, which
also makes it reproducible — the plot and the numbers came from a script anyone can read.

---

## Sentaurus Script Editor / jEdit

**What it is.** The editor bundled with the suite, with Sentaurus syntax awareness for
command files. Introduced formally at Level 2.

**What I used it for.** Reading and modifying the decks. It is where the three
mixed-mode screenshots in
[`../screenshots/04-mixed-mode-cmos-inverter/`](../screenshots/04-mixed-mode-cmos-inverter/)
were taken — the editor view of `sdevice_des.cmd` for the inverter project. Unglamorous,
but a syntax-aware editor is how you notice an unbalanced brace in a `System{}` block
before the solver does.

---

## Tool versions and where they ran

| Environment | Sentaurus version | Used for |
| --- | --- | --- |
| IISc remote hosts (`ancl2` / `ancl3.dese.iisc.ernet.in`, over VNC) | R-2020.09-SP1 | Levels 1 and 2 |
| Local VMware VM (RedHat AS 6.6), `/opt/STROOT/TCAD2017/` | N-2017.09 / N-2017.09-SP2 | Advanced level |

Working across two versions was incidentally instructive: syntax and model names are
stable enough that decks port, but not identical, and finding out which is which is a
useful reminder that "it worked on the other machine" is a diagnosis, not an excuse.
Setup detail in [03 · Environment setup](03-environment-setup.md).

---

**Next:** [03 · Environment setup](03-environment-setup.md) —
building the VM and getting the toolchain to launch.
