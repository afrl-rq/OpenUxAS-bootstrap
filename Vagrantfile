# -*- mode: ruby -*-
# vi: set ft=ruby :

# To use:
# `vagrant up uxas-contained` and `vagrant ssh uxas-contained`

# To more easily manage shared provisioning between the machine configurations,
# I'm defining the bits of provisioning here in constants.
#
# There are two machines:
# 1. uxas-shared - this machine maps local directories containing to satisfy
#                  various dependencies. It's suitable for development and to
#                  accelerate testing of instances.
#
# 2. uxas-contained - this machine redownloads everything every time and maps
#                     no local directories. It's suitable for one-shot use and
#                     to test the build on a fresh machine.

# Basic software install via apt (and pip)
PROVISIONING_APT = <<-SHELL
  # ---------
  # apt setup
  echo " "
  echo "# ------------------------------------------------------ #"
  echo "# Apt Update & Upgrade "
  apt-get update
  apt-get -y upgrade
  echo " "
  echo "# End Apt Update & Upgrade"
  echo "# ------------------------------------------------------ #"

  echo " "
  echo "# ------------------------------------------------------ #"
  echo "# apt install -y make cmake, pkg-config, uuid-dev, "
  echo "#                python3, python3-pip, python3-venv, "
  echo "#                libyaml-dev fontconfig libx11-xcb1"
  apt-get install -y make cmake pkg-config uuid-dev python3 python3-pip python3-venv libyaml-dev fontconfig libx11-xcb1
  echo " "
  echo "# end apt install"
  echo "# ------------------------------------------------------ #"
SHELL

# Cloning repos
PROVISIONING_REPOS = <<-SHELL
  # -----------
  # repos setup

  # Run as the vagrant user, so that it'll be easier to mess with
  # these, later.

  # The dependencies: the gnat community install script
  cd ~vagrant
  sudo -u vagrant mkdir -p dependencies

  echo " "
  echo "# ------------------------------------------------------ #"
  echo "# git gnat-community-install-script "
  cd ~vagrant/dependencies
  sudo -Hu vagrant git clone https://github.com/AdaCore/gnat_community_install_script
  echo " "
  echo "# end git gnat-community-install-script "
  echo "# ------------------------------------------------------ #"
SHELL

# Downloading GNAT community
PROVISIONING_GNAT_DOWNLOAD = <<-SHELL
  # Run as the vagrant user, so that it'll be easier to mess with
  # these, later.
  cd ~vagrant
  sudo -u vagrant mkdir -p software/gnat_community
  cd software/gnat_community

  # download the installer
  echo " "
  echo "# ------------------------------------------------------ #"
  echo "# downloading gnat community "
  echo "#"
  echo "# wget the install file"
  sudo -Hu vagrant wget -nv -O gnat-bin https://community.download.adacore.com/v1/0cd3e2a668332613b522d9612ffa27ef3eb0815b?filename=gnat-community-2019-20190517-x86_64-linux-bin
  echo " "
  echo "# end downloading gnat community "
  echo "# ------------------------------------------------------ #"
SHELL

# Installing GNAT community
PROVISIONING_DEPENDENCIES = <<-SHELL
  # ----------------------
  # gnat community install
  #
  echo " "
  echo "# ------------------------------------------------------ #"
  echo "# install gnat community "
  echo "#"

  # run the install script
  echo "# run the install script"
  cd /home/vagrant/dependencies/gnat_community_install_script
  sh install_package.sh /home/vagrant/software/gnat_community/gnat-bin /opt/gnat

  # set the paths - note that we have to move to the vagrant user dir
  # because provisioning runs as root
  echo "# set the paths"
  cd ~vagrant
  sudo -Hu vagrant echo "PATH=\\$PATH:/opt/gnat/bin" >> ~vagrant/.bashrc
  echo " "
  echo "# end gnat community "
  echo "# ------------------------------------------------------ #"
SHELL

# Running install_ and setup_env
PROVISIONING_ENV = <<-SHELL
  echo " "
  echo "# ------------------------------------------------------ #"
  echo "# install env"
  cd ~vagrant/bootstrap

  # run as vagrant
  sudo -Hu vagrant python3 install_env
  sudo -Hu vagrant echo "PATH=/home/vagrant/bootstrap/vpython/bin:\\$PATH" >> ~vagrant/.bashrc

  echo " "
  echo "# end install env"
  echo "# ------------------------------------------------------ #"
SHELL

PROVISIONING_LINKS = <<-SHELL
  echo " "
  echo "# ------------------------------------------------------ #"
  echo "# creating links"
  cd ~vagrant

  sudo -u vagrant mkdir -p uxas

  cd uxas

  # run as vagrant
  sudo -u vagrant ln -s ~vagrant/bootstrap/sbx/vcs/openuxas OpenUxAS
  sudo -u vagrant ln -s ~vagrant/bootstrap/sbx/vcs/amase OpenAMASE
  sudo -u vagrant ln -s ~vagrant/bootstrap/sbx/vcs/lmcpgen LmcpGen

  echo " "
  echo "# end creating links"
  echo "# ------------------------------------------------------ #"
SHELL

MOTD_MESSAGE = <<-SHELL
-------------------------------------------------------------------------------
Ubuntu 18.04 OpenUxAS Development Vagrant Box
-------------------------------------------------------------------------------

This machine has been preconfigured with all dependencies required to build and
run OpenUxAS. To get started, run the following command:

  cd ~vagrant/bootstrap && python3 anod-build uxas

That will build the C++ version of OpenUxAS. Additional instructions can be 
found in the README in ~vagrant/bootstrap/README.md (or more easily read on
github at https://github.com/AdaCore/OpenUxAS-bootstrap).

After uxas is built for the first time, the links under ~vagrant/uxas can be
used to quickly navigate to the OpenUxAS, OpenAMASE, or LMCPgen repositories.


SHELL

PROVISIONING_MOTD = <<-SHELL
  echo "#{MOTD_MESSAGE}" > /etc/motd
SHELL

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # Base for the virtual machine
  config.vm.box = "ubuntu/bionic64"

  # Specific configuration for Virtual Box
  config.vm.provider "virtualbox" do |vb|
    # Display the VirtualBox GUI when booting the machine
    vb.gui = true

    # Customize the amount of memory on the VM. This amount seems to be
    # required to complete the build.
    vb.memory = "4096"

    # From Rob's Vagrantfile
    vb.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]
  end

  # Common provisioning
  config.vm.provision "shell", inline: PROVISIONING_APT

  config.vm.synced_folder ".", "/home/vagrant/bootstrap"

  # This VM is self-contained: it doesn't need and doesn't map any local files.
  config.vm.define "uxas" do |contained|
    contained.vm.provision "shell", inline: PROVISIONING_REPOS + 
                                            PROVISIONING_GNAT_DOWNLOAD + 
                                            PROVISIONING_DEPENDENCIES +
                                            PROVISIONING_ENV +
                                            PROVISIONING_LINKS +
                                            PROVISIONING_MOTD
  end

  # This VM is a kind of compromise: it redownloads everything *except* for
  # GNAT community (which takes the longest)
  config.vm.define "uxas-almost" do |almost|
    almost.vm.synced_folder "../software/gnat_community", "/home/vagrant/software/gnat_community"

    almost.vm.provision "shell", inline: PROVISIONING_REPOS +
                                         PROVISIONING_DEPENDENCIES +
                                         PROVISIONING_ENV +
                                         PROVISIONING_LINKS +
                                         PROVISIONING_MOTD
  end
end
