# 15 · Viva and Interview Notes

Questions I should be able to answer about this work, with the answers I would give. Written
for two audiences: an examiner in a project viva, and an engineer interviewing me for a role
that touches device modelling.

The organising principle: for every claim in this repository there should be a question I can
answer, and for every question there should be a specific artefact I can point at.

---

## Opening question: "Tell me what you did."

*Short version.* I completed the Advanced level of ISWDP, a program run by IISc with Synopsys
and Samsung, which teaches semiconductor technology through hands-on TCAD. Over three months I
went from basic 2D device simulation to building a 28 nm CMOS device from a process flow,
simulating it electrically, co-simulating two of them as a CMOS inverter with a real circuit
netlist, and comparing the results against reference PDK data. I set up the whole toolchain
myself on a VM, and I scripted the post-processing and parameter extraction. Final assessment
was 92%, 93rd percentile.

*If asked for a specific highlight.* The mixed-mode inverter. Two physically meshed transistors
wired into a netlist with a pulse source and a 30 fF load, with the device transport equations
and the circuit equations solved in one Newton system — DC-ramped to the supply first, then run
as a transient with the timestep forced fine across the switching edges. It is the one piece of
work where device physics and circuit behaviour genuinely stop being separate subjects.

---

## On the tools

**Q. What is TCAD, and why does industry use it?**

Technology CAD is physics-based simulation of semiconductor fabrication and device operation.
The commercial argument is that a mask set and a fab run cost enormous amounts of money and
weeks of time, and TCAD lets you explore the process and device design space before committing
to silicon. It also answers questions measurement cannot: you can plot the electric field
inside a device at a specific instant during switching, which no probe can do.

**Q. Walk me through a full TCAD flow.**

Four stages. `sprocess` takes a fabrication recipe and produces a structure by simulating the
physics of each step. `sde` and `snmesh` handle geometry, doping, contacts and the mesh —
either as an alternative to process simulation or as post-processing on its output. `sdevice`
solves Poisson plus carrier continuity on that mesh under a bias schedule to give electrical
characteristics. `svisual` post-processes: field plots, curves, extracted parameters. Sentaurus
Workbench sits over all of it, expanding a parameterised flow into a tree of runs and managing
them.

**Q. When would you use process simulation instead of just building the structure directly?**

When the process itself is the question, or when you need a structure whose doping profile is
*credible* rather than merely specified — for instance as the starting point for a calibration.
Process simulation tells you things you did not put in: where a junction actually ends up after
a thermal budget, how a tilted implant shadows off a resist edge, how growing an oxide moves
the silicon surface.

When the question is electrical, emulation in `sde` is the right choice — seconds instead of
hours, and one number to change instead of re-running thirty process steps. For my mixed-mode
work I wanted to vary bias and circuit loading, so re-deriving the structure each time would
have bought nothing. Knowing which situation you are in before you start is most of what the
curriculum calls simulation strategy.

**Q. What language are Sentaurus command files written in?**

It depends on the tool, and this is worth being precise about. `sprocess` and `sdevice` decks
are interpreted by an embedded **TCL** interpreter. `svisual` scripts are TCL. But `sde`
structure files are **Scheme** — parenthesised prefix notation, Scheme semantics. On top of all
of them, Sentaurus Workbench runs its own preprocessing pass first, substituting `@param@`
tokens and resolving `#if`/`#noexec` conditionals. So there are three layers, in that order,
and most confusing deck errors come from expecting one layer to do another's job — a `#if`
cannot depend on a TCL variable, and a TCL `if` cannot skip a tool invocation.

---

## On device physics

**Q. Why does a MOSFET need a halo implant at 28 nm?**

Because at that gate length the source and drain depletion regions are close enough to
influence the channel potential, which lowers the barrier the gate is meant to control. That
shows up as threshold roll-off with gate length, drain-induced barrier lowering, and eventually
punch-through. The halo is a locally higher doping at the channel edges, precisely where those
depletion regions would otherwise reach, so the channel edges are harder to deplete. It is
implanted at an angle because the doping has to land at the channel edges *under* the gate, not
in the middle.

