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
"""
Groups together the code dealing with swarming.
(This is a component of the Many Hot Gyms Prediction Tutorial.)
"""
import os
import pprint

from nupic.swarming import permutations_runner
from base_swarm_description import BASE_SWARM_DESCRIPTION



def _getSwarmDescriptionFor(inputDataFilePath):
  print "Constructing swarm desc for %s" % inputDataFilePath
  descCopy = dict(BASE_SWARM_DESCRIPTION)
  stream = descCopy["streamDef"]["streams"][0]
  stream["info"] = inputDataFilePath
  stream["source"] = "file://%s" % inputDataFilePath
  return descCopy



def _modelParamsToString(modelParams):
  pp = pprint.PrettyPrinter(indent=2)
  return pp.pformat(modelParams)



def _writeModelParamsFile(modelParams, name):
  cleanName = name.replace(" ", "_").replace("-", "_")
  paramsName = "%s_model_params.py" % cleanName
  outDir = os.path.join(os.getcwd(), 'model_params')
  if not os.path.isdir(outDir):
    os.mkdir(outDir)
  outPath = os.path.join(os.getcwd(), 'model_params', paramsName)
  with open(outPath, "wb") as outFile:
    modelParamsString = _modelParamsToString(modelParams)
    outFile.write("MODEL_PARAMS = \\\n%s" % modelParamsString)
    print "Wrote model params file to %s" % outPath
  return outPath



def _swarmForBestModelParams(swarmConfig, name, maxWorkers=4):
  outputLabel = name
  permWorkDir = os.path.abspath('swarm')
  if not os.path.exists(permWorkDir):
    os.mkdir(permWorkDir)
  modelParams = permutations_runner.runWithConfig(
    swarmConfig,
    {"maxWorkers": maxWorkers, "overwrite": True},
    outputLabel=outputLabel,
    outDir=permWorkDir,
    permWorkDir=permWorkDir,
    verbosity=0
  )
  modelParamsFile = _writeModelParamsFile(modelParams, name)
  return modelParamsFile, modelParams



def _printSwarmSizeWarning(size):
  if size is "small":
    print "= THIS IS A DEBUG SWARM. DON'T EXPECT YOUR MODEL RESULTS TO BE GOOD."
  elif size is "medium":
    print "= Medium swarm. Sit back and relax, this could take awhile."
  else:
    print "= LARGE SWARM! Might as well load up the Star Wars Trilogy."



def swarmForInput(inputFilePath, name):
  swarmDescription = _getSwarmDescriptionFor(inputFilePath)
  print "================================================="
  print "= Swarming on %s data..." % name
  _printSwarmSizeWarning(swarmDescription["swarmSize"])
  print "================================================="
  return _swarmForBestModelParams(swarmDescription, name)



def _runSwarm(filePath):
  name = os.path.splitext(os.path.basename(filePath))[0]
  return swarmForInput(filePath, name)



def _report(output):
  print "\nWrote the following model param files:"
  def modelReport(oneOutput):
    print "\t%s" % oneOutput[0]
  if isinstance(output, list):
    for i in output:
      modelReport(i)
  else:
    modelReport(output)



def swarm(inputPath):
  output = []
  if os.path.isdir(inputPath):
    for filePath in os.listdir(inputPath):
      output.append(_runSwarm(os.path.join(inputPath, filePath)))
  elif os.path.isfile(inputPath):
    output = _runSwarm(inputPath)
  else:
    raise Exception("Swarm input path '%s' does not exist." % inputPath)
  _report(output)
  return output
