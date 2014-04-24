# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------
import importlib
import os

from nupic.frameworks.opf.modelfactory import ModelFactory

from swarm_helper import swarmForInput
from io_helper import runIoThroughNupic
import generate_data


DATA_DIR = "./local_data"
MODEL_PARAMS_DIR = "./model_params"



def _createModel(modelParams):
  model = ModelFactory.create(modelParams)
  model.enableInference({"predictedField": "kw_energy_consumption"})
  return model



def _getModelParamsFromName(gymName):
  importedModelParams = importlib.import_module(
    "model_params.%s_model_params" % (
      gymName.replace(" ", "_").replace("-", "_")
    )
  ).MODEL_PARAMS
  return importedModelParams



def runModel(gymName, plot=False):
  print "Creating model from %s..." % gymName
  model = _createModel(_getModelParamsFromName(gymName))
  inputData = ["%s/%s.csv" % (DATA_DIR, gymName.replace(" ", "_"))]
  runIoThroughNupic(inputData, [model], [gymName], plot)



def runAllModels(plot=False):
  models = []
  names = []
  inputFiles = []
  for inputFile in sorted(os.listdir(DATA_DIR)):
    name = os.path.splitext(inputFile)[0]
    names.append(name)
    inputFiles.append(os.path.abspath(os.path.join(DATA_DIR, inputFile)))
    models.append(_createModel(_getModelParamsFromName(name)))
  runIoThroughNupic(inputFiles, models, names, plot)



def runItAll(gymName=None, plot=False):
  inputFiles = generate_data.run()
  print "Generated input data files:"
  print inputFiles
  names = inputFiles.keys()
  inputFiles = inputFiles.values()
  allModelParams = []

  # Giving a gym name will limit all operations to just one gym instead of every
  # gym in the input data.
  if gymName is not None:
    if gymName not in names:
      raise Exception("No gym named '%s'." % gymName)
    gymIndex = names.index(gymName)
    inputFiles = [inputFiles[gymIndex]]
    names = [gymName]

  for index, inputFilePath in enumerate(inputFiles):
    modelParams = swarmForInput(inputFilePath, names[index])
    allModelParams.append(modelParams)

  print
  print "================================================="
  print "= Swarming complete!                            ="
  print "================================================="
  print

  models = []

  for index, modelParams in enumerate(allModelParams):
    print "Creating %s model..." % names[index]
    models.append(_createModel(modelParams[1]))

  print
  print "================================================="
  print "= Model creation complete!                      ="
  print "================================================="
  print

  runIoThroughNupic(inputFiles, models, names, plot)