**Q. Why does your inverter's PMOS have twice the AreaFactor of the NMOS?**

Hole mobility in silicon is roughly half electron mobility, so a PMOS of the same width drives
roughly half the current. For a symmetric inverter — equal rise and fall times, switching
threshold at mid-rail — you need the pull-up and pull-down strengths matched, so the PMOS has to
be about twice as wide. In a 2D simulation there is no width, so `AreaFactor` supplies an
effective one: 10 for the NMOS, 20 for the PMOS. It is the standard CMOS sizing ratio expressed
as a simulation parameter.

**Q. Why is a quantum correction needed in a 28 nm device?**

The inversion layer is a few nanometres thick, which is thin enough that carriers are quantum
confined. Classically the carrier density peaks right at the oxide interface; in reality
confinement pushes the centroid a couple of nanometres into the silicon. That displacement acts
like extra oxide thickness, so it lowers the gate capacitance in inversion — which means it is
directly visible in a C-V measurement, not a cosmetic correction. `eQuantumPotential(density)`
applies a density-gradient correction to capture it.

**Q. Explain the mobility models in your deck.**

Each term is a different scattering mechanism. `DopingDependence` is ionised impurity
scattering — heavier doping, lower mobility. `HighFieldSaturation` is velocity saturation: at
high longitudinal field carriers stop accelerating, which is why drain current saturates rather
than growing without bound. `Enormal` handles degradation from the transverse field pressing
carriers against the oxide interface, where surface roughness and phonon scattering dominate —
in a MOSFET that is a first-order effect, because the channel *is* an interface. Together they
are three physical claims about where the device operates.

**Q. Why does an LDD exist if it adds series resistance?**

Reliability. Without it, the field peaks sharply at the drain edge, which drives hot-carrier
generation, oxide damage and eventually breakdown. A lightly doped extension spreads that field
peak over a longer distance. You pay for it in series resistance and therefore drive current.
It is a deliberate trade of performance for lifetime.

**Q. What is a spike anneal for?**

Activating implanted dopant with as little diffusion as possible. Activation and diffusion are
driven by the same temperature, so the design of the anneal is a race between them — very hot,
very short. It is the clearest example in the flow of a trade-off with no free lunch.

**Q. Why does self-heating matter, and how did you simulate it?**

Because the coupling runs both ways. Temperature reduces mobility, which reduces current — a
stabilising loop. It also raises intrinsic carrier concentration and leakage and lowers the
impact-ionisation threshold — a destabilising loop that under high stress produces thermal
runaway. Which one wins depends on the operating point, and an isothermal simulation cannot
tell you, because there temperature is an input. You solve it with the `Thermodynamic` model,
which adds the lattice heat equation to the coupled system, plus a `Thermode` boundary for
where the heat leaves and a `SurfaceResistance` on it — because an ideal thermode is an
infinite heat sink and will under-predict the temperature rise.

---

## On numerical method

**Q. Why does mesh quality matter so much?**

Because the solver does not see your structure, it sees the mesh, and anything the mesh does
not resolve is not in the answer. The quantities that matter vary over wildly different length
scales: microns in the bulk, nanometres across the inversion layer, tens of nanometres across a
depletion region. A uniform mesh fine enough for the inversion layer would never finish; one
coarse enough to finish would smear the inversion layer away and report the wrong drive
current. So meshing is resource allocation — spend elements where a gradient is steep. The
elegant version is to refine on doping gradient and let the profile place the grid.

**Q. Your simulation will not converge. What do you check?**

