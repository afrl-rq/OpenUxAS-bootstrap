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
  DEBIAN_FRONTEND=noninteractive apt-get update
  DEBIAN_FRONTEND=noninteractive apt-get -y upgrade
  echo " "
  echo "# End Apt Update & Upgrade"
  echo "# ------------------------------------------------------ #"

  echo " "
  echo "# ------------------------------------------------------ #"
  echo "# apt install -y make cmake, pkg-config, uuid-dev, "
  echo "#                python3, python3-pip, python3-venv, "
  echo "#                libyaml-dev fontconfig libx11-xcb1"
  DEBIAN_FRONTEND=noninteractive apt-get install -y make cmake pkg-config uuid-dev python3 python3-pip python3-venv libyaml-dev fontconfig libx11-xcb1
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
  cd /home/vagrant
  sudo -u vagrant mkdir -p dependencies

  echo " "
  echo "# ------------------------------------------------------ #"
  echo "# git gnat-community-install-script "
  cd /home/vagrant/dependencies

  echo "# cloning gnat_community_install_script..."
  sudo -Hu vagrant git clone --quiet https://github.com/AdaCore/gnat_community_install_script
  echo " "
  echo "# end git gnat-community-install-script "
  echo "# ------------------------------------------------------ #"
SHELL

# Downloading GNAT community
PROVISIONING_GNAT_DOWNLOAD = <<-SHELL
  # Run as the vagrant user, so that it'll be easier to mess with
  # these, later.
  cd /home/vagrant
  sudo -u vagrant mkdir -p software/gnat_community
  cd /home/vagrant/software/gnat_community

  if [ ! -f gnat-bin ]; then
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
  fi
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
  
  # Running this as vagrant removes a spurious error message
  sudo -EHu vagrant sh install_package.sh /home/vagrant/software/gnat_community/gnat-bin /opt/gnat

  # set the paths - note that we have to move to the vagrant user dir
  # because provisioning runs as root
  echo "# set the paths"
  cd ~vagrant
  sudo -Hu vagrant echo "PATH=/opt/gnat/bin:\\$PATH" >> ~vagrant/.profile
  echo " "
  echo "# end install gnat community "
  echo "# ------------------------------------------------------ #"
SHELL

# Currently, we have to patch the formal containers in GNAT community. The
# changes here are already at the FSF and will be integrated into the next
# GCC release.
PROVISIONING_PATCH_COMMUNITY = <<-SHELL
  echo " "
  echo "# ------------------------------------------------------ #"
  echo "# patch gnat community "
  echo "#"

  cd /opt/gnat
  echo "Patching using ~vagrant/bootstrap-src-shared/community.patch"
  patch -p0 < /home/vagrant/bootstrap-src-shared/community.patch

  echo " "
  echo "# end patch gnat community "
  echo "# ------------------------------------------------------ #"
SHELL

# Running install_ and setup_env
PROVISIONING_ENV = <<-SHELL
  echo " "
  echo "# ------------------------------------------------------ #"
  echo "# install env"
  
  sudo -Hu vagrant cp -R /home/vagrant/bootstrap-src-shared /home/vagrant/bootstrap
  sudo rm -rf /home/vagrant/bootstrap/.git

  cd /home/vagrant/bootstrap

  # run as vagrant
  sudo -Hu vagrant python3 install_env
  sudo -Hu vagrant echo "PATH=/home/vagrant/bootstrap/vpython/bin:\\$PATH" >> ~vagrant/.profile

  # This is needed for testing support
  sudo -Hu vagrant /home/vagrant/bootstrap/vpython/bin/pip install zmq

  # After the build, java will be in a nonstandard place, so set the path for it:
  sudo -Hu vagrant echo "PATH=\\$PATH:/home/vagrant/bootstrap/sbx/x86_64-linux/java/install/bin" >> ~vagrant/.profile

  echo " "
  echo "# end install env"
  echo "# ------------------------------------------------------ #"
SHELL

