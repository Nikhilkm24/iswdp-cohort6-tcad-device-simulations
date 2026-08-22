# 04 · Sentaurus Workbench and Design of Experiments

Sentaurus Workbench is the part of the suite that a newcomer underestimates and an
experienced user leans on hardest. This chapter explains the layer that turns a single
simulation into an experiment.

## The problem SWB solves

Suppose you want to know how the halo implant dose affects short-channel behaviour. Done by
hand that means: edit the dose in the process deck, run it, rename the output so it does
not get overwritten, run the device simulation on it, rename that output, plot it, note
which curve was which, and repeat six times. Then your supervisor asks what happens if the
gate length also changes, and you have thirty-six runs and a naming scheme you no longer
trust.

Every part of that except "decide what to vary" is bookkeeping, and bookkeeping done by
hand is where results get silently corrupted. SWB replaces it with a declarative structure:
you state the flow, state the parameters, state the values, and SWB generates and tracks
every run.

## Anatomy of a project

An SWB project has three things in it.

**A tool flow.** An ordered list of tools, each with a command file: for example
`sprocess → sde → sdevice → svisual`. Each tool consumes what the previous one produced.

**A parameter set.** Named variables — implant dose, energy, depth, gate voltage, a switch
that selects an analysis type — with the values to explore.

**A node tree.** The expansion of the flow across the parameter values. Each **node** is
one concrete run of one tool at one point in parameter space, identified by a number
(`n15038`, `n6586`, `n12560`). Nodes downstream of a split inherit from their parent, so a
process split that produces six structures and a device simulation that sweeps four gate
voltages gives twenty-four device nodes over six process nodes — the process work is done
once per structure, not once per combination. That sharing is the reason the tree is a tree
rather than a flat list, and it is where the compute saving comes from.

The tree is stored in **`gtree.dat`**. Reading `gtree.dat` is how you find out what a
project actually does, and it is the first file I open in an unfamiliar project.

## Parameterisation: the `@…@` layer

SWB preprocesses each command file before the tool sees it, substituting `@name@`
placeholders. The vocabulary is small and worth knowing exactly:

| Token | Meaning |
| --- | --- |
| `@param@` | The value of parameter `param` for *this* node |
| `@node@` | This node's number — used to build unique output filenames |
| `@node:index@` | This node's index within its sweep, so scripts can vary behaviour per node |
| `@previous@` | The preceding node in the flow |
| `@node|-1@` | The node one step back — used to load the prior tool's output |
| `@tdr|nmos@` | A scoped reference: the structure file from the branch named `nmos` |
| `@Prefix@` | The generated file-name prefix for the node |

A common idiom is to lift a parameter into a TCL variable at the top of a deck:

```tcl
define NW_dose1 @NW_dose1@
```

after which the rest of the deck uses `$NW_dose1` normally. This is a small thing with a
real benefit: the parameter appears exactly once as an SWB token, so there is one place to
look when a substitution goes wrong, and the deck below it reads as ordinary TCL.

Output naming follows the same idea — `n@node@_msh`, `"n@node@_sys_des.plt"`,
`@log@`. Because the node number is baked into every filename, results from different
points in parameter space cannot collide. The generated per-node file appears on disk as
`n<NNNN>_fps.cmd` (or `_dvs.cmd`, `_des.cmd`, `_vis.tcl`), and **that** is the file to read
when a node misbehaves: it shows what the tool actually received after substitution, which
is not always what you thought you wrote.

## Conditional execution

SWB's preprocessor also does control flow over whole blocks, which is how one deck serves
several analyses:

```
#if @CV@ == 0
#noexec
#endif
```

Here `CV` is an ordinary SWB parameter. When it is `0`, the enclosing block is switched off
and `#noexec` tells SWB not to run the tool for that node at all. In practice this is how a
project offers both a DC characterisation branch and a C-V branch from a single source
file, rather than maintaining two near-identical decks that will inevitably drift apart.

The layering is important and is a genuine source of confusion:

```
   source deck ──▶ [ SWB preprocessor: @param@, #if, #noexec ]
                          │
                          ▼
              generated n<NNNN>_*.cmd ──▶ [ TCL interpreter: set, expr, if ]
                                                 │
                                                 ▼
                                          [ tool executes commands ]
```

Three interpreters, in order. A `#if` is resolved before TCL ever runs, so it cannot depend
on a TCL variable; conversely a TCL `if` cannot skip a tool invocation, because by then the
tool is already running. Half the "why is this not working" moments in a deck come from
expecting one layer to do the other's job.

## Scale, in practice

The Advanced course projects are not toy sweeps. The reference projects I ran carry node
trees in the range of roughly **85 to 125 nodes** each, across eleven projects covering the
N-well diode, 1D N-well profiles, the 28 nm NMOS and PMOS flows, the NMOS capacitor, 3D
structures and TLP/ESD analysis. Running these on a laptop VM is what makes the cost of a
DOE tangible rather than abstract: you plan a sweep differently once you have watched a
hundred nodes execute.

The parameter studies the material is built around are a good illustration of what TCAD is
*for*, since each one is a question you cannot answer with a single simulation:

- **Halo implant** — peak doping, depth and position, each against both
  I<sub>d</sub>-V<sub>g</sub> and I<sub>d</sub>-V<sub>d</sub>. The halo exists to control
  short-channel threshold roll-off, and its position matters as much as its dose.
- **Vt-adjust implant** — the same three-way variation. This is the most direct handle on
  threshold voltage, and seeing the transfer curve translate as the peak moves is the
  clearest possible demonstration of the link between recipe and specification.
- **N-well doping** — against transfer characteristics, output characteristics *and* the
  resulting doping profile, so you can see cause and effect in the same sweep.
- **Tap geometry** — well-tap length, depth and doping variation, which is where substrate
  resistance and latch-up-adjacent behaviour live.

> **Provenance.** The eleven reference projects, their `gtree.dat` split trees and the
> pre-computed sweep data shipped with them are instructor-authored course material dated
> 2023–2024. My work was executing them, varying parameters, and interpreting the output.
> See [`../PROVENANCE.md`](../PROVENANCE.md).

## Running a tree without wasting a weekend

The habits that made SWB workable on a laptop:

**Run one node of each tool first.** A syntax error in the first process deck will fail
identically in all ninety nodes. Validate the chain on a single path before expanding.

**Use `#noexec` deliberately.** If you only need the C-V branch, do not compute the DC
branch. The cheapest simulation is the one you decide not to run.

**Read the generated `n<NNNN>_*.cmd`, not the source deck.** When a node fails and the
source looks correct, the substitution is the suspect. The generated file settles it in
seconds.

**Let nodes inherit.** If a device sweep is failing, re-run the device nodes; the process
nodes above them are unchanged and re-running them is pure waste. Understanding the
inheritance structure is what makes an iteration loop fast.

**Watch the disk.** Structures and plot files per node add up, and a tree that dies
mysteriously two-thirds through is often a full filesystem rather than a physics problem.

---

**Next:** [05 · Scripting — TCL, Scheme and the SWB preprocessor](05-scripting-tcl-scheme-swb.md).
