# 03 · Environment Setup

This is the least glamorous chapter and the one I would most want a hiring engineer to
read, because "can you get a real toolchain running" is a real skill and most coursework
never tests it. Nothing in the Advanced level could start until the environment worked.

## Two environments, and why there are two

Sentaurus TCAD is licensed, Linux-native, and heavy. ISWDP solves the access problem twice
over, and I used both solutions.

**Levels 1–2 — IISc remote compute.** Sessions ran against IISc's lab hosts,
`ancl2.dese.iisc.ernet.in` and `ancl3.dese.iisc.ernet.in`, reached over **VNC** with
per-participant credentials, running Sentaurus **R-2020.09-SP1**. Everything was
pre-configured: licences, paths, project database. The learning here is about working on
shared infrastructure — the machine is not yours, the session is scheduled, latency is
real, and a run you launch carelessly costs someone else time. It teaches you to think
before pressing Run, which is a habit worth having.

**Advanced — a local virtual machine.** For the Advanced level the program distributes a
self-contained simulation appliance so that participants can run process simulations
without competing for shared compute. This is the environment all of my Advanced work
happened in, and building it was the first task of the level.

## The Advanced VM

| Component | What it was |
| --- | --- |
| Host | Windows |
| Hypervisor | **VMware Workstation Player 17.5.2** (build 23775571), with VMware Workstation 15.0.0 as the documented fallback |
| Guest OS | **RedHat Advanced Server 6.6** |
| Toolchain | Synopsys Sentaurus TCAD **N-2017.09 / N-2017.09-SP2** |
| Tool root | `/opt/STROOT/TCAD2017/` |
| Project database | `/home/sentaurus/STDB/projects/` |

Two things about this are worth understanding rather than just noting.

**Why RedHat 6.6 in 2025.** Because Sentaurus N-2017.09 was qualified against it. EDA
tools are validated against specific OS and library versions and are not casually portable
— the tool links against particular glibc and X11 versions, the licence daemon expects a
particular environment, and "just run it on Ubuntu" produces a long afternoon of missing
shared objects. Shipping a known-good guest image is the correct engineering answer, and
recognising *why* an EDA vendor pins an ancient distribution is itself part of learning the
industry.

**Why a VM at all rather than a container.** The suite is a GUI-heavy X11 application stack
with a licence daemon and a large on-disk tool tree; a full virtual machine with a working
desktop is simply the path of least resistance, and it also means the whole environment can
be handed to a participant as one artefact.

## What setup actually involved

The program supplied two documents — a TCAD environment setup guide (issued at Level 2)
and an instruction sheet on getting a folder from the Windows host into the VMware guest —
and the work broke down as follows.

**1 · Install the hypervisor.** VMware Player 17.5.2 on the Windows host. The main
practical prerequisite is enabling hardware virtualisation in firmware, and on Windows
being aware that Hyper-V and third-party hypervisors contend for the virtualisation layer.

**2 · Import and provision the guest.** Open the supplied VM, then size it honestly.
Process simulation with Monte-Carlo implantation is CPU- and memory-hungry, and the decks
themselves ask for parallelism — the inverter deck sets `Number_of_Threads = 4`, so
allocating fewer vCPUs than that makes the setting a lie. Under-provisioning here is the
single easiest way to make every subsequent run feel broken.

**3 · Move the project bundle into the guest.** The Advanced course material arrives as a
project folder to be imported into the guest's Sentaurus project database. This is the step
the instruction sheet existed for, and it is genuinely a small trap: VMware shared folders
depend on VMware Tools being installed and running in the guest, and on a RedHat 6.6 guest
that is not something you can assume. The destination is
`/home/sentaurus/STDB/projects/`, which is where Sentaurus Workbench looks for projects —
put the folder anywhere else and SWB simply will not see it, with no error to explain why.

**4 · Set up the tool environment.** Sentaurus is driven by `STROOT`: the tool root is
exported, the tool `bin` directory goes on `PATH`, and the licence path must resolve.
Concretely, the pattern is to point `STROOT` at `/opt/STROOT/TCAD2017` and prepend
`$STROOT/bin` to `PATH` in the shell profile, so that `swb`, `sprocess`, `sde`, `sdevice`
and `svisual` are all on the path in every new terminal. Getting this into the profile
rather than typing it per session matters more than it sounds: a half-set environment is
how you end up running one tool from the correct tree and another from somewhere else.

**5 · Verify the licence.** Sentaurus checks out a licence per tool invocation. A licence
failure looks like a tool that starts and immediately dies, and the message is in the
tool's log rather than on the terminal — so the first thing to learn is *where the tool
writes its complaints*, which is the same lesson every later debugging session repeats.

**6 · Launch and confirm the full flow.** `swb`, open the imported project, confirm that
the tool flow resolves, and run a single node end to end so that `sprocess`, `sde`,
`sdevice` and `svisual` have each actually executed at least once. Until a node goes green
through the whole chain, the environment is not verified — it is only hopeful.

## Sanity checks I came to rely on

Small, cheap, and they save hours:

- **Does `swb` see the project?** If a project you copied in does not appear, it is almost
  always in the wrong directory rather than corrupt.
- **Is the disk going to hold this?** A DOE with a hundred-plus nodes writes a `.tdr`
  structure and plot files per node. Process simulation output is not small, and a VM disk
  fills quietly. A run that dies late for no visible reason is often a full filesystem.
- **Run one node before running the tree.** Launching a whole split tree and discovering at
  node 3 that the very first tool has a syntax error wastes a lot of wall-clock time on a
  laptop.
- **Read the node's `.err` and `.log` before re-launching.** Re-running an unchanged failing
  node produces an identical failure. This sounds obvious; it is nonetheless the mistake I
  made most often at the start.
- **Snapshot the VM before changing anything structural.** Free, instant, and the reason a
  broken environment is a ten-second recovery instead of a re-import.

## The environment as part of the skill

By the end of the Advanced level I had a self-contained, reproducible TCAD environment on
my own machine and could take a project from import to plotted result without help. That
is a small thing to state and it was not a small thing to achieve, and it is the
precondition for everything in the rest of this repository — every node number, every
field plot, every error message quoted in [11 · Debugging log](11-debugging-log.md) came
out of this VM.

> **Provenance note.** The VM image, the hypervisor installers and the course project
> bundle are not redistributable and are not in this repository; they are excluded by
> [`../.gitignore`](../.gitignore). What is documented here is my configuration work, not
> their software. See [`../PROVENANCE.md`](../PROVENANCE.md).

---

**Next:** [04 · Workbench and design of experiments](04-workbench-and-doe.md) —
how SWB turns one deck into a parameter study.