# Set some symlinks to make it easier to get to the UxAS-related repos
PROVISIONING_LINKS = <<-SHELL
  echo " "
  echo "# ------------------------------------------------------ #"
  echo "# creating links"
  cd /home/vagrant

  sudo -u vagrant mkdir -p uxas

  cd uxas

  # run as vagrant
  sudo -u vagrant ln -fs ~vagrant/bootstrap/sbx/vcs/openuxas OpenUxAS
  sudo -u vagrant ln -fs ~vagrant/bootstrap/sbx/vcs/amase OpenAMASE
  sudo -u vagrant ln -fs ~vagrant/bootstrap/sbx/vcs/lmcpgen LmcpGen

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

  cd ~vagrant/bootstrap && ./anod-build uxas

That will build the C++ version of OpenUxAS. Additional instructions can be 
found in the README in ~vagrant/bootstrap/README.md (or more easily read on
github at https://github.com/AdaCore/OpenUxAS-bootstrap).

After uxas is built for the first time, the links under ~vagrant/uxas can be
used to quickly navigate to the OpenUxAS, OpenAMASE, or LMCPgen repositories.


SHELL

# Set the above MOTD so that the user can have some guidance upon login.
PROVISIONING_MOTD = <<-SHELL
  echo "#{MOTD_MESSAGE}" > /etc/motd
SHELL

PROVISIONING_GUI = <<-SHELL
  echo " "
  echo "# ------------------------------------------------------ #"
  echo "# apt-get install ubuntu-desktop "
  DEBIAN_FRONTEND=noninteractive apt-get install -y ubuntu-desktop virtualbox-guest-dkms
  echo "# end apt-get install ubuntu-desktop "
  echo "# ------------------------------------------------------ #"

  echo " "
  echo "# ------------------------------------------------------ #"
  echo "# starting the display server"
  service gdm3 start
  echo "# done"
  echo "# ------------------------------------------------------ #"
SHELL

# All machines need this provisioning
COMMON_PROVISIONING = PROVISIONING_REPOS + 
                      PROVISIONING_GNAT_DOWNLOAD +
                      PROVISIONING_DEPENDENCIES +
                      PROVISIONING_ENV +
                      PROVISIONING_PATCH_COMMUNITY +
                      PROVISIONING_LINKS +
                      PROVISIONING_MOTD

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (Vagrant supports older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # Base for the virtual machine
  config.vm.box = "ubuntu/bionic64"
  
  # Increase the disk size. Was 10GB but building uxas, amase, and uxas-ada fills it.
  # (Requires installing a plugin: "vagrant plugin install vagrant-disksize".)
  # 50GB is plenty for builds and development.
  config.disksize.size = '50GB'

  # Specific configuration for Virtual Box
  config.vm.provider "virtualbox" do |vb|
    # Controls whether or not the VirtualBox GUI is displayed when booting 
    # the machine
    vb.gui = false

    # Customize the amount of memory on the VM. This amount seems to be
    # required to complete the build.
    vb.memory = "4096"

    # From Rob's Vagrantfile
    vb.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]
  end

  # Always sync this repo.
  config.vm.synced_folder ".", "/home/vagrant/bootstrap-src-shared"

  # As a compromise, see if gnat community has already been downloaded. If so,
  # we map that into the VM, where we test for the installer before downloading
  # it again.
  if File.exist?("../software/gnat_community/gnat-bin") then
    config.vm.synced_folder "../software/gnat_community", "/home/vagrant/software/gnat_community"
  end

  # Common provisioning
  config.vm.provision "shell", inline: PROVISIONING_APT

  # This VM is self-contained: it doesn't need and doesn't map any local files.
  config.vm.define "uxas" do |uxas|
    uxas.vm.provision "shell", inline: COMMON_PROVISIONING
  end

  # This VM is self-contained: it doesn't need and doesn't map any local files.
  config.vm.define "uxas-gui" do |uxas_gui|
    # Specific configuration for Virtual Box
    uxas_gui.vm.provider "virtualbox" do |vb_gui|
      # Controls whether or not the VirtualBox GUI is displayed when booting 
      # the machine
      vb_gui.gui = true

      # GUI machine needs more RAM.
      vb_gui.memory = "8192"

      # Give the VM a reasonable amount of VRAM.
      vb_gui.customize ["modifyvm", :id, "--vram", "128"]
      vb_gui.customize ["modifyvm", :id, "--clipboard", "bidirectional"]

    end

    uxas_gui.vm.provision "shell", inline: COMMON_PROVISIONING
    uxas_gui.vm.provision "shell", inline: PROVISIONING_GUI
  end
end
