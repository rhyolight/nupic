import sys
import os
import subprocess

"""
This file only will call CMake process to generate scripts, build, and then install the NuPIC binaries.
ANY EXTRA code related to build process MUST be put into CMake file.
"""

repositoryDir = os.getcwd()


# Read command line options looking for extra options for CMake and Make
# For example, an user could type:
#   python setup.py install make_options='-j3'
# which will add '-j3' option to Make commandline
cmakeOptions = ""
makeOptions = ""
installOptions = ""
for arg in sys.argv:
  if ("cmake_options" in arg) or ("make_options" in arg):
    (option, _, rhs) = arg.partition("=")
    if option[0] == "--cmake_options":
      cmakeOptions = rhs
    if option[0] == "--make_options":
      makeOptions = rhs
  elif (not "setup.py" in arg):
    installOptions += arg + " "


def build_nupic():
  """
  CMake-specific build operations
  """

  # Prepare directories to the CMake process
  sourceDir = repositoryDir
  buildScriptsDir = repositoryDir + '/build/scripts'
  if not os.path.exists(buildScriptsDir):
    os.makedirs(buildScriptsDir)
  os.chdir(buildScriptsDir)

  # Generate build files with CMake
  return_code = subprocess.call("cmake " + sourceDir + ' ' + cmakeOptions, shell=True)
  if (return_code != 0):
    sys.exit("Unable to generate build scripts!")

  # Build library with Make
  return_code = subprocess.call("make " + makeOptions, shell=True)
  if (return_code != 0):
    sys.exit("Unable to build the library!")


def install_nupic():
  """
  SetupTools install operations
  """
  
  # Install library
  os.chdir(repositoryDir)
  return_code = subprocess.call("python scripts/install.py " + installOptions, shell=True)
  if (return_code != 0):
    sys.exit("Unable to install the library!")


# Build and install NuPIC
build_nupic()
install_nupic()
