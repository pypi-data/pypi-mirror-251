import subprocess
import os

def run_command(command):
    subprocess.run(command, shell=True, check=True)

def install_quickfix():
    # Install necessary tools and libraries
    run_command("sudo yum install -y git ruby libtool")
    run_command("sudo yum group install -y 'Development Tools'")
    run_command("sudo yum install -y m4")

    # Clone QuickFIX repository
    run_command("git clone https://github.com/quickfix/quickfix.git")

    # Download and install Autoconf
    run_command("wget http://ftp.gnu.org/gnu/autoconf/autoconf-latest.tar.gz")
    run_command("tar -xvzf autoconf-latest.tar.gz")
    os.chdir("autoconf-2.72")  # Update this if the version changes
    run_command("./configure --prefix=/usr/local")
    run_command("make")
    run_command("sudo make install")
    run_command("hash -r")

    # Continue with QuickFIX installation
    os.chdir("../quickfix")
    run_command("./bootstrap")
    run_command("./configure")
    run_command("make")
    run_command("make check")
    run_command("sudo make install")

if __name__ == "__main__":
    install_quickfix()
