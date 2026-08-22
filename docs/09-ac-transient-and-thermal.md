# 09 · AC, Transient and Thermal Analysis

DC characteristics tell you what a device does in steady state. Almost everything that
matters commercially — speed, power, robustness, whether it survives an ESD strike — lives
outside steady state. This chapter covers the three analyses the Advanced level uses to get
there.

## Small-signal AC and C-V

**What it is.** `ACCoupled` linearises the device about a DC operating point and solves for
its response to a small sinusoidal perturbation at a specified frequency. Sweep the DC bias,
repeat the AC solve at each point, and you get admittance versus bias — from which
capacitance follows.

**Why C-V is the measurement that matters.** It is easy to underrate C-V next to I-V, and
that is a mistake, for two reasons.

The first is that **capacitance sets speed**. A digital gate's delay is the time to move
charge onto the next stage's input capacitance. Drive current is half the story; the other
half is C. The 30 fF load in the
[inverter simulation](08-mixed-mode-simulation.md) is exactly this, and a device's own
C<sub>gg</sub>, C<sub>gd</sub> and C<sub>gs</sub> are what it presents to whatever drives it.

The second is that **C-V constrains a calibration in a way I-V does not**. Drain current
depends on mobility, threshold voltage, series resistance, velocity saturation and effective
channel length all at once — several different wrong models can produce a right-looking
I<sub>d</sub>-V<sub>g</sub> curve. Gate capacitance versus bias depends much more directly on
oxide thickness, the doping profile under the gate, and how the inversion and depletion
charge actually distribute. If your C-V matches and your I-V matches, you have probably got
the structure right. If only the I-V matches, you may have compensating errors. Fitting two
independent measurements is much harder to fake than fitting one.

**The frequency choice.** The C-V work in the course runs at **1 MHz**. That is not
arbitrary: it is the standard measurement frequency for MOS capacitance, chosen to be high
enough that interface traps and minority-carrier generation cannot follow the signal (so you
measure high-frequency capacitance in inversion rather than the quasi-static value), and low
enough that series resistance and distributed effects do not distort it. Matching the
simulation frequency to the measurement frequency is a precondition for comparing them at
all — a point that sounds obvious and is the sort of thing that quietly invalidates a
comparison.

**What a MOS C-V curve tells you, region by region.** In accumulation the capacitance is
essentially the oxide capacitance, so the high-bias plateau reads out effective oxide
thickness. As bias moves into depletion, a depletion capacitance appears in series with the
oxide and the total falls — and *how fast* it falls is set by the substrate doping under the
gate. The minimum sits near threshold. Beyond it, in inversion at high frequency, the
capacitance rises back toward the oxide value. So a single curve contains oxide thickness,
channel doping, and threshold — which is why it is the first thing to compare against
reference data.

**Where quantum correction shows up.** The `eQuantumPotential` correction discussed in
[07](07-structure-device-and-meshing.md) displaces the inversion charge centroid a couple of
nanometres away from the interface. That adds an effective series capacitance and lowers the
measured inversion capacitance below the ideal oxide value. In a 28 nm device the effect is
not subtle, and it is directly visible in C-V. This is the cleanest example I met of a
quantum-mechanical correction with an immediately measurable classical consequence.

The C-V calibration result is discussed in
[10 · Calibration and parameter extraction](10-calibration-and-extraction.md).

**One practical note on deck structure.** A project that does both DC and AC work typically
carries both in one command file, with the AC portion switched by an SWB parameter and a
`#if @CV@ == 0 / #noexec / #endif` guard — so a node either runs the DC characterisation or
the C-V analysis, from a single maintained source. See
[04 · Workbench and DOE](04-workbench-and-doe.md).

## Transient analysis

**What it is.** `Transient` integrates the device equations forward in time under a
time-varying stimulus. `Transient=BE` selects backward Euler: implicit, first-order,
unconditionally stable, with some numerical damping. For stiff problems and for stress events
with fast edges, stability is worth more than formal accuracy order.

**Timestep control is the whole game.** The controls are `InitialStep`, `MaxStep`, `MinStep`
and `Increment` (the growth factor between accepted steps), plus `TurningPoints` for
forcing fine resolution at known-interesting moments. The reasoning behind `TurningPoints` is
covered in detail in [08 · Mixed-mode simulation](08-mixed-mode-simulation.md), and it
generalises: an adaptive controller reacts to change after the fact, so anywhere you *know*
in advance that something fast happens, you should say so.

**Two quite different uses.** In the inverter work, the transient measures switching:
propagation delay, rise and fall times, short-circuit current during the transition. In the
ESD work below, the transient is a survival test: what happens inside the device when far more
current passes through it than it was designed for.

## Electro-thermal analysis

**Why temperature has to be solved, not assumed.** Every device simulation up to this point
assumes the lattice sits at a fixed temperature. That is fine when dissipation is small. It
stops being fine the moment power density is high enough to heat the silicon locally, because
the coupling runs both ways:

```
   current ──▶ power dissipation ──▶ local temperature rise
       ▲                                      │
       │                                      ▼
       └──── mobility ↓ , n_i ↑ , leakage ↑ ──┘
```

