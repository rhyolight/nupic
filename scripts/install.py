import sys
import os
from setuptools import setup

"""
This file only will call CMake process to generate scripts, build, and then install the NuPIC binaries.
ANY EXTRA code related to build process MUST be put into CMake file.
"""

repositoryDir = os.getcwd()


def find_packages(repositoryDir):
  """
  Traverse nupic directory and create packages for each subdir containing a
  __init__.py file
  """
  packages = []
  for root, dirs, files in os.walk(repositoryDir + '/nupic'):
    if '__init__.py' in files:
      subdir = root.replace(repositoryDir + '/', '')
      packages.append(subdir.replace('/', '.'))
  return packages


# Call the setup process
os.chdir(repositoryDir)
setup(
  name = 'nupic',
  version = '1.0.0',
  packages = find_packages(repositoryDir),
  package_data = {
    'nupic': ['README.md', 'LICENSE.txt'],
    'nupic.bindings': ['_*.so', '_*.dll'],
    'nupic.data': ['*.json'],
    'nupic.frameworks.opf.exp_generator': ['*.json', '*.tpl'],
    'nupic.frameworks.opf.jsonschema': ['*.json'],
    'nupic.support.resources.images': ['*.png', '*.gif', '*.ico', '*.graffle'],
    'nupic.swarming.jsonschema': ['*.json']},
  description = 'Numenta Platform for Intelligent Computing',
  author='Numenta',
  author_email='help@numenta.org',
  url='https://github.com/numenta/nupic',
  classifiers=[
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: OS Independent',
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Artificial Intelligence'
  ],
  long_description = """\
NuPIC is a library that provides the building blocks for online prediction systems. The library contains the Cortical Learning Algorithm (CLA), but also the Online Prediction Framework (OPF) that allows clients to build prediction systems out of encoders, models, and metrics.

For more information, see numenta.org or the NuPIC wiki (https://github.com/numenta/nupic/wiki).
"""
)

