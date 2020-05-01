# -*- mode: ruby -*-
# vi: set ft=ruby :

# See README.md, in the same directory as this Vagrantfile.

# This block is loaded into the shell before any other commands.
LOG_REPORT_FUNCTION = <<-SHELL
  touch /home/vagrant/log.txt
  chown vagrant:vagrant /home/vagrant/log.txt

  log_report() {
    if [ $1 != "echo" ]; then
      echo $@ >> /home/vagrant/log.txt
    fi

    $@ >> /home/vagrant/log.txt 2>&1

    RET=$?

    if [ $RET -ne 0 ]; then
        echo "[Error]   $@"
    else
        case $1 in
            echo|cd) ;;
            *) echo "[Success] $@" ;;
        esac
    fi

    return $RET
  }

  export DEBIAN_FRONTEND=noninteractive
SHELL

# Write an entry for the log that indicates the date.
PROVISIONING_DATE = <<-SHELL
  echo "# ------------------------------------------------------ #"
  echo "# Starting provisioning at `date`"
  echo "# ------------------------------------------------------ #"
SHELL

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
  echo "# apt install -y make cmake pkg-config uuid-dev "
  echo "#                libyaml-dev fontconfig libx11-xcb1 "
  echo "#                python3 python3-dev "
  echo "#                python3-distutils python3-venv "
  echo "#                python3-pip"
  apt-get install -y make cmake pkg-config uuid-dev libyaml-dev fontconfig libx11-xcb1 libx11-6 python3 python3-dev python3-distutils python3-venv python3-pip

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

# Running install_ and setup_env
PROVISIONING_ENV = <<-SHELL
  echo " "
  echo "# ------------------------------------------------------ #"
  echo "# install env"
  
  sudo -Hu vagrant cp /home/vagrant/bootstrap-src-shared/refresh-bootstrap /home/vagrant
  sudo -Hu vagrant python3 refresh-bootstrap --no-prompt

  sudo -Hu vagrant echo "PATH=/home/vagrant/bootstrap/vpython/bin:\\$PATH" >> ~vagrant/.profile

  # After the build, java will be in a nonstandard place, so set the path for it:
  sudo -Hu vagrant echo "PATH=\\$PATH:/home/vagrant/bootstrap/sbx/x86_64-linux/java/src/bin" >> ~vagrant/.profile

  echo " "
  echo "# end install env"
  echo "# ------------------------------------------------------ #"
SHELL

MOTD_MESSAGE = <<-SHELL

-------------------------------------------------------------------------------
Ubuntu 20.04 OpenUxAS Development Vagrant Box
-------------------------------------------------------------------------------

This machine has been preconfigured with all dependencies required to build and
run OpenUxAS. To get started, run the following command:

  cd ~/bootstrap && ./anod-build uxas

That will build the C++ version of OpenUxAS. Additional instructions can be 
found in the README in ~/bootstrap/README.md (or more easily read on
github at https://github.com/AdaCore/OpenUxAS-bootstrap).

SHELL

# Set the above MOTD so that the user can have some guidance upon login.
PROVISIONING_MOTD = <<-SHELL
  echo "#{MOTD_MESSAGE}" > /etc/motd
SHELL

PROVISIONING_GUI = <<-SHELL
  echo " "
  echo "# ------------------------------------------------------ #"
  echo "# apt-get install ubuntu-desktop "
  apt-get install -y ubuntu-desktop libncurses5 virtualbox-guest-dkms
  echo "# end apt-get install ubuntu-desktop "
  echo "# ------------------------------------------------------ #"

  echo " "
  echo "# ------------------------------------------------------ #"
  echo "# starting the display server"
  service gdm3 start
  echo "# done"
  echo "# ------------------------------------------------------ #"
SHELL


# This function will take our provisioning fragments and turn them into a
# sequence of commands run through `log_report`.
#
# Each command must be on a single line, or this will not work. Comment and
# blank lines are skipped.
#
# Simple if statements are also skipped, but this is brittle and should be
# treated with caution.
#
# Commands that redirect their output to files are also skipped.
def build_logged_commands(commands)
  script = LOG_REPORT_FUNCTION
  script += "\n"

  script += commands.split("\n").
                     reject { |line| line if line.match(/^\s*#/) }.
                     reject { |line| line if line.match(/^\s*$/) }.
                     collect { |line|
                      if line.include?('>>') or
                         line.match(/^\s*if/) or
                         line.match(/^\s*fi/) 
                      then
                        line
                      else
                        'log_report ' + line.strip
                      end
                     }.join("\n")
end

# Initial provisioning
INIT_PROVISIONING = build_logged_commands(PROVISIONING_DATE +
                                          PROVISIONING_APT)

# All machines need this provisioning
COMMON_PROVISIONING = build_logged_commands(PROVISIONING_REPOS + 
                                            PROVISIONING_GNAT_DOWNLOAD +
                                            PROVISIONING_DEPENDENCIES +
                                            PROVISIONING_ENV) + "\n" +
                                            PROVISIONING_MOTD

# GUI machines need this provisioning
GUI_PROVISIONING = build_logged_commands(PROVISIONING_GUI)

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (Vagrant supports older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # Base for the virtual machine
  #
  # Using bento's build because the ubuntu-provided machine doesn't provide
  # build-in support for virtualbox.
  config.vm.box = "bento/ubuntu-20.04"
  
  if Vagrant.has_plugin?("vagrant-vbguest")
    config.vbguest.auto_update = false
  end

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
  COMMUNITY_FOLDER = "../software/gnat_community"
  if File.exist?(COMMUNITY_FOLDER) then
    config.vm.synced_folder COMMUNITY_FOLDER, "/home/vagrant/software/gnat_community"
  end

  # Initial provisioning
  config.vm.provision "shell", inline: INIT_PROVISIONING

  # This defines the non-graphical VM. Does not depend on plugins, to keep the
  # VM build as fast as possible.
  config.vm.define "uxas" do |uxas|

    config.vm.synced_folder "../OpenUxAS", "/home/vagrant/software/OpenUxAS"
    uxas.vm.provision "shell", inline: COMMON_PROVISIONING
  end

  # This defines the graphical VM. Does attempt to use plugins, because they
  # are needed/useful.
  config.vm.define "uxas-gui" do |uxas_gui|
    # Specific configuration for Virtual Box
    uxas_gui.vm.provider "virtualbox" do |vb_gui|
      if Vagrant.has_plugin?("vagrant-vbguest")
        uxas_gui.vbguest.auto_update = true
      else
        puts "** WARNING **: You really should install vagrant-vbguest:"
        puts "  `vagrant plugin install vagrant-vbguest`"
      end

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
    uxas_gui.vm.provision "shell", inline: GUI_PROVISIONING
  end
end
