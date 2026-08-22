# Reference figures — course-supplied material

**These four images are not my captures.** They are outputs shipped inside the Sentaurus
Workbench reference project bundle distributed with the ISWDP Advanced level, with file dates of
14 August 2023 — more than two years before my cohort ran.

They are kept in this separate top-level folder, rather than mixed into
[`../screenshots/`](../screenshots/), precisely so the distinction cannot be missed. My own
captures are all under `screenshots/`. See [`../PROVENANCE.md`](../PROVENANCE.md).

**Why include them at all.** Because they are the clearest available illustration of the single
most important idea in the level — comparing a simulation against real measured data — and the
documentation would be materially worse without them. My contribution here is the reading of them:
what the discrepancy is, what it points at, and how you would go about closing it. That analysis
is in [`../docs/10-calibration-and-extraction.md`](../docs/10-calibration-and-extraction.md).

---

## `nmos-28nm-process-structure-doping.png`

The complete 2D NMOS structure produced by the `sprocess` flow, plotted on signed doping
concentration (±6 × 10²¹ cm⁻³) across roughly 4.7 µm × 2 µm. Node `n12560`.

Everything the process flow builds is visible: the two STI trenches isolating the active area, the
P-well beneath it, the poly gate on its dielectric, source and drain either side, and the P-tap and
N-tap contact regions at the edges that tie well and substrate to defined potentials. Referenced
from [`../docs/06-process-simulation.md`](../docs/06-process-simulation.md).

## `nmos-28nm-transfer-characteristic-vs-pdk.png`

Simulated I<sub>d</sub>-V<sub>g</sub> at V<sub>DS</sub> = 0.5 V overlaid on the PDK reference, over
V<sub>g</sub> = 0 to 2 V. Turn-on aligns well — the threshold is close — but the simulated current
runs above the reference throughout the above-threshold range.

## `nmos-28nm-output-characteristic-vs-pdk.png`

Simulated I<sub>d</sub>-V<sub>d</sub> at V<sub>GS</sub> = 1 V against the PDK reference. The
simulation saturates near 1.25 × 10⁻⁵ A where the reference saturates near 7.3 × 10⁻⁶ A — an
over-prediction of roughly 1.7×.

## `nmos-28nm-cv-simulated-vs-reference.png`

Simulated small-signal capacitance from the AC node (`c(a,a)`, node `n12547_ac_des`) against
reference capacitance data, from −1 V to +1 V, spanning roughly 3 × 10⁻¹⁵ F to 2.1 × 10⁻¹⁴ F. The
agreement here is close across the full bias range.

---

## Why these three together are more informative than any one of them

C-V matches, threshold aligns, and both I-V curves over-predict by a similar factor. That
combination is a *diagnosis*, not just a set of results: capacitance is set primarily by oxide
thickness and by how charge distributes under the gate, so a good C-V match says the structure and
electrostatics are approximately right. Aligned turn-on says the same. Which leaves transport and
resistance — mobility set too high, velocity saturation under-weighted, or series resistance not
adequately represented — as where the error must be.

Having three independent measurements does not just give a better fit. It lets you localise the
error, which is the difference between knowing something is wrong and knowing what to change.
