# Many Hot Gyms Prediction Tutorial

The program in this folder is the complete source code for the "Many Hot Gyms Prediction" Tutorial. This is an extension to the "One Hot Gyms Prediction Tutorial". It presents a more complete case-study of a NuPIC application that processes many inputs, creates many NuPIC models, and feeds data & extracts predictions from all of them at once.

## Premise

The "hot gym" sample application has been around for a long time, and was one of the first real-world applications of NuPIC that actually worked. The data used is real energy consumption data from several gym buildings in Australia. We start with a raw data file and process in a way that NuPIC can swarm over the data, then feed each one into NuPIC Models.

### What's the different between this and the "One Gym" Tutorial?

This program is a more complete application with more processing options. It starts from a raw data file, showing how to process it into multiple files formatted for NuPIC (one for each gym). Each step of this process is broken into commands for a CLI, and can be run on one gym at a time, or all gyms simultaneously. The output is can be plotted and viewed across all gyms at once, which makes for an interesting demo of the live capabilities of many NuPIC Models at once.

## Program Description

This is a Python CLI program that uses NuPIC's [Online Prediction Framework](https://github.com/numenta/nupic/wiki/Online-Prediction-Framework). The CLI wrapper is described in the [Running the Program](#running-the-program) section below.

## Program Phases

### 1. Swarming Over the Input Data

Swarming is an essential part of preparing a NuPIC Model. 

#### Swarm Description

The swarming process requires an initial _swarm description_, which defines the input data and limits some of the permutations that must occur during the swarming process.

> **TODO: include base description here**

- `includedFields`: These correspond do the columns of data the swarm will use when searching for model parameters. A `fieldName` and `fieldType` are required. In this example, we are specifying minimum and maximum values for the `kw_energy_consuption` data column, which will help the swarm logic limit the amount of work it does to find the best params.

- `streamDef`: Tells the swarm where the input data file is. You have to put the "file://" prefix before the path to the data file defined in `streams.source`. The path can be relative or absolute.

- `inferenceType`: Indicates that we expect time-based multistep predictions to be evaluated. Other inference types include `Multistep`, `NontemporalMultistep`, and `TemporalAnomaly`.

- `inferenceArgs`: Defines which field should be predicted, and how many steps into the future the field should be predicted. Several step-ahead predictions can be specified in `predictionSteps`, but be aware that more prediction steps will slow down NuPIC execution.

- `iterationCount`: How many rows within the input data file to swarm over. If `-1`, assume all rows.

- `swarmSize`: Can be `small`, `medium`, and `large`. Small swarms are used only for debugging. Medium swarms are almost always what you want. Large swarms can take a very long time, but get slightly better model params than medium.

#### Results of the Swarms

##### Working files (junk)
> Once the swarm is complete, you'll see a `swarm` folder within your working directory. It contains the internal workings of the swarm, which includes utilities you can use for advanced swarming (out of scope for this tutorial). This tutorial application places all the swarming junk into the `swarm` folder mostly just to keep the working directory uncluttered. When you [run swarms](https://github.com/numenta/nupic/wiki/Running-Swarms) through the swarming CLI, all this cruft is dumped into your current working directory.

##### Model Params (GOLD!)
> Within the `model_params` directory, you'll also see a python file appear called `rec-center-hourly_model_params.py`. This file contains a configuration object for the **best model** the swarm found for the input data. This config object is used to create the NuPIC Model in the next step.

### 2. Running the NuPIC Models

> The primary result of swarming is the **best model** configuration (detailed above). Once the best model parameters have been identified, a new NuPIC Model object can be created, data can be passed into it, and predictions can be retrieved. During this phase of the program, a new Model is created, and the [rec-center-hourly.csv](rec-center-hourly.csv) input data file is fed line-by-line into the model. For each line feed, a prediction for the next value of energy consumption is retrieved from the NuPIC Model and either written to file or presenting in a graph on the screen.

### 3. Cleanup (optional)

This phase simply removes all the file artifacts created within previous steps from the file system and presents a clean slate for further program executions.

## Running the Program

**TODO**
