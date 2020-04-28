import subprocess
import os

# Version 73 is from 2018.
# If your version of Google Chrome is older
# than that, please consider upgrading.
CHROMEDRIVER_VERSIONS = {
	"73": "73.0.3683.68",
    "74": "74.0.3729.6",
    "75": "75.0.3770.140",
    "76": "76.0.3809.126",
    "77": "77.0.3865.40",
    "78": "78.0.3904.105",
    "79": "79.0.3945.36",
    "80": "80.0.3987.106",
    "81": "81.0.4044.69",
    "83": "83.0.4103.14"
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
    exit(CHROMEDRIVER_VERSIONS[gc_version[:2]])
 
get_compatibility()
