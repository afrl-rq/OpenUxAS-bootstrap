# -*- mode: ruby -*-
# vi: set ft=ruby :

# See README.md, in the same directory as this Vagrantfile.

# This block is loaded into the shell before any other commands.
#
# This defines the logfile to which we write
VAGRANT_LOGFILE = "/home/vagrant/vagrant-provisioning-log.txt"

# Here's the logging function; the constant above is embedded directly.
LOG_REPORT_FUNCTION = <<-SHELL
  touch #{VAGRANT_LOGFILE}
  chown vagrant:vagrant #{VAGRANT_LOGFILE}

  log_report() {
    if [ $1 != "echo" ]; then
      echo $@ >> #{VAGRANT_LOGFILE}
    fi

    $@ >> #{VAGRANT_LOGFILE} 2>&1

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
  echo "# apt install -y git curl"
  apt-get install -y git curl

  echo " "
  echo "# end apt install"
  echo "# ------------------------------------------------------ #"
SHELL

# Cloning repos
PROVISIONING_BOOTSTRAP = <<-SHELL
  echo "# ------------------------------------------------------ #"
  cd /home/vagrant
  su -Hu vagrant git clone https://github.com/manthonyaiello/OpenUxAS-bootstrap bootstrap

  cd /home/vagrant/bootstrap
  su -Hu vagrant python3 util/install --automatic -vv --no-update
  echo "# ------------------------------------------------------ #"
SHELL


# Running install_ and setup_env
PROVISIONING_ENV = <<-SHELL
  echo " "
  echo "# ------------------------------------------------------ #"
  echo "# set profile"
  
  sudo -Hu vagrant echo "PATH=/home/vagrant/bootstrap/software/gnat/bin:\\$PATH" >> ~vagrant/.profile
  sudo -Hu vagrant echo "PATH=/home/vagrant/bootstrap/vpython/bin:\\$PATH" >> ~vagrant/.profile

  echo "# end set profile"
  echo "# ------------------------------------------------------ #"
SHELL

MOTD_MESSAGE = <<-SHELL

-------------------------------------------------------------------------------
Ubuntu 20.04 OpenUxAS Demonstration Vagrant Box
-------------------------------------------------------------------------------

This machine has been preconfigured with all dependencies required to build and
run OpenUxAS. To get started, run the following command:

  cd ~/bootstrap && ./anod-build uxas && ./anod-build amase

That will build the C++ version of OpenUxAS and OpenAMASE. Then, you can run
the waterways example like this:

  ./run-example 02_Example_WaterwaySearch

Additional instructions can be found in the README in ~/bootstrap/README.md (or
more easily read on github at https://github.com/AdaCore/OpenUxAS-bootstrap).

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
COMMON_PROVISIONING = build_logged_commands(PROVISIONING_BOOTSTRAP +
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
    uxas.vm.provision "shell", inline: COMMON_PROVISIONING
  end

  # This defines the graphical VM.
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
    uxas_gui.vm.provision "shell", inline: GUI_PROVISIONING
  end
end
