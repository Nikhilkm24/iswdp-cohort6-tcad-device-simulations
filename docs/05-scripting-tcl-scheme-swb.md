# 05 · Scripting: TCL, Scheme and the SWB Preprocessor

My resume says I learned scripting for TCAD automation. This chapter is what that means
precisely, including the part most people get wrong.

## Three languages, not one

Sentaurus command files look superficially alike and are not the same language.

| File | Tool | Language |
| --- | --- | --- |
| `sprocess_fps.cmd` | Sentaurus Process | **TCL** (embedded interpreter) |
| `sdevice_des.cmd` | Sentaurus Device | **TCL** (embedded interpreter) |
| `sde_dvs.cmd` | Sentaurus Structure Editor | **Scheme** |
| `svisual_vis.tcl` | Sentaurus Visual | **TCL** |

`sde` being Scheme is the one that catches people out. Its commands are parenthesised
prefix expressions:

```scheme
(sde:build-mesh "snmesh" "-a -c conforming" "n@node@_msh")
```

That is not TCL with unusual punctuation; it is Scheme, with Scheme's evaluation rules. I
state this flatly because claiming "I wrote TCL for structure editing" would be wrong, and
a reviewer who knows the suite would spot it immediately. The honest claim is: **process
and device decks are TCL, Sentaurus Visual scripts are TCL, structure editor scripts are
Scheme, and I worked with all three.**

Layered on top of all of them is the **SWB preprocessor**, which is not a language so much
as a substitution and conditional-inclusion pass. It runs first, before any interpreter
sees the file. The ordering was covered in
[04 · Workbench and DOE](04-workbench-and-doe.md) and is the single most useful thing to
hold in your head when a deck misbehaves.

## What TCL buys you inside a process or device deck

Because `sprocess` and `sdevice` embed a TCL interpreter, a deck is a *program*, not a
configuration file. You get variables, arithmetic, conditionals, loops, string handling and
procedures alongside the tool's own commands. Concretely, that means:

**Parameters instead of magic numbers.** A dose written as `1e13` in six places is six
places to forget. Bound once to a variable and referenced thereafter, it is one.

```tcl
define NW_dose1 @NW_dose1@
```

**Derived quantities.** If an implant energy should scale with a depth you are varying, you
compute it with `expr` rather than maintaining a table of pre-multiplied values by hand.

**Conditional process steps.** A deck can grow an oxide or deposit one depending on a
switch, so that a comparison between the two is a parameter change rather than a second
file.

**Structural repetition.** A four-rotation implant is the same implant at 0°, 90°, 180° and
270°; expressing that as a loop over rotation angles rather than four pasted blocks means a
change to the dose is one edit and cannot be applied inconsistently.

The general point is the one that applies to any engineering codebase: the value of putting
logic in the deck is not cleverness, it is that inconsistent duplication becomes
impossible.

## Sentaurus Visual scripting, annotated

This is where I did the most substantive scripting work, because it is where the Advanced
level explicitly teaches automation. The pattern below is the course's on-resistance
extraction script; I have annotated it because reading it line by line is what taught me
the `svisual` API.

> **Provenance.** The code in this section is an excerpt from the course-supplied
> `svisual_vis.tcl` in the `Sdevice-I-II_NMOS_28nm_AC_Simulation` reference project. The
> annotation is mine. See [`../PROVENANCE.md`](../PROVENANCE.md).

**Declaring the dependency and loading the extraction library.**

```tcl
#setdep @node|sdevice@
load_library extract
lib::SetInfoDef 1
```

The `#setdep` comment is read by SWB, not by TCL: it tells the Workbench that this
visualisation node depends on the `sdevice` node, so the tree knows the ordering.
`load_library extract` pulls in the parameter-extraction library — this is what makes
`svisual` an analysis tool rather than a plotting tool.

**Node identity and deterministic colours.**

```tcl
set N  @node@
set i  @node:index@
set COLORS  [list green blue red orange magenta violet brown]
set NCOLORS [llength $COLORS]
set color   [lindex $COLORS [expr $i%$NCOLORS]]
```

This is the small idea I liked most in the whole script. When a sweep produces a dozen
curves in one plot, they must be distinguishable — and colours assigned by hand will be
wrong the moment the sweep length changes. Indexing a colour list modulo its length by the
node's own sweep index means the colouring is automatic, stable and never collides for
sweeps up to seven wide. It costs three lines and removes an entire category of manual
work.

**Creating the plot idempotently.**

