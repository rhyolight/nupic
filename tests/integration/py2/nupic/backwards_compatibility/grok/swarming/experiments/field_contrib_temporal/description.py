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
Template file used by the OPF Experiment Generator to generate the actual
description.py file by replacing $XXXXXXXX tokens with desired values.

This description.py file was generated by:
'/Users/ronmarianetti/nta/eng/lib/python2.6/site-packages/nupic/frameworks/opf/expGenerator/ExpGenerator.py'
"""

from nupic.frameworks.opf.expdescriptionapi import ExperimentDescriptionAPI

from nupic.frameworks.opf.expdescriptionhelpers import (
  updateConfigFromSubConfig,
  applyValueGettersToContainer,
  DeferredDictLookup)

from nupic.frameworks.opf.clamodelcallbacks import *
from nupic.frameworks.opf.metrics import MetricSpec
from nupic.frameworks.opf.opfutils import (InferenceType,
                                           InferenceElement)
from nupic.support import aggregationDivide

from nupic.frameworks.opf.opftaskdriver import (
                                            IterationPhaseSpecLearnOnly,
                                            IterationPhaseSpecInferOnly,
                                            IterationPhaseSpecLearnAndInfer)


# Model Configuration Dictionary:
#
# Define the model parameters and adjust for any modifications if imported
# from a sub-experiment.
#
# These fields might be modified by a sub-experiment; this dict is passed
# between the sub-experiment and base experiment
#
#
# NOTE: Use of DEFERRED VALUE-GETTERs: dictionary fields and list elements
#   within the config dictionary may be assigned futures derived from the
#   ValueGetterBase class, such as DeferredDictLookup.
#   This facility is particularly handy for enabling substitution of values in
#   the config dictionary from other values in the config dictionary, which is
#   needed by permutation.py-based experiments. These values will be resolved
#   during the call to applyValueGettersToContainer(),
#   which we call after the base experiment's config dictionary is updated from
#   the sub-experiment. See ValueGetterBase and
#   DeferredDictLookup for more details about value-getters.
#
#   For each custom encoder parameter to be exposed to the sub-experiment/
#   permutation overrides, define a variable in this section, using key names
#   beginning with a single underscore character to avoid collisions with
#   pre-defined keys (e.g., _dsEncoderFieldName2_N).
#
#   Example:
#      config = dict(
#        _dsEncoderFieldName2_N = 70,
#        _dsEncoderFieldName2_W = 5,
#        dsEncoderSchema = [
#          base=dict(
#            fieldname='Name2', type='ScalarEncoder',
#            name='Name2', minval=0, maxval=270, clipInput=True,
#            n=DeferredDictLookup('_dsEncoderFieldName2_N'),
#            w=DeferredDictLookup('_dsEncoderFieldName2_W')),
#        ],
#      )
#      updateConfigFromSubConfig(config)
#      applyValueGettersToContainer(config)
config = {
    # Type of model that the rest of these parameters apply to.
    'model': "CLA",

    # Version that specifies the format of the config.
    'version': 1,

    # Intermediate variables used to compute fields in modelParams and also
    # referenced from the control section.
    'aggregationInfo': {   'days': 0,
        'fields': [   (u'timestamp', 'first'),
                      (u'gym', 'first'),
                      (u'consumption', 'mean'),
                      (u'address', 'first')],
        'hours': 0,
        'microseconds': 0,
        'milliseconds': 0,
        'minutes': 0,
        'months': 0,
        'seconds': 0,
        'weeks': 0,
        'years': 0},
    
    'predictAheadTime': None,

    # Model parameter dictionary.
    'modelParams': {
        # The type of inference that this model will perform
        'inferenceType': 'TemporalNextStep',

        'sensorParams': {
            # Sensor diagnostic output verbosity control;
            # if > 0: sensor region will print out on screen what it's sensing
            # at each step 0: silent; >=1: some info; >=2: more info;
            # >=3: even more info (see compute() in py/regions/RecordSensor.py)
            'verbosity' : 0,

            # Example:
            #     dsEncoderSchema = [
            #       DeferredDictLookup('__field_name_encoder'),
            #     ],
            #
            # (value generated from DS_ENCODER_SCHEMA)
            'encoders': {   'address': {   'fieldname': u'address',
                               'n': 300,
                               'name': u'address',
                               'type': 'SDRCategoryEncoder',
                               'w': 21},
                'consumption': {   'clipInput': True,
                                   'fieldname': u'consumption',
                                   'maxval': 200,
                                   'minval': 0,
                                   'n': 1500,
                                   'name': u'consumption',
                                   'type': 'ScalarEncoder',
                                   'w': 21},
                'gym': {   'fieldname': u'gym',
                           'n': 300,
                           'name': u'gym',
                           'type': 'SDRCategoryEncoder',
                           'w': 21},
                'timestamp_dayOfWeek': {   'dayOfWeek': (7, 3),
                                           'fieldname': u'timestamp',
                                           'name': u'timestamp_dayOfWeek',
                                           'type': 'DateEncoder'},
                'timestamp_timeOfDay': {   'fieldname': u'timestamp',
                                           'name': u'timestamp_timeOfDay',
                                           'timeOfDay': (7, 8),
                                           'type': 'DateEncoder'}},

            # A dictionary specifying the period for automatically-generated
            # resets from a RecordSensor;
            #
            # None = disable automatically-generated resets (also disabled if
            # all of the specified values evaluate to 0).
            # Valid keys is the desired combination of the following:
            #   days, hours, minutes, seconds, milliseconds, microseconds, weeks
            #
            # Example for 1.5 days: sensorAutoReset = dict(days=1,hours=12),
            #
            # (value generated from SENSOR_AUTO_RESET)
            'sensorAutoReset' : None,
        },

        'spEnable': True,

        'spParams': {
            # SP diagnostic output verbosity control;
            # 0: silent; >=1: some info; >=2: more info;
            'spVerbosity' : 0,

            'globalInhibition': 1,

            # Number of cell columns in the cortical region (same number for
            # SP and TP)
            # (see also tpNCellsPerCol)
            'columnCount': 2048,

            'inputWidth': 0,

            # SP inhibition control (absolute value);
            # Maximum number of active columns in the SP region's output (when
            # there are more, the weaker ones are suppressed)
            'numActivePerInhArea': 40,

            'seed': 1956,

            # coincInputPoolPct
            # What percent of the columns's receptive field is available
            # for potential synapses. At initialization time, we will
            # choose coincInputPoolPct * (2*coincInputRadius+1)^2
            'coincInputPoolPct': 0.5,

            # The default connected threshold. Any synapse whose
            # permanence value is above the connected threshold is
            # a "connected synapse", meaning it can contribute to the
            # cell's firing. Typical value is 0.10. Cells whose activity
            # level before inhibition falls below minDutyCycleBeforeInh
            # will have their own internal synPermConnectedCell
            # threshold set below this default value.
            # (This concept applies to both SP and TP and so 'cells'
            # is correct here as opposed to 'columns')
            'synPermConnected': 0.1,

            'synPermActiveInc': 0.1,

            'synPermInactiveDec': 0.01,
        },

        # Controls whether TP is enabled or disabled;
        # TP is necessary for making temporal predictions, such as predicting
        # the next inputs.  Without TP, the model is only capable of
        # reconstructing missing sensor inputs (via SP).
        'tpEnable' : True,

        'tpParams': {
            # TP diagnostic output verbosity control;
            # 0: silent; [1..6]: increasing levels of verbosity
            # (see verbosity in nta/trunk/py/nupic/research/TP.py and TP10X*.py)
            'verbosity': 0,

            # Number of cell columns in the cortical region (same number for
            # SP and TP)
            # (see also tpNCellsPerCol)
            'columnCount': 2048,

            # The number of cells (i.e., states), allocated per column.
            'cellsPerColumn': 32,

            'inputWidth': 2048,

            'seed': 1960,

            # Temporal Pooler implementation selector (see _getTPClass in
            # CLARegion.py).
            'temporalImp': 'cpp',

            # New Synapse formation count
            # NOTE: If None, use spNumActivePerInhArea
            #
            # TODO: need better explanation
            'newSynapseCount': 15,

            # Maximum number of synapses per segment
            #  > 0 for fixed-size CLA
            # -1 for non-fixed-size CLA
            #
            # TODO: for Ron: once the appropriate value is placed in TP
            # constructor, see if we should eliminate this parameter from
            # description.py.
            'maxSynapsesPerSegment': 32,

            # Maximum number of segments per cell
            #  > 0 for fixed-size CLA
            # -1 for non-fixed-size CLA
            #
            # TODO: for Ron: once the appropriate value is placed in TP
            # constructor, see if we should eliminate this parameter from
            # description.py.
            'maxSegmentsPerCell': 128,

            # Initial Permanence
            # TODO: need better explanation
            'initialPerm': 0.21,

            # Permanence Increment
            'permanenceInc': 0.1,

            # Permanence Decrement
            # If set to None, will automatically default to tpPermanenceInc
            # value.
            'permanenceDec' : 0.1,

            'globalDecay': 0.0,

            'maxAge': 0,

            # Minimum number of active synapses for a segment to be considered
            # during search for the best-matching segments.
            # None=use default
            # Replaces: tpMinThreshold
            'minThreshold': 12,

            # Segment activation threshold.
            # A segment is active if it has >= tpSegmentActivationThreshold
            # connected synapses that are active due to infActiveState
            # None=use default
            # Replaces: tpActivationThreshold
            'activationThreshold': 16,

            'outputType': 'normal',

            # "Pay Attention Mode" length. This tells the TP how many new
            # elements to append to the end of a learned sequence at a time.
            # Smaller values are better for datasets with short sequences,
            # higher values are better for datasets with long sequences.
            'pamLength': 1,
        },

        'clParams': {
            'regionName' : 'CLAClassifierRegion',

            # Classifier diagnostic output verbosity control;
            # 0: silent; [1..6]: increasing levels of verbosity
            'clVerbosity' : 0,

            # This controls how fast the classifier learns/forgets. Higher values
            # make it adapt faster and forget older patterns faster.
            'alpha': 0.001,

            # This is set after the call to updateConfigFromSubConfig and is
            # computed from the aggregationInfo and predictAheadTime.
            'steps': '1',
            
            
        },

        'trainSPNetOnlyIfRequested': False,
    },
          
  
}
# end of config dictionary


# Adjust base config dictionary for any modifications if imported from a
# sub-experiment
updateConfigFromSubConfig(config)


# Compute predictionSteps based on the predictAheadTime and the aggregation
# period, which may be permuted over.
if config['predictAheadTime'] is not None:
  predictionSteps = int(round(aggregationDivide(
      config['predictAheadTime'], config['aggregationInfo'])))
  assert (predictionSteps >= 1)
  config['modelParams']['clParams']['steps'] = str(predictionSteps)


# Adjust config by applying ValueGetterBase-derived
# futures. NOTE: this MUST be called after updateConfigFromSubConfig() in order
# to support value-getter-based substitutions from the sub-experiment (if any)
applyValueGettersToContainer(config)




################################################################################

control = {
  # The environment that the current model is being run in
  "environment": 'grok',

  # Input stream specification per py/grokengine/cluster/database/StreamDef.json.
  #
  'dataset' : {   u'info': u'test_NoProviders',
      u'streams': [   {   u'columns': [u'*'],
                          u'info': u'test data',
                          u'source': u'file://test_data.csv'}],
      u'version': 1},


  # Iteration count: maximum number of iterations.  Each iteration corresponds
  # to one record from the (possibly aggregated) dataset.  The task is
  # terminated when either number of iterations reaches iterationCount or
  # all records in the (possibly aggregated) database have been processed,
  # whichever occurs first.
  #
  # iterationCount of -1 = iterate over the entire dataset
  #'iterationCount' : ITERATION_COUNT,

  # Metrics: A list of MetricSpecs that instantiate the metrics that are
  # computed for this experiment
  'metrics':[
    MetricSpec(field=u'consumption',
               inferenceElement=InferenceElement.prediction,
               metric='rmse'),
  ],

  # Logged Metrics: A sequence of regular expressions that specify which of
  # the metrics from the Inference Specifications section MUST be logged for
  # every prediction. The regex's correspond to the automatically generated
  # metric labels. This is similar to the way the optimization metric is
  # specified in permutations.py.
  'loggedMetrics': ['.*grokScore.*'],
}



################################################################################
################################################################################
descriptionInterface = ExperimentDescriptionAPI(modelConfig=config,
                                                control=control)
