# 11 · Debugging Log

Most of what I learned at Advanced level, I learned from things not working. This chapter is
the log: real messages, what each one actually meant, and what I changed. It is deliberately
the least polished-looking chapter in the repository, because a debugging log that contains
only successes is not a debugging log.

> **Provenance note.** The messages quoted here come from node error and log output in the
> Advanced project database — a mix of output from my own runs and from results shipped with
> the reference bundle. I have not tried to attribute each individual message, because these
> are properties of the decks and they reproduce whenever the flow is re-run. What is mine is
> the diagnosis and the reasoning. See [`../PROVENANCE.md`](../PROVENANCE.md).

## The method, before the messages

The workflow I ended up with, in this order, because arriving at it took a while:

1. **Check node status in Workbench.** Which node failed, and at which tool? A failure in
   `svisual` and a failure in `sprocess` are unrelated problems.
2. **Open that node's `.err` file, then its `.log`.** Not the source deck. The tool has
   usually already told you what is wrong in plain language.
3. **Open the *generated* `n<NNNN>_*.cmd`.** This is what the tool actually received after
   SWB substitution. If the source looks right and the run is wrong, the substitution is the
   suspect.
4. **Distinguish warning from error.** Warnings are the dangerous ones: the run completes,
   produces a plot, and the plot is wrong.
5. **Change one thing.** Then re-run one node, not the tree.

Point 2 is the one I would emphasise to anyone starting. Almost every hour I lost early on, I
lost to information that was sitting in an `.err` file I had not opened.

---

## Problem 1 — Layout mask used for an implant

**Message** (`sprocess`, NMOS capacitor flow, node `n6586`):

```
** Warning ** Layout mask is not suitable for ion implantation.
Please use a physical mask (such as Photoresist)
```

**What it means.** A *layout* mask is a geometric abstraction — a 2D region telling the tool
"pattern here, not there." An implant is a physical process: ions arrive with energy and
momentum, and whether they are blocked depends on a real layer with real thickness and real
stopping power. A layout mask has no thickness, so it cannot physically stop an ion. The tool
is warning that it has been asked to model a physical blocking process with a non-physical
object.

**Why it matters.** For a normal-incidence implant into a large open area, the geometric
approximation is nearly harmless. For a **tilted** implant — the halo, for instance — it is
not, because a real photoresist layer of finite thickness casts a *shadow* whose extent
depends on the tilt angle and the resist height. A zero-thickness mask casts no shadow, so the
implant lands in places it physically could not reach, and the halo profile near the gate edge
is wrong. Since the halo exists specifically to control short-channel behaviour, that error
propagates straight into the threshold voltage.

**Resolution.** Depositing an actual photoresist layer, patterning it, implanting, then
stripping it — modelling the masking step the way the fab performs it. In the flow as
supplied, the warning is tolerable for the steps it appears on; the value in it is
understanding *when* it would not be.

**Generalisable lesson.** The difference between drawing a device and building one shows up in
exactly this kind of warning. A tool that tells you your abstraction is too coarse for the
physics you asked for is doing you a favour.

---

## Problem 2 — Region naming ambiguity

**Message** (`sprocess`, same flow):

```
** Warning ** Region sorting has ambiguity and may cause mismatched region names
```

**What it means.** As the flow etches, deposits, oxidises and polishes, regions are created,
split and merged. The tool names them automatically, and after enough structural change the
ordering it uses to assign names becomes ambiguous — two regions could legitimately receive
either name.

**Why this is worse than it sounds.** The device deck refers to regions **by name**. A
`Physics(Region="Silicon_1")` block, a refinement box scoped to a region, a doping profile
targeted at a region — all of them are name lookups. If the name-to-region mapping can shift
between runs, then a parameter sweep can silently apply the correct physics to the wrong piece
of silicon in some nodes and not others. You get a full set of results and one of them is
quietly nonsense.

**Resolution.** Name regions explicitly at creation rather than relying on automatic naming,
and after any structurally significant step, verify in Sentaurus Visual that region names
still land where you expect. Which is a small habit: *look at the structure before you
simulate it.*

**Generalisable lesson.** Implicit identifiers are a correctness hazard in any pipeline. If
downstream stages reference upstream objects by an automatically generated name, pin the
names.

---

## Problem 3 — Silently substituted models (the important one)

**Message** (`sdevice`, node `n6592`):

```
Region "Silicon_1" (Material "SiliconGermanium->Germanium"):
  UNDEFINED model "Scharfetter", Silicon default will be used
  UNDEFINED model "Auger", Silicon default will be used
  UNDEFINED model "DopingDependence(electrons)", Silicon default will be used
  UNDEFINED model "DopingDependence(holes)", Silicon default will be used
Check UNDEFINED Models !
```

**What it means.** The deck requested SRH recombination (Scharfetter lifetime), Auger
recombination and doping-dependent mobility in a region whose material is **SiGe grading to
Ge**. The parameter file has coefficients for those models in silicon; it does not have them
for this material. Rather than stopping, `sdevice` substituted the **silicon** values and
continued.

**Why this is the worst failure mode in the whole chapter.** The simulation converges. It
produces a plot. The plot looks entirely plausible. And it is physically wrong, because
germanium is not silicon: its bandgap is roughly 0.66 eV against silicon's 1.12 eV, its
carrier mobilities are substantially higher, and its intrinsic carrier concentration is orders
of magnitude larger. Using silicon lifetimes and silicon mobility coefficients in a Ge region
does not produce a slightly-off answer; it produces a different device. And nothing on screen
tells you.

**Resolution.** Two parts, and both matter.

First, **run with `-CheckUndefinedModels`**. This is the flag that turns this class of silent
substitution into something you cannot miss. I now regard it as the default rather than an
option.

