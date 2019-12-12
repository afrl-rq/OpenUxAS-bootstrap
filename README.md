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

1. Install Vagrant, after downloading it from https://www.vagrantup.com/downloads.html
2. Install a virtual machine provider, preferably Virtual Box, which is available from https://www.virtualbox.org/wiki/Downloads

***IMPORTANT***: if you are on Windows then you **must** start your console session as an Administrator.

Then, open a terminal (on *NIX machines) or a command prompt (on Windows), navigate to the directory where you've cloned this repository, and run the command:

    vagrant up uxas

Vagrant will download the base image for Ubuntu 18.04 LTS, install needed software, and configure the environment for building OpenUxAS.

Once the machine has been created, you can interact with it by running the command:

    vagrant ssh uxas

This will log you into the machine as the user "vagrant".
You can now navigate into the `bootstrap` directory and run the build, like this:

    cd ~vagrant/bootstrap && python3 anod-build uxas

That will fetch remaining dependencies and build the C++ version of OpenUxAS. 

Once the build is complete, you will be able to get to the OpenUxAS, OpenAMASE and LmcpGen repos by looking under `uxas` directory at the top of the home directory.

Additional build and advanced configuration options are discussed below.


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
* Ada compiler (to build ada demo)

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
* Create in 'vpython' subdirectory a python 3.x virtualenv with the necessary modules
  to launch anod-build command (see next section).

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
|./README.txt                     | This file.
|./anod-build                     | This the tool to build any spec present in the specs subdirectory. You can use the `--help` switch to see available options
|./install_env                    |  Creates the Python 3.x environment necessary to launch `anod-build`
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
        url: git@github.com:AdaCore/LmcpGen.git
        revision: ada

By:

   
    lmcpgen:
        vcs: external
        url: /some_absolute_dir_containing_your_checkout
        revision: None

In that case the build script will pick the content of your directory instead of doing an
automatic checkout. In that case the script do not try to do updates.

Force rebuild
-------------

If you pass --force to uxas-build command, current state will be ignore and
everything rebuilt from scratch
