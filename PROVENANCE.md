# Provenance and Authorship

This repository is a technical record of my participation in the **India Semiconductor
Workforce Development Program (ISWDP), Cohort 6**. Because the program is delivered by
IISc with tooling and courseware from Synopsys and sponsorship from Samsung, it matters
a great deal that this repository is precise about what is mine and what is not. This
file is that statement. Everything else in the repository is written to be consistent
with it.

## What is mine

**The environment.** I installed and configured the local simulation environment
(VMware Player 17.5.2 on Windows, RedHat AS 6.6 guest, Synopsys Sentaurus TCAD
N-2017.09 inside the guest), imported the course project database into
`/home/sentaurus/STDB/projects/`, and got Sentaurus Workbench, Sentaurus Process,
Sentaurus Structure Editor, Sentaurus Device and Sentaurus Visual running end to end.
Earlier levels were run against IISc's remote hosts (`ancl2`/`ancl3.dese.iisc.ernet.in`,
Sentaurus R-2020.09-SP1) over VNC.

**The simulation runs.** I executed the process, structure, device and visualisation
flows in Sentaurus Workbench: launching nodes, watching them fail, reading the `.err`
and `.log` files, fixing what could be fixed, and re-running. The node numbers visible
in my screenshots (`n15038`, `n15046`, `n15083`, `n3586`, `n3715`) are nodes from my
own project database, captured during my own working sessions on the dates shown in the
file metadata.

**The analysis.** Every figure under [`screenshots/`](screenshots/) is a capture of my
own Sentaurus Visual or editor session. The choices in those figures are mine: which
scalar field to plot, which nodes to overlay, whether to fix the colour range so that
panels are comparable, where to take a vertical cutline, whether to render current
density as a filled contour or as a vector field. That is the part of TCAD work that is
judgement rather than clicking, and it is the part I am putting forward.

**The documentation.** Everything in [`docs/`](docs/) is written by me: the explanation
of each tool, the walk-through of each flow, the physics notes, the debugging log, and
the interview/viva preparation material. Where I quote a command file, the quote is
short, attributed, and accompanied by my own commentary on what it does and why.

## What is not mine

**The Sentaurus Workbench project bundle.** The Advanced level ships a reference project
database (`ISWDP_AdvanceLevel/`, 11 SWB projects) that participants import into their VM
and run. Those projects — the `sprocess_fps.cmd`, `sde_dvs.cmd`, `sdevice_des.cmd` and
`svisual_vis.tcl` command files, the `gtree.dat` split trees, and the pre-computed
results shipped with them — were authored by the program's instructors. Their file
timestamps run from **August 2023 to November 2024** — the most recent of them close to a
year, and the earliest more than two years, before Cohort 6 began in October 2025. I did
not write them, and this repository does not republish them as if I had.

I have therefore **not** committed the course command files. Instead,
[`docs/`](docs/) explains each flow in my own words and quotes short excerpts
(typically 5–25 lines) where an excerpt is genuinely necessary to explain a concept.
Each such excerpt is labelled as course material. If a reviewer wants the full files,
they come with the course, not from me.

**Reference figures.** The four images in [`reference/`](reference/) — the 2D NMOS
process cross-section and the three calibration comparison plots — are outputs shipped
inside that same course bundle (file dates 2023-08-14). They are included because they
are the clearest illustration of what "model calibration against reference data" means
in this course, and the documentation would be poorer without them. They are labelled
as course material everywhere they appear, and they are deliberately kept in a separate
top-level folder from `screenshots/` so the distinction cannot be missed.

**Lecture slides.** I captured roughly 40 slides from the live sessions. Most carry a
visible `© 2022 Synopsys, Inc.` footer, and the program's own orientation guidelines
prohibit redistributing session content. **None of those captures are in this
repository.** Where lecture material is relevant, I have written out the concept in my
own words instead. See [Why the lecture slides are not here](#why-the-lecture-slides-are-not-here).

**Third-party software and books.** The VMware installers, the RedHat guest image and
the textbook PDF that live in my local coursework folder are not redistributable and are
excluded by [`.gitignore`](.gitignore).

## How to read a claim in this repository

I have tried to keep three registers strictly separate, and to use consistent wording:

| Wording | Means |
| --- | --- |
| "I built / I ran / I plotted / I debugged" | My own action, evidenced by a screenshot or an artefact in this repository |
| "The course reference project does X" | A property of the instructor-supplied material |
| "The Advanced level covered X" | Curriculum scope, quoted from my certificates or the official program brochure |

Scores, percentiles, dates and level content are taken verbatim from my certificates,
which are in [`certificates/`](certificates/) so that any claim in the README can be
checked against the source document in the same repository.

## Why the lecture slides are not here

The orientation deck for Cohort 6 contains an explicit guidelines slide stating that
recording, screen-capturing or redistributing any part of a session is prohibited, and
that a violation may result in removal from the session and disqualification from the
fellowship. Separately, the decks are Synopsys copyright.

Publishing 40-odd slide captures would therefore have been both a copyright problem and
a program-compliance problem, and it would have made the repository weaker anyway — a
folder of someone else's slides says nothing about what I can do. The lecture content is
represented here as prose in [`docs/`](docs/), which is both safe and more useful.

## Known gaps, flagged rather than filled

- Three of the projects I demonstrably worked in — `Sdevice-I-II_NMOS_28nm_Extension`,
  `Sdevice-I-II_PMOS_28nm_Extension` and `Sdevice-I-II_Inverter_28nm` — appear in my
  screenshots but are **not** present in the coursework folder I still have. They lived
  in the VM's `STDB` database, which I no longer have a copy of. The screenshots are the
  only surviving artefact, so the documentation is built around them rather than around
  files I cannot show.
- The official program URL cited in the README, `https://iisc-iswdp.org`, is taken from
  the program's own brochure (`iswdp.pdf`, which also cites `iisc-iswdp.org/about.php`
  and `iisc-iswdp.org/schedule.php`) and from the registration link
  `iswdp.registeryourseat.in` in my shortlisting email. I could not re-verify it against
  the live site while assembling this repository, so treat it as document-sourced.
- Level 1 coursework files are not in my archive; Level 1 is documented from its
  certificate and the official curriculum only.
