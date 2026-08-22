# 02 · Device structures — 28 nm NMOS and PMOS

The two structures that the device-level and mixed-mode work in this repository is built on,
plotted on doping concentration in Sentaurus Visual.

Both were captured on the evening of 23 November 2025, minutes apart — the first Advanced-level
work session. Bringing the structures up and confirming they look physically right *before*
running any electrical analysis is the correct order of operations, and it is the habit that
catches region-naming and doping-placement problems early rather than after a day of
simulations. See [`../../docs/11-debugging-log.md`](../../docs/11-debugging-log.md).

Background: [`../../docs/07-structure-device-and-meshing.md`](../../docs/07-structure-device-and-meshing.md)

---

## 28 nm NMOS

![28 nm NMOS doping concentration](nmos-28nm-doping-concentration-structure.png)

`nmos-28nm-doping-concentration-structure.png` · captured 23 November 2025, 23:32

Doping concentration across the full 28 nm NMOS cross-section, on the signed logarithmic scale
that Sentaurus uses for doping — so donor and acceptor regions are distinguishable by colour and
each spans several orders of magnitude of concentration.

What to look for: the isolation at either side of the active area, the well beneath the channel,
the gate stack, and the source and drain regions with their heavily doped contact areas. On this
scale the halo and extension implants are visible as gradations near the channel edges rather
than as sharp features, which is itself accurate — they are graded profiles, not boxes.

---

## 28 nm PMOS

![28 nm PMOS doping concentration](pmos-28nm-doping-concentration-structure.png)

`pmos-28nm-doping-concentration-structure.png` · captured 23 November 2025, 23:32

The complementary device, plotted on the same scale.

Plotting both on identical scales is deliberate. The visible difference between the two is not
cosmetic — it is the physical reason a CMOS inverter cannot use identical devices. Hole mobility
in silicon is roughly half electron mobility, so a PMOS of the same width drives roughly half the
current, and a symmetric inverter therefore needs a wider PMOS. In the mixed-mode deck this
appears as `AreaFactor=10` on the NMOS against `AreaFactor=20` on the PMOS.

That 2:1 sizing ratio is something everyone learns as a rule. Having the two structures side by
side on the same colour scale is what turned it from a rule into a reason, for me. See
[`../../docs/08-mixed-mode-simulation.md`](../../docs/08-mixed-mode-simulation.md).
