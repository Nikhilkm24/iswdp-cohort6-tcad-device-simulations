# Screenshots — my own tool sessions

Every image in this folder and its subfolders is a capture of a Sentaurus session of mine,
taken while working through the ISWDP Advanced level. Filenames are descriptive, and each
subfolder has a README explaining what the figures show and — more usefully — why the
particular view was chosen.

Full-screen captures have been cropped only to remove the host operating system's taskbar. No
other editing has been done.

| Folder | Contents |
| --- | --- |
| [`01-process-simulation/`](01-process-simulation/) | N-well diode process-simulation output: current density across a node array, and as a vector field |
| [`02-device-structures/`](02-device-structures/) | The 28 nm NMOS and PMOS structures on doping concentration |
| [`03-device-simulation/`](03-device-simulation/) | Carrier and current density under gate bias; fixed colour range; vertical cutline |
| [`04-mixed-mode-cmos-inverter/`](04-mixed-mode-cmos-inverter/) | The mixed-mode CMOS inverter command file: device blocks, netlist, solve schedule |

## What is deliberately not here

**Lecture slides.** I captured roughly forty slides from the live sessions. Most carry a
`© 2022 Synopsys, Inc.` footer, and the program's own participation guidelines prohibit
recording, screen-capturing or redistributing session content. None of them are published here.
Where lecture material is relevant it is written out as prose in [`../docs/`](../docs/).

**Course-supplied output.** Figures shipped inside the reference project bundle are kept
separately in [`../reference/`](../reference/) so that the distinction between my captures and
course material cannot be missed.

See [`../PROVENANCE.md`](../PROVENANCE.md) for the full authorship statement.

## Reading the node numbers

Sentaurus Workbench identifies every run with a node number, and those numbers are visible in
the plot titles and legends — `n15038`, `n15046`, `n15083`, `n3586`, `n3715` and others. They
are how a figure traces back to a specific point in a parameter sweep. Two figures showing
consecutive node numbers are two points in the same sweep, which is what makes a side-by-side
comparison meaningful rather than incidental.
