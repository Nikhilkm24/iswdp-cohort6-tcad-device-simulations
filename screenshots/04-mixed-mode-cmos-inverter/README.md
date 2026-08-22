# 04 · Mixed-mode — CMOS inverter command file

Three captures of my editor session in the `Sdevice-I-II_Inverter_28nm` project on
2 December 2025, showing the `sdevice_des.cmd` deck for the mixed-mode CMOS inverter.

These are the only captures in this repository that show source rather than results, and they are
here because the deck *is* the interesting object. It is where two physically meshed 28 nm
transistors get wired into a circuit netlist and solved together with the circuit equations in a
single Newton system — which is the most substantial concept in the Advanced level.

Full line-by-line walkthrough:
[`../../docs/08-mixed-mode-simulation.md`](../../docs/08-mixed-mode-simulation.md)

> **Provenance.** The command file shown is course-supplied material; the capture, the annotation
> and the analysis are mine. See [`../../PROVENANCE.md`](../../PROVENANCE.md).

---

## 1 · The two `Device` blocks

![NMOS and PMOS device blocks](sdevice-inverter-nmos-pmos-device-blocks.png)

`sdevice-inverter-nmos-pmos-device-blocks.png` · 20:01

`Device NMOS { … }` and `Device PMOS { … }` — each declaring its own electrodes, its own imported
grid, its own output files and its own `Physics` block.

Three things in this view are the substance of mixed-mode. The grids are pulled from separate
branches of the Workbench split tree (`@tdr|nmos@`, `@tdr|pmos@`), so the structures are imported
rather than defined here. The gate workfunctions are parameterised (`@wfn@`, `@wfp@`), making gate
material a variable of the experiment and therefore threshold voltage a knob. And each device
carries `AreaFactor` — 10 for the NMOS, 20 for the PMOS — which is how a 2D simulation acquires an
effective width, and where the 2:1 CMOS sizing ratio lives.

Note also that `Physics` is declared *per device*. They happen to carry the same model set here —
`Mobility(DopingDep HighFieldSaturation Enormal)` and `EffectiveIntrinsicDensity(oldSlotboom)` —
but they need not, which matters if a question requires asymmetric physics.

---

## 2 · `Math` and the `System` netlist

![Math block and System netlist](sdevice-inverter-math-system-netlist.png)

`sdevice-inverter-math-system-netlist.png` · 20:01

The numerics block and the circuit.

`Math` carries the settings that make a two-device system tractable: `Method=Blocked` with
`SubMethod=ParDiSo`, which exploits the naturally block-structured Jacobian instead of treating the
system as dense; `Transient=BE` for stable backward-Euler integration; `Extrapolate` to seed each
step from the previous solutions; and `Number_of_Threads = 4`.

`System` is a netlist in the SPICE sense. A supply source on node `dd`, a pulse source on `in`, the
two device *instances* with their electrode names mapped to circuit nodes — both gates to `in`,
both drains to `out` — and a 30 fF load capacitor from `out` to ground. The load matters: without
it the output node has only the devices' own parasitics and the transient is governed by numerical
rather than physical timescales.

The `Plot` line at the bottom saves `v(in)`, `v(out)` and the three currents *separately*
(`i(nmos1,out)`, `i(pmos1,out)`, `i(cout,out)`). That decomposition is what lets you see the
short-circuit current during a transition as distinct from the current charging the load, rather
than inferring it.

---

## 3 · The `Solve` schedule with `TurningPoints`

![Solve block with transient and TurningPoints](sdevice-inverter-solve-transient-turningpoints.png)

`sdevice-inverter-solve-transient-turningpoints.png` · 20:02

The four-stage solve schedule, and the staging is the engineering.

Poisson alone first, for a cheap self-consistent electrostatic starting point. Then a `Coupled`
block adding carrier transport, contacts and — critically — `Circuit`, because the netlist is part
of the same Newton system rather than something solved separately and applied. Then a
`Quasistationary` ramp of the supply to 1.2 V in adaptive steps, establishing a valid DC operating
point before anything time-dependent is asked for. Then the transient, 0 to 20 ns.

`TurningPoints` is the part worth studying. It forces the timestep down to 0.3 ps at specified
instants and 1 ps across specified ranges, all falling within the input's rising edge — precisely
where the output slews, both devices conduct simultaneously, and the solution moves fastest. An
adaptive controller only reacts to change *after* detecting it, so it can step straight past a fast
edge. This is domain knowledge being used to make a numerical method affordable, and it is the
single most transferable idea in the deck.