```tcl
if {[lsearch [list_plots] Plot_IdVd] == -1} { create_plot -1d -name Plot_IdVd }
select_plots Plot_IdVd
```

Every node in the sweep runs this same script, but only the first should *create* the plot;
the rest must add their curve to the existing one. The guard is what makes many nodes
accumulate into one figure instead of each producing its own.

**Loading the data and building the curve.**

```tcl
load_file @Vd@_n@node|-1@_des.plt -name PLT_IdVd($N)
set Vds [get_variable_data "Drain OuterVoltage" -dataset PLT_IdVd($N)]
set Ids [get_variable_data "Drain TotalCurrent"  -dataset PLT_IdVd($N)]
create_curve -name IdVd($N) -dataset PLT_IdVd($N) \
    -axisX "Drain OuterVoltage" -axisY "Drain TotalCurrent"
```

`@node|-1@` reaches back to the `sdevice` node that produced the data, so the filename is
constructed rather than hard-coded. The dataset and curve names are keyed on the node
number, which is what keeps twelve nodes' worth of data separate in one `svisual` session.
Note that the same variables are also pulled into plain TCL lists — the curve is for the
human, the lists are for the extraction.

**Labelling from parameters.**

```tcl
set_curve_prop IdVd($N) -label "($N): Vgs=@Vgs@" -color $color -line_style solid -line_width 3
```

The legend entry carries both the node number and the gate voltage *for that node*, taken
from the SWB parameter. A legend that cannot go stale is worth more than a tidy one.

**Extracting a parameter, not just drawing it.**

```tcl
set Vo 0.3
ext::ExtractRdiff out= Ron name= "Ron" v= $Vds i= $Ids vo= $Vo
echo "Ron (Vd = $Vo V) is [format %.3f $Ron] Ohm"
```

`ext::ExtractRdiff` computes the differential resistance from the I-V data at a specified
operating point — here on-resistance at V<sub>d</sub> = 0.3 V, in the linear region where
R<sub>on</sub> is meaningful. This is the step that turns a picture into a number, and a
number is what goes into a specification or a comparison against measurement. Discussed
further in [10 · Calibration and extraction](10-calibration-and-extraction.md).

**Presentation, scripted.**

```tcl
set_axis_prop -plot Plot_IdVd -axis x -title "Vd (V)" -title_font_size 20 \
    -scale_font_size 18 -title_font_att bold
set_legend_prop -plot Plot_IdVd -label_font_family arial -label_font_size 12 \
    -label_font_color #000000 -label_font_att bold
## export_view Fig_n@node@_IdVd.eps -plots Plot_IdVd -format eps -overwrite
```

Axis titles with units, readable font sizes, and a commented-out vector export. It looks
like fussiness; it is the difference between a plot you can put in front of someone and a
plot you have to explain. The commented `export_view` is the hook that makes the whole
flow headless — uncomment it and the figure is produced as a file with no interactive
session at all.

## What I can do with this

Stated at the level I would defend in an interview:

- Read a `sprocess` or `sdevice` deck and explain what every block does.
- Modify a deck: change parameters, add or remove process steps, switch model sets, alter a
  bias schedule, add a new analysis.
- Use TCL control flow and variables inside a deck to parameterise it and remove duplicated
  values.
- Read Scheme-based `sde` structure scripts and modify geometry, regions, contacts, doping
  and refinement.
- Write and adapt `svisual` TCL: create and select plots, load `.plt` datasets, extract
  named variables into lists, build and style curves, drive colour and labelling from node
  index and parameters, and call the `extract` library to pull parameters out of curves.
- Understand and debug the interaction between SWB substitution, TCL evaluation and tool
  execution — including reading the generated per-node command file to see what the tool
  actually received.

What I would **not** claim: that I authored the course's process and device decks from
scratch. I did not, and [`../PROVENANCE.md`](../PROVENANCE.md) says so. What I did was
learn to read them fluently, change them with intent, and script the analysis around them —
which is what the job actually consists of.

## The transferable part

Underneath the syntax, the Advanced level's scripting content is about three ideas that are
not specific to TCAD at all: **parameterise instead of duplicating**, so that a change
happens in one place; **automate the analysis, not just the run**, so that results and
figures are regenerated together and stay in sync; and **make outputs self-describing**, by
keying filenames, dataset names and legend labels on the identity of the run that produced
them. Those three habits are why the figures in this repository can be traced back to
specific nodes, and they are the part of this chapter I expect to still be using in ten
years.

---

**Next:** [06 · Process simulation](06-process-simulation.md) —
building a device the way a fab would.
