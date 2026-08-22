# 12 · Key Learnings

The consolidated version: what I actually understand now that I did not before, organised by
kind rather than by chronology. Where a claim rests on a specific piece of work, it links to
it.

## Semiconductor device physics

**A MOSFET is an interface device, and that changes everything.** Before this program I
thought of a transistor as a bulk object with terminals. The inversion layer is a sheet of
carriers a few nanometres thick pressed against the oxide, and almost every non-ideality
follows from that fact: mobility is degraded by the transverse field pressing carriers into a
rough interface (`Enormal`), the classical carrier-density peak sits at the wrong depth so a
quantum correction is needed (`eQuantumPotential`), and the gate capacitance you measure is
lower than the ideal oxide value because the charge centroid is displaced. Seeing the
inversion layer form panel by panel in a
[gate-bias sweep](../screenshots/03-device-simulation/) is what converted this from a fact I
could recite into a picture I can reason from.

**Short-channel effects are geometric, and the halo implant is the answer.** At 28 nm the
source and drain depletion regions are close enough to interact with the channel potential,
which lowers the barrier the gate is supposed to control — threshold roll-off,
drain-induced barrier lowering, punch-through. The halo implant raises doping locally, exactly
where those depletion regions would otherwise reach, so the channel edges are harder to
deplete. The reason it is *angled* is that the doping must land at the channel edges under the
gate, not in the middle. Sweeping halo depth, dose and position and watching the transfer
characteristic move is the most direct demonstration I have seen that a fabrication step and a
datasheet number are the same statement.

**Process determines device, quantitatively.** Junction depth is an *output* of an implant plus
a thermal budget, not an input. Spike anneal exists because activation and diffusion are driven
by the same temperature, so the recipe is a race between them. Growing a screening oxide moves
the silicon surface, so subsequent implant depths are referenced to somewhere new. None of
these are refinements — they change the electrical result. Details in
[06 · Process simulation](06-process-simulation.md).

**Mobility is not a number.** It is a composition of scattering mechanisms, each dominant in a
different regime: ionised impurities in heavily doped regions, surface roughness and phonons at
the interface, velocity saturation at high longitudinal field, carrier–carrier scattering at
high injection. `Mobility(DopingDep HighFieldSaturation Enormal)` is three physical claims about
where your device operates, not a preset.

**Heavy doping changes the band structure.** Bandgap narrowing at 10²⁰ cm⁻³ doping levels
raises the effective intrinsic density, which alters junction built-in potential and injection.
Leaving `BandGapNarrowing` out of a device with modern source/drain doping is a real error, not
a simplification.

**Self-heating is a feedback loop with two signs.** Temperature reduces mobility, which reduces
current — stabilising. It also raises intrinsic concentration and leakage and lowers the
impact-ionisation threshold — destabilising. Which wins depends on the operating point, and
under ESD stress the destabilising loop can win outright. This is why
[electro-thermal analysis](09-ac-transient-and-thermal.md) exists and why an isothermal
simulation cannot tell you about failure.

**C-V constrains a model in a way I-V cannot.** Drain current depends on so many parameters
that several wrong models fit one I-V curve. Gate capacitance versus bias depends much more
directly on oxide thickness and the charge distribution under the gate. Matching both is a much
stronger claim than matching either. This is the reasoning behind the three-way comparison in
[10 · Calibration](10-calibration-and-extraction.md), and it is the single most useful piece of
methodology I took from the level.

**CMOS sizing is mobility asymmetry made concrete.** Hole mobility is roughly half electron
mobility, so a symmetric inverter needs a PMOS roughly twice as wide. In the mixed-mode deck
this is literally two numbers, `AreaFactor=10` and `AreaFactor=20`, and having the
[two structures side by side](../screenshots/02-device-structures/) makes the reason visible
rather than memorised.

## Numerical methods

**Discretisation is part of the model.** The solver sees a mesh, not a structure. Anything the
mesh does not resolve, the answer does not contain. A too-coarse mesh across an inversion layer
does not give a slightly wrong drive current; it gives a device that barely turns on. Meshing
is resource allocation — spend elements where gradients are steep — and the elegant way to do
it is to refine on doping gradient and let the profile place the grid.

**Staged solving is a requirement, not a nicety.** Poisson alone first, then coupled carrier
transport, then a ramped bias sweep, then the transient. Each stage exists to give the next one
a good initial guess. Jumping to the final operating point from a cold start is the most
reliable way to fail to converge.