Second, **supply the material parameters**. Either extend the parameter file with a coefficient
set for SiGe/Ge, or — if the material's properties are not important in that region — do not
invoke the models there. The choice depends on whether that region carries physics you care
about, and answering that question is itself the useful part.

**Generalisable lesson.** The most dangerous defect is not the one that crashes; it is the one
that returns a confident wrong answer. Any tool that silently falls back to a default is a
tool whose warnings you must read. This is the single most transferable thing in this chapter,
and it is why I now open the `.err` file before the `.plt` file.

---

## Problem 4 — Missing intermediate file on cleanup

**Message** (`sde`, multiple nodes):

```
rm: cannot remove 'n6710_fps_bnd.tdr': No such file or directory
```

**What it means.** A cleanup step tried to delete an intermediate boundary file that was never
created, because the flow branch in question does not produce one.

**Why it is worth including.** Because recognising a **benign** error is a skill in itself.
This one is cosmetic — nothing downstream depends on the file, and the node completes
correctly. Time spent chasing it is time not spent on Problem 3.

**Resolution.** None needed. It is noise. The judgement call — is this message load-bearing? —
is the actual content, and the way to make it is to ask what depends on the thing that failed.

---

## Problem 5 — Missing run-limits table

**Message** (`gsub`, in four projects):

```
Error (run limits): 'RunLimitsTable' tag hasn't been found.
File name: /opt/STROOT/TCAD2017/tcad/current/lib/glib2/runlimits.xml
```

**What it means.** Workbench's job-submission layer looks for a table describing resource
limits for scheduled runs — the sort of thing that exists on a managed compute cluster with a
queueing system. In a standalone VM there is no such infrastructure, so the tag is absent.

**Why it matters, and why it does not.** It does not affect results: jobs still run locally,
and every simulation in this repository was produced on a VM emitting this message. What it
*does* teach is that the tool is built for an institutional environment — a shared cluster with
job scheduling, licence pools and resource accounting — and a single-user VM is a degraded
configuration of that. Environment-shaped errors are their own category, and distinguishing
"this deployment lacks a facility" from "my simulation is wrong" is a real diagnostic skill.

**Resolution.** Accept it. Same class as Problem 4: understood, and correctly ignored.

---

## Problem 6 — An undefined variable hiding in a deck

**Found by reading** the N-well diode process deck: the file references `$NW_dose2`, while
only `NW_dose1` (and its energy counterpart `Eg_NW_dose1`) are defined.

**What it means.** A latent bug. Depending on the branch taken, `$NW_dose2` either resolves to
nothing or raises a TCL error. It is the residue of an edit — a second well implant that was
parameterised, then removed or renamed, leaving one reference behind.

**Why I am including a bug I found by reading rather than by running.** Because reading decks
critically is the skill this represents. Inheriting a working simulation deck and assuming it
is correct is how errors survive; the same thing is true of inheriting code. Finding this one
also made concrete why the `define X @X@` idiom is good practice — a parameter that appears
exactly once as an SWB token has exactly one place to check.

**Resolution.** Define the missing parameter, or remove the orphaned reference. In a deck I
owned I would remove it, since nothing else references a second dose.

---

## Recurring problem classes

Beyond individual messages, four categories accounted for most of my lost time.

**Non-convergence.** A `Quasistationary` ramp that stalls at a particular bias. Almost never
random. The usual causes, in the order I learned to check them: the step is too large going
into a strongly nonlinear region (reduce `Increment`, lower `MaxStep`); the mesh is too coarse
in a region that has just become electrically important, such as the inversion layer as it
forms (refine there); the solve is not staged, so there is no good initial guess (solve
`Poisson` first, then couple); or the linear solver does not suit the problem (`ILS` for large
systems, `Method=Blocked` with `SubMethod=ParDiSo` for multi-device). *A solve that will not
converge is usually telling you about your mesh or your bias schedule.*

**Meshing.** Structures that meshed but gave implausible results, and structures that failed
to mesh at trench corners. The pattern that worked: refine on gradients rather than on regions,
put `MaxLenInt` on material interfaces, use `MaxTransDiff` so element size does not jump, and
remesh after structural change.

**Disk and resources.** A tree that dies two-thirds through, for no visible physics reason, is
often a full VM filesystem. A hundred-plus nodes each writing structures and plot files adds up
faster than you expect. Similarly, `Number_of_Threads = 4` in a deck is a request; if the VM
has two vCPUs, it is fiction.

**Environment.** Projects invisible to Workbench because they were copied somewhere other than
`/home/sentaurus/STDB/projects/`. Tools not found because `STROOT` and `PATH` were set in one
shell and not in the profile. Licence check-out failures that appear as a tool exiting
instantly with the explanation written only to its log. These are the boring failures, and they
cost the most time at the start because none of them are about semiconductors.

---

## What the debugging taught me that the lectures could not

**Read the error file first.** Almost every hour I wasted, I wasted on something already
written plainly in output I had not opened.

**Warnings are more dangerous than errors.** An error stops you. A warning lets you publish a
wrong number. Problem 3 is the canonical example, and it changed how I work.

**Read the generated file, not the source.** With a preprocessing layer between you and the
tool, the source deck is your intent and the generated deck is reality.

**Classify before investigating.** Is this a physics problem, a numerics problem, a
housekeeping problem or an environment problem? Problems 4 and 5 are safely ignorable; Problem
3 invalidates results. Spending your attention in the right place is most of debugging.

**Reproduce, then change one thing.** Re-running an unchanged failing node produces an
identical failure. Obvious, and I did it anyway, more than once.

---

**Next:** [12 · Key learnings](12-key-learnings.md).