In order: is the bias step too large going into a strongly nonlinear region — reduce
`Increment`, cap `MaxStep`. Is the mesh too coarse in a region that has just become
electrically important, such as the inversion layer as it forms. Is the solve staged — Poisson
alone first, then coupled transport, so each step has a good initial guess. Does the linear
solver suit the problem — `ILS` for large systems, `Method=Blocked` with `SubMethod=ParDiSo`
for multi-device. The general point is that non-convergence is a diagnostic: it usually tells
you something about the mesh or the bias schedule, and it is rarely random.

**Q. What is `TurningPoints` and why did you need it?**

An adaptive timestep controller reacts to change after detecting it, which means it can step
straight over a fast event using a step size that was appropriate a moment earlier.
`TurningPoints` lets you specify instants and ranges where the step must be fine regardless.
In the inverter transient it forces sub-picosecond steps across the input's rising edge — where
the output slews, both devices conduct simultaneously, and the solution moves fastest. The
alternative is to reduce the step globally and waste effort across the 20 ns where nothing is
happening. It is a good example of using domain knowledge to make a numerical method
affordable.

**Q. Why `Method=Blocked` with `SubMethod=ParDiSo`?**

Because the Jacobian of a two-device-plus-circuit system is naturally block structured — a
block per device, plus circuit coupling. A blocked method exploits that instead of treating the
system as dense, and ParDiSo is the parallel sparse direct solver used within a block. Matching
the solver to the known structure of the problem is a general principle; this is the clearest
instance of it I met.

---

## On calibration — expect the hardest questions here

**Q. What is calibration and why does it matter?**

Adjusting model parameters until simulated characteristics match measured data from real
fabricated devices. It matters because an uncalibrated simulation is a hypothesis. Once
calibrated against silicon, the model can be trusted to *predict* — to explore process
variations that have not been fabricated — and that predictive use is the entire economic
argument for TCAD.

**Q. Your simulated drain current was about 1.7× the reference. What would you do?**

First, note *what else* was true, because that is the diagnosis. The C-V matched well and the
threshold aligned — turn-on happened at essentially the same gate voltage. So the electrostatics
are approximately right: oxide thickness and channel doping cannot be far off, or the threshold
would be displaced. That points away from geometry and doping and toward transport and
resistance.

The candidates are then mobility set too high, velocity saturation under-weighted, effective
channel length too long, or — usually the first suspect — series resistance not adequately
represented. Source/drain and contact resistance drop voltage that never reaches the channel; a
simulation omitting them delivers full bias to the channel and over-predicts current.

To separate them: series resistance costs proportionally more at high current, so if resistance
is the cause the error should *grow* with drive level, whereas a mobility error stays roughly
proportional. Both I-V curves being high by a similar factor also argues for one systematic
cause rather than several independent ones. And I would fix the structure and electrostatics
before touching any transport parameter, because tuning coefficients to compensate for wrong
geometry produces numbers that fit one device and predict nothing.

**Q. Why compare C-V as well as I-V?**

Because drain current depends on mobility, threshold, series resistance, velocity saturation
and effective channel length all at once, so several different wrong models can fit one
I<sub>d</sub>-V<sub>g</sub> curve. Capacitance versus bias depends much more directly on oxide
thickness and how charge distributes under the gate. Matching both with one parameter set is a
far stronger claim than matching either, and — as in the previous answer — having independent
measurements is what lets you *localise* an error rather than merely observe it.

**Q. How do you know you have calibrated rather than curve-fitted?**

Two tests. Validate on data you did not fit: tune against the transfer characteristic, then
check the output characteristic — if it also improves, the parameters are physical; if it
degrades, you have curve-fitted. And keep every parameter inside physically defensible bounds.
A mobility coefficient pushed outside its physical range will produce a good-looking plot and a
model that fails the moment you extrapolate, which is the only thing you wanted it for.

---

## On debugging

**Q. Tell me about a bug you found and how you found it.**