**Match the solver to the structure of the problem.** A two-device-plus-circuit system has a
naturally block-structured Jacobian, and `Method=Blocked` with `SubMethod=ParDiSo` exploits it.
`ILS` for large single-device problems. This is a general principle — exploit known structure
rather than treating every system as dense — and mixed-mode is the clearest instance of it I
have met.

**Put resolution where the physics is, not uniformly.** `TurningPoints` forces a fine timestep
at instants you know are interesting, because an adaptive controller reacts to change only
after detecting it and can step straight past a fast edge. Using domain knowledge to make a
numerical method affordable is a habit worth having; see
[08 · Mixed-mode](08-mixed-mode-simulation.md).

**Non-convergence is a diagnostic.** A solve that stalls at a particular bias is telling you
about your mesh in a region that has just become important, or about a step that is too large
going into a nonlinearity. Treating it as information rather than as an obstacle is what turned
convergence from a frustration into a debugging channel.

## Methodology

**Read the error file before the result file.** The single highest-value habit from the whole
program. Nearly every hour I lost was to something already written plainly in output I had not
opened.

**Warnings are more dangerous than errors.** An error stops you. A warning lets you publish a
confident wrong number. The `UNDEFINED model … Silicon default will be used` case in
[11 · Debugging log](11-debugging-log.md) is the canonical example: a Ge region silently
simulated with silicon coefficients, converging cleanly and producing a plausible plot of a
device that does not exist. `-CheckUndefinedModels` is now a default for me, not an option.

**Parameterise instead of duplicating.** A value that appears once cannot be updated
inconsistently. `define X @X@` at the top of a deck is a small thing that eliminates a whole
class of error, and it is the same reasoning as any refactor.

**Automate the analysis, not just the run.** With a hundred nodes, any plotting done by hand
will be done a hundred times and then redone. Scripted post-processing keeps figures and data in
sync and makes the analysis reproducible by anyone who can read the script.

**Make outputs self-describing.** Key filenames, dataset names and legend labels on the node
that produced them (`n@node@_sys_des.plt`, `-label "($N): Vgs=@Vgs@"`). A legend that cannot go
stale is worth more than a tidy one, and it is why the figures in this repository can be traced
to specific nodes.

**Reduce dimensionality until only the question remains.** The course does a 1D N-well profile
before the 2D structure, and that ordering is pedagogy worth stealing. If you want to know what
implant energy does to a profile, a full 2D structure is not just slower — it is worse, because
everything else in it is noise relative to your question.

**Choose your fidelity deliberately.** Process simulation when the recipe is the question;
emulation in `sde` when the electrical behaviour is. Compact models when you need a circuit
answer in milliseconds; mixed-mode when the device is operating where no compact model was
fitted. Stating which situation you are in *before* you start is most of simulation strategy.

**Fix the structure before tuning parameters.** Calibrating model coefficients to compensate
for a wrong geometry yields numbers that fit one device and predict nothing — which defeats the
only purpose calibration has.

**Validate on data you did not fit.** Fit the transfer characteristic, then check the output
characteristic. If it improves too, your parameters are physical. If it degrades, you
curve-fitted. This is the same discipline as a held-out test set, and it is why
[10 · Calibration](10-calibration-and-extraction.md) is the chapter I would defend hardest.

## What changed about how I think

Three things, and they are not TCAD-specific.

**Simulation is an argument, not an output.** A converged run with a beautiful colour map
proves nothing on its own. What makes it credible is the chain: a defensible structure, a
resolved mesh, a justified model set, a converged solution, and agreement with an independent
measurement. Any link missing, and the picture is decoration. I did not have that framing before
this program and I now apply it to everything.

**The interesting information is in the disagreement.** The most valuable figure in this
repository is the one where the simulation over-predicts current by 1.7× while matching C-V and
threshold, because that combination *localises the error* — electrostatics right, transport or
series resistance wrong. A perfect match would have taught me nothing.

**Abstraction boundaries are where the bugs live.** SWB substitution above TCL above the tool.
Region names generated upstream and referenced downstream. Model coefficients defined per
material and invoked per region. Every problem in
[11 · Debugging log](11-debugging-log.md) is a boundary where one layer assumed something about
another. That is true of software generally, and TCAD is where I finally saw it clearly.

---

**Next:** [13 · Skills and concepts](13-skills-and-concepts.md) — the same content mapped to
evidence.
