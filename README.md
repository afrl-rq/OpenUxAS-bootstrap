OpenUxAS-bootstrap
==================

[![Github Actions](https://github.com/afrl-rq/OpenUxAS-bootstrap/workflows/Checks/badge.svg)](https://github.com/afrl-rq/OpenUxAS-bootstrap/actions)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This respository is designed to get you up and running with [OpenUxAS](https://github.com/afrl-rq/OpenUxAS) development as quickly and efficiently as possible.
This repository contains scripts to help you configure your environment and provides a fully automated, reproducible build for OpenUxAS.

OpenUxAS is complex project, so there's a lot to talk about here.
If you want to get started using OpenUxAS as quickly as possible, you can jump to the [quick-start guide](#quick-start).
We've organized this README into sections, to simplify navigation.

*Table of Contents*

1. [Quick Start](#quick-start)
2. [Bootstrapping OpenUxAS](#getting-started)
   1. [Basic Requirements](#uxas-requirements)
   2. [OpenUxAS Users](#uxas-users)
   3. [OpenUxAS Developers](#uxas-developers)
   4. [Ada Development](#uxas-ada)
3. [Detailed Discussion](#detailed-information)
   1. [Organization of this Repository](#organization)
   2. [Install Support](#install)
   3. [The Anod Build System](#anod)
      1. [What is Anod?](#what-is-anod)
      2. [Why Anod?](#why-anod)
      3. [Understanding Anod](#anod-understanding)
      4. [Using Anod during OpenUxAS Development](#anod-development)
   4. [Division of Labor: OpenUxAS and OpenUxAS-bootstrap](#division)
      1. [Adding a New Dependency to OpenUxAS](#new-dependency)
4. [Troubleshooting](#troubleshooting)
   1. [Verbosity](#verbosity)

There are three components discussed in this README:

1. [OpenUxAS](https://github.com/afrl-rq/OpenUxAS) — the project that you wish to use or develop.
2. OpenUxAS-bootstrap — this repository, which provides build automation and a preconfigured environment.
3. Anod — the system used to provide a fully automated and reproducible build for OpenUxAS.

Throughout the remainder of the README, we will write commands that you should enter in your Linux terminal like this:

    ~/bootstrap$ command argument

This means that you have changed to the directory `~/bootstrap` in your Linux machine and you are going to execute the command `command` with the arguments `argument`.
If you would like to copy-paste commands from this README, you should only copy the part that begins after the `$`.


# 1. Quick Start<a name="quick-start" />

The simplest approach to getting up and running with OpenUxAS is discussed in this section.
If you wish to develop for OpenUxAS or wish to better understand the install process, refer to the [next section](#getting-started), which offers more complete information.

Before you begin, you will need:

1. Ubuntu 20.04
2. curl
3. git
4. python 3.8

Bootstrap your install by running this command:

    ~$ curl -L https://github.com/afrl-rq/OpenUxAS-bootstrap/raw/develop/install/bootstrap | bash

Configure your environment to run the build tool:

    ~$ eval "$( cd ~/bootstrap && install/install-anod-venv --printenv )"

Build OpenUxAS and OpenAMASE:

    ~/bootstrap$ ./anod build uxas
    ~/bootstrap$ ./anod build amase

Now you can run the OpenUxAS examples:

    ~/bootstrap$ ./run-example 02_Example_WaterwaySearch


# 2. Bootstrapping OpenUxAS<a name="getting-started" />

One of the aims of this repository is to simplify to the greatest extent practicable the process of getting started with OpenUxAS.
There are two perspectives we target:

1. User: someone who wishes to try out or use OpenUxAS; and
2. Developer: someone who wishes to contribute to or extend OpenUxAS.

Both of these use cases share the same basic requirements, presented below.

## 2.1. Basic Requirements<a name="uxas-requirements" />

This repository makes assumptions about the platform on which OpenUxAS will be built.
We assume — that is, we have tested with — the following configurations:

1. Linux, specifically Ubuntu 18.04 or Ubuntu 20.04
2. curl
3. git
4. python 3.7 or 3.8

> _**Note**: The system python on Ubuntu 18.04 is python 3.6._
> _This version of python is **not** supported._
> _If you must use Ubuntu 18.04, use [pyenv](https://github.com/pyenv/pyenv) to install python 3.8._
> _(But really, just use Ubuntu 20.04.)_

Other dependencies required for OpenUxAS will be installed either by the install scripts in this repository or will be built as part of the reproducible build of OpenUxAS.

> _**Note**: OpenUxAS can be built on other platforms, however the install scripts provided in this repository will probably not work correctly on them._

If you're not a Linux user, we recommend that you install a virtual machine provider, like [VirtualBox](https://www.virtualbox.org/wiki/Downloads).
Then, we recommend that you download the desktop image of [Ubuntu 20.04](https://releases.ubuntu.com/20.04) and create a virtual machine from the image.
VirtualBox will help you do this; many tutorials can be found on the Internet that will help you with this step.

> _**Note**: the default settings suggested by VirtualBox are not appropriate for building and running OpenUxAS._
> _You should make sure to provide at least **8GB of RAM** and **20GB of disk space**._

## 2.2. OpenUxAS Users<a name="uxas-users" />

There are three steps you need to complete before you can use OpenUxAS:

1. install the build system
2. configure your environment for the build
3. build OpenUxAS and OpenAMASE

Once these steps are completed, you can run OpenUxAS.

### 2.2.1. Install the Build System

To get started as a user of OpenUxAS, simply run this command in a terminal:

    ~$ curl -L https://github.com/afrl-rq/OpenUxAS-bootstrap/raw/develop/install/bootstrap | bash

The command will fetch the shell script named `bootstrap` from the `install` directory in this repository's develop branch and will then execute the script using `bash`.
The script will confirm that basic dependencies are met and will then clone this repository and execute the `install` script in the `install` directory in this repository. 

Once the command has successfully executed, you will have a new directory `bootstrap` in your home directory.

> _**Note**: if you have already cloned this repository, you should not run the `curl` command above, and instead should simply run `install/install`._
> _The installer will run in interactive mode, so you will be able to make choices about what actions it should take._

### 2.2.2. Configure Your Environment for the Build

To use the build system in `bootstrap`, you need to configure your environment.
You can do so like this:

    ~$ eval "$( cd ~/bootstrap && install/install-anod-venv --printenv )"

If you do not wish to enter this command each time you want to build OpenUxAS, you can add it to your profile.

### 2.2.3. Build OpenUxAS and OpenAMASE

Now, you can build OpenUxAS and OpenAMASE:

    ~/bootstrap$ ./anod build uxas
    ~/bootstrap$ ./anod build amase

### 2.2.4. Running OpenUxAS

The best way to get a feel for OpenUxAS is to run one of the examples provided with OpenUxAS.
You can do that like this:

    ~/bootstrap$ ./run-example 02_Example_WaterwaySearch

OpenAMASE will start and OpenUxAS will be launched in a separate process.
Click on the run button in OpenAMASE once the OpenAMASE window opens.
The scenario will start.

You can get a listing of the other examples that can be run with `run-example` by using:

    ~/bootstrap$ ./run-example --list

## 2.3. OpenUxAS Developers<a name="uxas-developers" />

The steps required to start developing OpenUxAS are more complex than those required to start using OpenUxAS.
The added complexity arises primarily because we expect that developers will want a fair degree of control over their development environment so that they can tailor their environment to suit their experience and preference.

We provide two approaches to developer setup:
1. automated: we provide a script that configures OpenUxAS, OpenAMASE, and LMCPgen for development
2. manual: we provide instructions for how to flexibly configure any of the above for development

### 2.3.1. Automatic Developer Setup

To get started as a developer of OpenUxAS, simply run this command in a terminal:

    ~$ curl -L https://github.com/afrl-rq/OpenUxAS-bootstrap/raw/develop/install/bootstrap | DEVEL=1 bash

The command will fetch the shell script named `bootstrap` from the `install` directory in this repository's develop branch and will then execute the script using `bash`.
The script will confirm that basic dependencies are met and will then clone this repository and execute the `install` script in the `install` directory in this repository. 

Once the command has successfully executed, you will have a new directory `bootstrap` in your home directory.
Within the `bootstrap` directory, you will have a directory `develop`.
The `develop` directory contains:
- `LmcpGen` - a clone of the LmcpGen repository
- `OpenAMASE` - a clone of the OpenAMASE repository
- `OpenUxAS` - a clone of the OpenUxAS repository

The contents of these three repositories will be used whenever OpenUxAS is built with anod.

### 2.3.2. Manual Developer Setup

To get started as a developer of OpenUxAS, simply run this command in a terminal:

    ~$ curl -L https://github.com/afrl-rq/OpenUxAS-bootstrap/raw/develop/install/bootstrap | bash

The command will fetch the shell script named `bootstrap` from the `install` directory in this repository's develop branch and will then execute the script using `bash`.
The script will confirm that basic dependencies are met and will then clone this repository and execute the `install` script in the `install` directory in this repository. 

Once the command has successfully executed, you will have a new directory `bootstrap` in your home directory.

You may clone OpenUxAS, OpenAMASE, or LCMPgen manually, placing them wherever you would like.
Then, you need to tell the build system that it should use your clone, rather than a fresh checkout of the repository.
You do this by editing `specs/config/repositories.yaml`.
Here's an example of how you would update the entry for OpenUxAS:

    openuxas:
      vcs: external
      url: /absolute/path/to/your/clone
      revision: None

Alternatively, you can use anod to clone the repository for you, like this:

    ~/bootstrap$ ./anod devel-setup uxas

Anod will clone OpenUxAS, placing it in `bootstrap/develop/OpenUxAS` and will update the `repositories.yaml` file for you.
You can configure where `anod devel-setup` places the repository using command-line options; see `anod devel-setup --help` for complete options.

### 2.3.3. Configure Your Environment for the Build

To use the build system in `bootstrap`, you need to configure your environment.
You can do so like this:

    ~$ eval "$( cd ~/bootstrap && install/install-anod-venv --printenv )"

If you do not wish to enter this command each time you want to build OpenUxAS, you can add it to your profile.

### 2.3.4. Build OpenUxAS and OpenAMASE

Now, you can build OpenUxAS and OpenAMASE:

    ~/bootstrap$ ./anod build uxas
    ~/bootstrap$ ./anod build amase

### 2.3.5. Configure Your Environment to Run OpenUxAS or OpenAMASE

You can use anod to automatically configure your environment to run OpenUxAS, OpenAMASE, or any of the other components that anod builds.
For example, to configure your environment to run OpenUxAS:

    ~/bootstrap$ eval "$( ./anod printenv uxas )"
    ~/bootstrap$ eval "$( ./anod printenv amase )"

Note that this step is performed automatically if you use the `run-example` script that is provided in this repository.
You will need to perform this step only if you plan to run OpenUxAS some other way (either manually or using the `run-example` script provided in the OpenUxAS repository).

If you do not wish to enter these commands each time you want to run OpenUxAS, you can add it to your profile.

### 2.3.6. Configure Your Environment to Build OpenUxAS Manually

If you develop OpenUxAS, you will probably not want to use anod to rebuild OpenUxAS each time you make changes.
As is explained [below](#anod), anod will completely rebuild OpenUxAS whenever any change is made, as though you had cleaned the build first.
Instead, you should use `make` to build OpenUxAS.

Change to your OpenUxAS clone and build OpenUxAS using `make`:

    /path/to/OpenUxAS$ make all

Once you are finished making modifications to OpenUxAS and before you push your changes, you should re-run the anod build.
Essentially, this will repeat on your local machine the same build that will be performed during continuous integration, ensuring that your build is consistent and reproducible.

## 2.4. Ada Development<a name="uxas-ada" />

OpenUxAS includes several services that have been developed using Ada and SPARK.
To compile these services, you need an Ada compiler.
To rerun the proofs for these services, you need the SPARK tools.

### 2.4.1. Bootstrapping with GNAT Community Edition

GNAT Community Edition provides both a suitable Ada compiler and the SPARK tools.
You can bootstrap with the GNAT Community Edition like this:

    ~$ curl -L https://github.com/afrl-rq/OpenUxAS-bootstrap/raw/develop/install/bootstrap | ADA=1 bash

To use the build system in `bootstrap`, you need to configure your environment.
You can do so like this:

    ~$ eval "$( cd ~/bootstrap && install/install-gnat --printenv )"
    ~$ eval "$( cd ~/bootstrap && install/install-anod-venv --printenv )"

If you do not wish to enter these commands each time you want to build OpenUxAS, you can add them to your profile.

### 2.4.2. Bootstrapping with an Existing GNAT Pro and SPARK Pro Install

If you have GNAT Pro and SPARK Pro, you can use them rather than GNAT Community Edition.
Follow the instructions [above](#uxas-developers) to bootstrap as normal.
As long as your environment is properly configured to use GNAT Pro and SPARK Pro, anod will find and use them to build Ada and prove SPARK.

### 2.4.3. Building the Ada Code

Now, you can build the Ada services for OpenUxAS like this:

    ~/bootstrap$ ./anod build uxas-ada

You configure your environment to run the Ada services like this:

    ~/bootstrap$ eval "$( ./anod printenv uxas-ada )"

### 2.4.4. Running the Ada Examples

Once you have built the Ada services for OpenUxAS, as well as the C++ OpenUxAS and OpenAMASE, you can run the Ada examples:

    ~/bootstrap$ ./run-example 02a_Ada_WaterwaySearch

### 2.4.5. Ada Development Using GNAT Studio

If you want to use GNAT Studio to develop OpenUxAS Ada code, you will need to export the build environment configured by anod:

    ~/bootstrap$ eval "$( ./anod printenv uxas-ada --build-env )"

This makes the dependencies that are built by anod available in GNAT Studio, so that you can rebuild your Ada sources using the IDE.

Once you are finished making modifications to the OpenUxAS Ada code and before you push your changes, you should re-run the anod build.
Essentially, this will repeat on your local machine the same build that will be performed during continuous integration, ensuring that your build is consistent and reproducible.


# 3. Detailed Discussion<a name="discussion" />

This section of the README contained more detailed discussion of this repository and the tools it provides.

## 3.1 Organization of this Repository<a name="organization" />

This repository contains the following:

* anod - the top-level script providing build automation for OpenUxAS
* CONTRIBUTING.md - instructions for contributors to this repository
* install - scripts (and supporting code) to support installation of this repository
* lib - support for the anod top-level script
* README.md - this file
* run-example - the top-level script for running OpenUxAS examples
* specs - specifications of components that anod can build

## 3.2 Install Support<a name="install-support" />

To simplify the installation of the dependencies needed to run anod, we provide a top-level install script in the `install` directory.
Assuming you have cloned this repository to `~/bootstrap`, you would run the install script like this:

    ~/bootstrap$ install/install

The script automates the installation of GNAT Community Edition, which is needed to build the OpenUxAS Ada services, and the python virtual environment that is needed to run anod.
When run as above, the script is interactive, so you can choose which components to install.
You can always rerun the script; it will not make changes unless needed (or unless you specify `--force`).

The script offers extensive configuration options, which you can see with `--help`.

After running, the script prints a summary of what it did.
This summary includes the environment configuration needed to run anod.

To see the summary again without making any changes, you can run:

    ~/bootstrap$ install/install -ny

The `-n` option instructs the installer to perform a dry run; no changes are made.
The `-y` option instructs the installer to run in automatic mode. 

## 3.3. The Anod Build System<a name="anod" />

The build automation for OpenUxAS is based on anod.

### 3.3.1. What is Anod?<a name="what-is-anod" />

Anod is a component of [e3](https://github.com/AdaCore/e3-core), a Python-based build framework that is built and used by AdaCore to provide reproducible builds of AdaCore's professionally supported software.
AdaCore's business is the development and support of tools for high-assurance software.
As such, AdaCore requires full traceability and reproducibility of builds over long periods of time.
The tools built on top of e3 provide this capability.

E3 and anod are open-source software.

### 3.3.2. Why Anod?<a name="why-anod" />

Basing the OpenUxAS build automation on anod allows OpenUxAS builds to benefit from similar stability, traceability, and reproducibility to AdaCore's professional tools. 
Given the scope of the OpenUxAS project and the number of collaborators, this is a significant benefit.

Anod uses lightweight specifications that describe how to build and test software components.
Each anod spec describes:

  * how to create source packages from repositories;
  * the dependencies of the component; and
  * how to build the component.

Importantly, anod delegates the actual build of each component to that component's native build system.
This greatly simplifies the process of updating components or including new components in the build, as component build files do not have to be rewritten.

Finally, anod encapsulates most dependencies of the build environment — especially libraries.
This ensures that developers on different platforms can reproduce similar builds.
This also means that the resulting executable is static and complete, which can be redistributed easily on similar platforms.

### 3.3.3. Understanding Anod<a name="anod-understanding" />

The aim of this section is not to provide comprehensive information about anod, but to provide sufficient information to clarify some of the details about how anod organizes artifacts.

#### 3.3.3.1. Anod Specs<a name="anod-specs" />

Anod describes software components using lightweight specifications.
Anod specs are contained in the `specs` directory in this repository.
Each anod spec is written in Python and inherits from the spec class that is defined in e3.

Good examples of specs include `lmcpgen.anod` and `uxas.anod`, which provide examples for many common elements of specs.

Of particular note is the `source_pkg_build` method, which defines how anod should fetch the source for the component.
The `checkout` argument to `SourceBuilder` is used to identify the key to the repository that holds the source.
This key must match an entry in `repositories.yaml`, which is contained in the `specs/config` directory.

#### 3.3.3.2. Anod Repositories<a name="anod-repositories" />

As noted [above](#anod-specs), each spec identifies the repository that holds its source by way of a key that must match an entry in the `repositories.yaml`, which is contained in the `specs/config` directory.
This configuration file lists all of the repositories for components that may be built.

For each repository, the version-control system is identified, a URL to the repository is given, and a specific revision is identified.
For git, the most common version-control system, the revision is a refspec and may be:

- a specific branch, such as "develop"
- a tag, such as "v2.0.0"
- a specific commit, identified directly

#### 3.3.3.4. The Anod Sandbox<a name="anod-sandbox" />

Anod does all of its work in a *sandbox*, a directory structure that is assumed to be under anod's control and that has minimal dependencies.
The anod sandbox is a critical component of anod's ability to provide reproducible builds. 
Anod therefore assumes that it has complete control over the sandbox.
In general, anod will freely delete and recreate any element of the sandbox during the build process.

The two most important elements of the sandbox are the `vcs` and the platform directory, which, on 64-bit Linux is `x86_64-linux`.

The `vcs` directory contains anod's managed clones of version-control repositories.
You should not make changes to the repositories that are kept under `vcs`.
If you do, anod will always attempt to stash those changes during the build, so that it can check out the specific version of the repository that is listed in `repositories.yaml` (see [above](#anod-repositories)).

The platform directory (e.g., `x86_64-linux`) contains the artifact directories for each project.
For example, after a successful anod build of OpenUxAS with `anod-build uxas`, the platform directory will contain `uxas-release`.
This is the project directory for OpenUxAS.

Inside each project directory is a set of nine artifact directories:

  - binary
  - build
  - install
  - log
  - pkg
  - results
  - src
  - test
  - tmp

Not all of these directories are used at all times for all projects.
We will focus on three of these directories: `src`, `build`, and `install`.

  - The `src` directory contains a copy of the repository for the project.
    Anod makes this copy because some build systems may modify the sources during the build.
    Since anod's goal is reproducibility, copying the repository contents at the start of each build is an important step.

  - The `build` directory generally contains build outputs for the project, but this depends on the configuration of the project's native build system.
    For OpenUxAS, the `build` directory contains the object files and the final binary.

  - The `install` directory generally contains the final result of the build in a location that is representative of an install.
    For OpenUxAS, the `install` directory contains `bin/uxas`, which is the OpenUxAS binary.

> ***Important***
> 
> Anod will always remove and recreate all of the directories for a project if there are any changes to the project's repository.
> This means that you should *never* modify the contents of the `src` directory for a given project.

### 3.3.4. Using Anod during OpenUxAS Development<a name="anod-development" />

If you wish to develop OpenUxAS, then you *must* create your own clone of the OpenUxAS repository, rather than relying on the clone that anod keeps in `sbc/vcs`.
This is because, as noted [above](#and-sandbox), anod will stash any changes you make to its clone of a repository during the build process.

Once you have created your own clone, you should update `specs/config/repositories.yaml` to tell anod where to find your clone.
Using OpenUxAS as an example, you would make the following changes:

    openuxas:
        vcs: external
        url: /path/to/your/clone
        revision: none

With these changes, anod will no longer attempt to fetch a specific revision of OpenUxAS from git.
Instead, anod will copy your local clone at the beginning of the build process.

Before starting development, you should use anod to build OpenUxAS.
This will ensure that all dependencies have been built and are ready for use.
Then, you export the build environment by running `anod printenv`, like this:

    ~/bootstrap$ eval "$( ./anod printenv uxas --build-env )"

Now, as you do your development work, you won't need to use anod anymore.
Instead, you should use the local build system to build your changes.
For OpenUxAS, you would use `make all`.

You should only use anod when you are ready to test the build, prior to committing your changes.
You can think of anod as standing in for the continuous-integration process, on your local machine.
Anod will then copy your sources, including all changes, and rebuild OpenUxAS within the context of its sandbox.

You can force a full rebuild by passing `--force` to anod, like this:

    ~/bootstrap$ ./anod build uxas --force

## 3.4. Division of Labor: OpenUxAS and OpenUxAS-bootstrap<a name="division" />

OpenUxAS-bootstrap (this repository) is intended to provide build automation support for OpenUxAS and to make it easier to get started with OpenUxAS development.
As such, most changes to OpenUxAS should be made in the OpenUxAS repository and should not impact this repository.

However, if a new dependency is added to OpenUxAS, the new dependency will need to be added to this repository.

### 3.4.1. Adding a New Dependency to OpenUxAS<a name="new-dependency" />

Whenever a new dependency is added to OpenUxAS, that dependency should be added to OpenUxAS-bootstrap as well.
In particular, the following should be done:

  - a new spec should be added to `specs` to describe the new dependency (see [above](#anod-specs))
  - an entry in `specs/config/repositories.yaml` should be added for the new dependency (see [above](#anod-repositories))

If the new dependency is on the "develop" branch of OpenUxAS, the dependency should be added to the "develop" branch of OpenUxAS-bootstrap.

If the new dependency is on another branch of OpenUxAS, the dependency should be added to a new branch of OpenUxAS-bootstrap of the same name.
For example, in OpenUxAS, the "DAIDALUS_integration" branch depends upon the NASA well-clear library. 
A branch has thus been added to OpenUxAS-bootstrap that provides an anod spec for the well-clear library and that lists the NASA well-clear repository in `repositories.yaml`. 
These two branches are tested and deployed together.

# 4. Troubleshooting<a name="troubleshooting" />

If at any point you get a message that an executable, library, or header file is not defined and you believe that the missing file should have been built or installed by anod, this probably means that some part of the anod-managed environment has not been exported to your shell's environment.
For example, if you get a message that `uxas` is not a recognized command, try:

    ~/bootstrap$ eval "$( ./anod printenv uxas )"

Or, if `ant` is not a recognized command, try:

    ~/bootstrap$ eval "$( ./anod printenv ant )"

Similarly, if a library or header file is not found during the build of OpenUxAS, try:

    ~/bootstrap$ eval "$( ./anod printenv uxas --build-env )"

## 4.1. Verbosity<a name="verbosity" />

Anod and most of the other scripts provided in this repository offer more verbose logging.
In general, passing additional `-v` flags will make logging more verbose.
For example, for the most verbose logging, you can pass `-vv` to most scripts.