Higher temperature reduces mobility (phonon scattering), which reduces current — a negative
feedback that produces current de-biasing. But it also raises the intrinsic carrier
concentration and leakage, and it lowers the impact-ionisation threshold — positive feedback
that, if it wins, produces **thermal runaway** and destroys the device. Which loop dominates
depends on the operating point. You cannot get either from an isothermal simulation, because
in an isothermal simulation temperature is an input.

**How it is set up.** The `Thermodynamic` model adds the lattice heat equation to the coupled
system, so temperature is solved alongside potential and carrier densities. Two boundary
elements make it physical:

- **`Thermode`** — a thermal contact, the boundary at which heat leaves the simulated domain.
  Physically it is the package, the heatsink, the substrate — wherever the heat actually goes.
- **`SurfaceResistance`** — a finite thermal resistance at that boundary. This is the
  important refinement: an ideal thermode at fixed temperature is an infinite heat sink,
  which is optimistic and will under-predict heating. A real thermal path has resistance, and
  putting a finite value on it is what makes the predicted temperature rise credible.

**Where it is needed.** ESD and TLP analysis, power devices, high-current stress, and any
reliability question involving self-heating. The course's TLP work exercises exactly this
combination — a `Transient(BE)` solve with the `Thermodynamic` model, a `Thermode` with
`SurfaceResistance`, and `Avalanche(UniBo2)` switched on so impact ionisation is captured.

## TLP and ESD stress

**What TLP is.** Transmission Line Pulse testing characterises a device's response to a
short, high-current pulse — the laboratory stand-in for an electrostatic discharge event. A
transmission line is charged and discharged into the device, delivering a rectangular current
pulse of roughly 100 ns, and the resulting voltage is measured. Sweeping the pulse amplitude
traces out the device's high-current I-V behaviour, including **snapback** — the region where
a parasitic bipolar turns on and the voltage across the device *drops* as current rises — and
ultimately the failure current.

**Why it needs everything at once.** A TLP simulation is the analysis that requires the whole
toolkit simultaneously: transient integration for the pulse shape, avalanche generation for
the parasitic bipolar turn-on, electro-thermal coupling for the self-heating that determines
failure, and careful convergence handling because snapback is a genuine negative-resistance
region where the solution is multi-valued in voltage. It is the hardest thing in the course
and a good demonstration of why the earlier chapters exist.

**What ESD protection design is actually about.** An ESD clamp must do nothing at all during
normal operation — no leakage, no capacitance penalty — and then conduct amps within
nanoseconds when a discharge arrives, clamping the voltage below whatever would rupture the
gate oxide of the circuit it protects, and survive the resulting heating. That specification
is why TCAD is used here rather than compact models: the device is deliberately operated far
outside the regime any compact model was fitted for.

> **Provenance.** The TLP/ESD project, its command files, and the post-processing script
> shipped with it are course-supplied material; the Perl helper distributed with the project
> is Synopsys-shipped and is not in this repository. What is documented here is the analysis
> I ran and the physics I learned from it. See [`../PROVENANCE.md`](../PROVENANCE.md).

## Frequency dependence and RF

My Advanced certificate lists **frequency dependence** and **RF device simulations** as part
of the level's coverage, and both build directly on the small-signal machinery above. The
progression is: an AC solve at one frequency gives capacitance; sweeping frequency gives the
full small-signal admittance, from which the Y-parameters and hence S-parameters follow, and
from those the figures of merit that RF work is judged on — cut-off frequency f<sub>T</sub>,
maximum oscillation frequency f<sub>max</sub>, and gain. The physical point that makes this
more than bookkeeping is that at RF, *parasitics stop being parasitic*: gate resistance,
overlap capacitance and substrate coupling are first-order terms in f<sub>T</sub> and
f<sub>max</sub>, so a structure that is perfectly adequate for DC characterisation may be
inadequate for RF because it does not resolve them.

I am flagging deliberately that my hands-on work concentrated on the DC, C-V, mixed-mode
transient and calibration material rather than on a full RF extraction; the RF content is
curriculum coverage I was assessed on, not a simulation I can show a figure for. That
distinction is the kind [`../PROVENANCE.md`](../PROVENANCE.md) exists to keep clear.

## Analysis types, side by side

| Analysis | Sentaurus construct | Answers |
| --- | --- | --- |
| DC / quasi-stationary | `Quasistationary` + `Goal` | I-V characteristics, threshold, drive current, R<sub>on</sub> |
| Small-signal AC | `ACCoupled` at frequency | C-V, admittance, RF figures of merit |
| Transient | `Transient(BE)` + `TurningPoints` | Switching delay, short-circuit current, pulse response |
| Electro-thermal | `Thermodynamic` + `Thermode` + `SurfaceResistance` | Self-heating, thermal runaway, failure current |
| Mixed-mode | `System{}` + `Circuit` in `Coupled` | Real device behaviour inside a circuit |

---

**Next:** [10 · Calibration and parameter extraction](10-calibration-and-extraction.md) —
the part that makes a simulation trustworthy.
