import subprocess
import os

# Version 70.0.3538.16 is from 2018.
# If your version of Google Chrome is older
# than that, please consider upgrading.
CHROMEDRIVER_VERSIONS = {
}

def get_compatibility():
    gc_proc =  subprocess.Popen("google-chrome --version", shell=True, stdout=subprocess.PIPE).stdout
    gc_version =  gc_proc.read()
    gc_version = ".".join(gc_version.decode('utf-8').split()[-1].split(".")[:-1])
    cd_proc = subprocess.Popen('chromedriver --version', shell=True, stdout=subprocess.PIPE).stdout
    cd_version = cd_proc.read()
    cd_version = ".".join(cd_version.decode('utf-8').split()[1].split(".")[:-1])
    if gc_version == cd_version:
        exit(0)
    exit('81.0.4044.69')
 
get_compatibility()
