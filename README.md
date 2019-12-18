OpenUxAS-bootstrap
==================

This respository is designed to get you up and running with [OpenUxAS](https://github.com/afrl-rq/OpenUxAS) development as quickly and efficiently as possible.
This repository configures your environment, fetches OpenUxAS and its related repositories [OpenAMASE]() and [LmcpGen](), and provides a fully automated build system.

There are two primary ways to use this repository, in order of simplicity:

1. using [Vagrant](https://www.vagrantup.com/) to create a new, fully configured virtual machine
2. configuring an existing machine

We'll talk about Vagrant first.


Vagrant-Based Setup
===================

[Vagrant](https://www.vagrantup.com/) is a set of tools that create, provision, and control virtual machines.
The great thing about Vagrant is virtual machines can be described declaratively.
Practically speaking, this means that virtual-machine configurations can be easily placed under version control.
This repository contains a Vagrantfile that will create a virtual machine based on Ubuntu 18.04 LTS and provision it with all necessary dependencies so that you can immediately build and run OpenUxAS.
When you're done playing with OpenUxAS, you can use Vagrant to destroy the virtual machine, freeing up disk space.

To get started with Vagrant, you will first need to:

1. install Vagrant, after downloading it from https://www.vagrantup.com/downloads.html
2. install a virtual machine provider, preferably VirtualBox, which is available from https://www.virtualbox.org/wiki/Download_Old_Builds_6_0.
   ***WARNING***: Vagrant 2.2.6, the current version of Vagrant, does not support VirtualBox 6.1, the newest version of VirtualBox.
   Please make sure to download and install version 6.0 from https://www.virtualbox.org/wiki/Download_Old_Builds_6_0 and not from www.virtualbox.org/wiki/Downloads.

> ***Shortcut***: Once this is done, if you want a graphical machine that you can keep using after it is configured, you can mostly forget about the rest of this README, open a terminal (on *NIX machines) or a command prompt (on Windows), navigate to the directory where you've cloned this repository, and run `./build-vagrant-gui`.
> This will configure a graphical machine and run all of the builds related to OpenUxAS.
> After the script completes, you can log in (see "Vagrant Username and Password", below) and immediately run examples (see "Running Examples", below).

Once Vagrant is installed, open a terminal (on *NIX machines) or a command prompt (on Windows), navigate to the directory where you've cloned this repository, and run the command (or see "GUI Machine", below, if you want a machine with a GUI):

    vagrant up uxas

Vagrant will download the base image for Ubuntu 18.04 LTS, install needed software, and configure the environment for building OpenUxAS.

Once the machine has been created, you can interact with it by running the command:

    vagrant ssh uxas

This will log you into the machine as the user "vagrant".
You can now navigate into the `bootstrap` directory and run the build, like this:

    cd ~vagrant/bootstrap && python3 anod-build uxas

That will fetch remaining dependencies and build the C++ version of OpenUxAS. 

Once the build is complete, you will be able to get to the OpenUxAS, OpenAMASE and LmcpGen repos by looking under the `uxas` directory at the top of the home directory.

Additional build and advanced configuration options are discussed below.

*Note*: if you want to build the machine and then run builds in one command, you can:

    vagrant up uxas && vagrant ssh uxas -c "cd ~vagrant/bootstrap && python3 anod-build uxas"

Additional build commands can be chained to this, within the quotes.

Vagrant Username and Password
-----------------------------

As is common for Vagrant machines, the username is "vagrant" and the password is "vagrant".

Other Vagrant Commands
----------------------

> ***Shortcut***: If you configured a graphical machine, you can choose to ignore Vagrant and manage the machine through VirtualBox's user interface.
> In that case, you can ignore the commands below.
> **Note**: If you do this, the Vagrant-provided shared folder `bootstrap-src-shared` will not be available; this is not terribly important as it mostly exists to enable initial provisioning of the machine.

You can suspend your Vagrant machine, saving all state, with:

    vagrant suspend uxas

Likewise, you can shut it down with:

    vagrant halt uxas

Once shut down, you start the machine again with:

    vagrant up uxas

Finally, if you want to restart, **do not** restart from within the machine, or shared folders will *not* be mapped.
Instead, use:

    vagrant reload uxas

When you are done with your Vagrant machine, you can destroy it with:

    vagrant destroy uxas


Vagrant GUI Machine
-------------------

If you plan to do development work on OpenUxAS using Vagrant, you may prefer to have a machine with a GUI.
A spec is provided that adds Ubunutu desktop and provides a graphical login.
You can build this machine with:

    vagrant up uxas-gui

You can also build this machine using the supplied script:

    ./build-vagrant-gui

which will run all of the OpenUxAS builds automatically.

This machine takes significantly longer to build, downloads about twice as much data, and requires twice as much RAM as the non-GUI machine.

All of the commands listed above will work for this machine; you replace `uxas` with `uxas-gui`.
So to log in from a console:

    vagrant ssh uxas-gui

You can also log in via the graphical interface, which VirtualBox will show automatically.


Running Examples
================

OpenUxAS includes a large number of examples, which you can find in `~uxas/OpenUxAS/examples`.
To make running these examples much more convient, this repository provides a Python script `run-example.py` that you can use to run examples.
After you have built OpenUxAS and OpenAMASE, switch to the `bootstrap` directory and run an example like this:

    cd ~bootstrap && python3 run-example.py 02_Example_WaterwaySearch

The `run-example.py` script provides built-in help, which you can access with

    python3 run-example.py -h


Configuring an Existing Machine
===============================

If you don't wish to use a virtual machine, you can use this repository to help you configure an existing machine to build OpenUxAS.

Common prerequisites
--------------------

You need to ensure that you have:

* Git
* Cmake
* C++ compiler
* pkg-config
* libuuid (uuid-dev package on ubuntu or debian)
* A Python 3.x with pip and venv
* Ada compiler (to build the Ada demo)

*Note: the build system will pick the compiler on the path.*
If you change the compiler in the path, a full rebuild will be triggered.

Bootstrapping your environment
------------------------------

After installing the prerequisites, in order to bootstrap your environment you need to run the following command:

    ./install_env

*Note: if the default python in your path is a python 2.x you may have to run*:

    python3 install_env

This step only needs to be done once. It will do the following:

* Check your environment for the prerequisites
* Create, under the 'vpython' subdirectory, a python 3.x virtual environment with the necessary modules to launch anod-build command (see next section).

If you do not wish to update your path permanently, you can run

    . ./setup_env

which configures your path for your current terminal session.

Building the project and its dependencies
-----------------------------------------

To build, run:

    ./anod-build <target>

where target can be:

* uxas: to build the C++ uxas executable
* uxas-ada: to build the Ada demo
* amase: to build the simulator

Other targets are available to build some of the dependencies:

* lmcpgen: to build lmcpgen
* uxas-lmcp: will generate sources and build them for a given language.
    To select the language (ada, cpp, java, py), add the switch --qualifier=lang=<LANG>


Additional Details
==================

Directory structure
-------------------

| File                            | Description
| ------------------------------- | -----------
|./README.md                      | This file.
|./anod-build                     | This the tool to build any spec present in the specs subdirectory. You can use the `--help` switch to see available options
|./install_env                    | Creates the Python 3.x environment necessary to launch `anod-build`
|./setup_env                      | Source that script to put the Python environment in your PATH
|./specs/*.anod                   | The build specifications for the different component of UxAS
|./specs/config/repositories.yaml | Configuration file containing the list of repositories used
|./specs/patches/*.patch          | Contains some local patches for some corresponding anod specs
|./sbx                            | The sandbox in which everything is build. You will find a directory `<platform>/<name>` for each component built. These directories are called 'build space's (generated)
|./vpython                        | The python environment to run anod-build (generated)

Each build space usually has the following subdirectories:

| Directory | Description
| --------- | -----------
| ./src     | Location in which sources are installed
| ./build   | Directory in which the build is performed
| ./install | Directory in which a component is installed

Repositories Used
-----------------

The list of repositories used is in specs/config/repositories.yaml. The file is configured
so that all repositories are automaticly cloned. In case you want to manage a given checkout
you can change the repositories.yaml file. For example if you want to control the lmcpgen
sources, replace:

    lmcpgen:
        vcs: git
        url: https://github.com/AdaCore/LmcpGen.git
        revision: ada

By:

    lmcpgen:
        vcs: external
        url: /some_absolute_dir_containing_your_checkout
        revision: None

In that case the build script will pick the content of your directory instead of doing an
automatic checkout. In that case the script does not try to do updates.

Force rebuild
-------------

If you pass --force to uxas-build command, the current state will be ignored and
everything rebuilt from scratch.