The one I would pick is a warning, not an error, which is the point of the story. A device
simulation was running a region whose material was SiGe grading to germanium, and the deck
invoked SRH, Auger and doping-dependent mobility there. The parameter file has coefficients for
those models in silicon and not for that material, so `sdevice` silently substituted the
**silicon** values and carried on — noted only in the `.err` file.

It converged. It produced a plot. The plot looked entirely plausible. And it was wrong, because
germanium's bandgap is about 0.66 eV against silicon's 1.12 eV, its mobilities are much higher,
and its intrinsic carrier concentration is orders of magnitude larger. Silicon lifetimes and
silicon mobility coefficients in a Ge region do not give a slightly-off answer, they give a
different device.

The fix is `-CheckUndefinedModels`, which makes that class of silent substitution impossible to
miss, plus either supplying the material parameters or not invoking those models in that
region. The habit it left me with is that I now open the `.err` file before the results file,
because the most dangerous defect is not the one that crashes — it is the one that returns a
confident wrong answer.

**Q. How do you approach a failed run generally?**

Classify first. Check node status in Workbench to find which node failed and at which tool.
Open that node's `.err` and then its `.log` — the tool has usually already said what is wrong
in plain language. If the source deck looks correct, open the *generated* per-node command file,
because with a preprocessing layer in between, the source is your intent and the generated file
is reality. Then decide whether the message is load-bearing: some are cosmetic, like a cleanup
step failing to delete a file that was never created, and time spent on those is time not spent
on the ones that invalidate results. Then change one thing and re-run one node.

---

## On the honest limits of my work

I would rather raise these than be caught by them.

**Q. Did you write these simulation decks?**

No, and I would not claim so. The Advanced level ships a reference project database — eleven
Workbench projects with process, structure, device and visualisation command files, authored by
the instructors; their file dates run from 2023 to 2024, well before my cohort. What I did was
set up the environment, run the flows, modify decks and parameters, write and adapt
post-processing scripts, debug failures, and interpret the results. That is stated explicitly in
[`../PROVENANCE.md`](../PROVENANCE.md), which is in the repository for exactly this reason. For
anyone who knows these tools, "ran, modified, analysed and debugged" is not a weaker claim — it
is what the job consists of.

**Q. What did you not get hands-on with?**

Full RF extraction — f<sub>T</sub>, f<sub>max</sub>, S-parameters — is curriculum I was taught
and assessed on, but I cannot show my own figure for it. Same for 3D structure work: my own
captures are 2D. Both are marked **Exposed** rather than **Working** in
[13 · Skills and concepts](13-skills-and-concepts.md), which uses an explicit three-level scale
so the distinction is visible rather than glossed.

**Q. What would you do next?**

Three things, in order of what I would learn most from. Build a process flow from scratch rather
than modifying one, because authoring exposes gaps that reading does not. Complete a calibration
end to end — take the 1.7× current discrepancy and actually close it, documenting which
parameter moved what, since the reasoning in
[10 · Calibration](10-calibration-and-extraction.md) is currently a diagnosis rather than a
fix. And run a full RF extraction, because that is the honest gap above.

---

## Three answers I would rehearse

**"What is the most interesting thing you learned?"** That the most dangerous simulation is the
one that converges cleanly and returns a wrong answer. The undefined-model substitution is my
example, and it changed my working habits permanently: read the diagnostics before the results.

**"What was hardest?"** Not the physics — the numerics. Getting solves to converge, and learning
to read non-convergence as information about the mesh or the bias schedule rather than as bad
luck. Second hardest was accepting how much of TCAD is meshing.

**"Why should I care that you did a training program?"** Because TCAD is a gated skill — the
software is institutionally licensed and the domain knowledge to get a meaningful answer out of
it is not something you pick up from documentation. And because the method transfers: define the
problem, choose and justify a model, control the discretisation, solve in a sensible order,
compare against measurement, iterate on the discrepancy. That loop is the whole of computational
engineering. TCAD is just where I learned it.

---

**Back to:** [README](../README.md) · [Provenance](../PROVENANCE.md)
