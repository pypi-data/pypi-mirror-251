# `Travo`: Distributed GitLab ClassRoom

[![PyPI version](https://badge.fury.io/py/travo.svg)](https://badge.fury.io/py/travo)
[![SWH](https://archive.softwareheritage.org/badge/swh:1:dir:1083531372d599755347bcbfb478610ff8339080/)](https://archive.softwareheritage.org/swh:1:dir:1083531372d599755347bcbfb478610ff8339080;origin=https://gitlab.com/travo-cr/travo.git;visit=swh:1:snp:458440b476451270a660b5f905c70db028fed2b4;anchor=swh:1:rev:52687b5bc250b79a7c2c852acad1f900a3770ef6)

## In a nutshell

Are you teaching computer or computational sciences, with hands-on
assignments in the computer lab? Inspired by e.g. GitHub ClassRoom,
`Travo` is a lightweight Python toolkit that helps you turn your
favorite GitLab instance into a flexible assignment management
solution. It does so by automating steps in the assignment workflow
through Git and [GitLab's REST API](https://docs.gitlab.com/ce/api/).

## Motto

*Teaching computer science or computational courses is
all about collaboration on code. It is thus unsurprising that,
with a pinch of salt, forges like GitLab can provide helpful
infrastructure to support and enhance that collaboration.*

## Principles

* Do not impose workflows. Each course and instructor is different.
* Be a small layer. Travo is optional and compatible with standard
  Git & GitLab workflows.
* Do not store data or require an autonomous server. The information
  is already in the Git & Gitlab; just use it.

## Features

- [x] **Trivial to use for students**: simple workflow with only three
      completely automated operations: `fetch`, `submit`,
      `fetch_feedback` (see the [Tutorial](#Tutorial)). No prior
      experience is required other than opening a terminal and
      copy-pasting a command.  
	  For Jupyter users, a widget based student dashboard provides a
	  Graphical User Interface; no terminal needed (see the
	  screenshots below).  
	  Meanwhile students get progressively exposed to using version
	  control and forges, with the incentive to explore more to
	  unleash the full power these tools deliver for more advanced
	  collaboration on code.
- [x] **Battle field tested** with large courses (200+ students at
      lower undergraduate level) with multiple assignments, groups,
      instructors, and sessions.
- [x] **Distributed and personal-data friendly**:
      - you can use any instance of GitLab, e.g. that self-hosted on
        premises by your institution.
      - students and teachers can use their favorite work environment
        (personal laptop, physical computer labs, virtual environments
        on the cloud such as JupyterHub, ...) provided the required
        software for the course is installed, together with Travo.
- [x] **Command line interface** for most common usages.
- [x] Reusable Python library to develop custom extensions, workflows,
      dashboards, e.g. within Jupyter.
- [x] Instructor side: utilities to help with the preparation,
      distribution, monitoring, automatic grading by continuous
      integration. Some familiarity with version control and GitLab is
      required since Travo mainly automatizes tedious manual
      operations.
- [x] Collect GitLab pipeline reports for feedback or grading
- [x] **Dedicated utilities for Jupyter-based assignments**:
      [nbgrader](https://nbgrader.readthedocs.io/) integration for
      automatic and manual grading, ...
- [x] **Lightweight and sustainable**: Travo is meant to reuse as much
      of your favorite infrastructures and tools as possible, focusing
      on just a bit of glue (~3k lines of code) to hold them together
      for that particular application.
- [x] **Modular and extensible**: you use whichever part of Travo is
      convenient for you and ignore or extend or replace the rest.
      For example, instructors can setup tailored CLI Python scripts
      for their courses.
- [x] **Internationalization**: French, English (in progress); more
      languages can be added.
- [x] Designed to be generalizable for other forges.
- [x] Travo is based on a general purpose Python module to interact
      with GitLab through its API which could serve other purposes.

## Screenshots

Fetching and submitting assignments from the terminal:

```shell
./course.py fetch Assignment1
```

```shell
./course.py submit Assignment1
```

The student dashboard for Jupyter users :

![Student dashboard](docs/sources/talks/student_dashboard.png)

Overview of student submissions on GitLab :

![student submissions](docs/sources/talks/vue-soumissions-groupe.png)

## [Tutorial](docs/sources/tutorial.md)


## Requirements and installation

Requirements: Python >= 3.6

Installation:

    pip install travo

Tips:
- you may need to use `pip3` instead of `pip` to force the use of
  Python 3.
- If using `pip` as provided by your operating system, you may need to
  use `sudo` to install `travo` system wide (sometimes, the user
  installation is unusable due to `~/.local/bin` not being in the
  users' path)

## Authors

Pierre Thomas Froidevaux, Alexandre Blondin-Massé, Jean Privat, and
Nicolas M. Thiéry, with contributions from Jérémy Neveu and Viviane
Pons.

Feedback and contributions are most welcome!

## Tiny history and status

Travo started in Spring 2020 at [UQAM](https://uqam.ca/) as a Python
shell script. See the
[Legacy User Interface](https://gitlab.info.uqam.ca/travo/travo-legacy).
The user interface was completely refactored in Summer and Fall 2020.
Travo was then reimplemented in Python in Winter 2021 and continuously
expanded since.

## Status and future evolutions

Travo is used in production in a dozen large classes at [Université
Paris-Saclay](https://universite-paris-saclay.fr/) and
[UQAM](https://uqam.ca/), and many other smaller
classes. Nevertheless, it is still **a work in progress**!

**Documentation:** The tutorials could use some more love. On the
other hand we would be very happy to help you get started as this is
the most efficient approach to explore new use cases and improve the
documentation. Get in touch!

**Better messages:** less verbosity by default; provide tips on what
to do next.

**Internationalization:** Basic support for internationalization has
been set up, and many, but not all, messages are available both in
French and English. The next steps are to scan the Travo library to
use internationalization in all messages, and to translate the
messages. Contributions welcome!

**Support for collaborative work:** in progress, with experimental
support for modeling teams of students working collaboratively on an
assignment, with basic tooling for students. Tooling for instructors
remains to be implemented.

**Graphical User Interface within Jupyter:** in progress, with a
student dashboard and an experimental instructor dashboard.

**Forge agnosticism:** Currently, only GitLab is supported, but the
code was designed to be modular to make it easy to support other
forges (e.g. GitHub).

**Automatic grading:** support for a wider range of use cases beyond
Jupyter assignments; tighter integration with nbgrader for Jupyter
assignments.
