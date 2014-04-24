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

import os
import csv
import datetime

# Hot Gym data is stored with other data at
# examples/prediction/data/extra/hotgym
INPUT = '../../../../../prediction/data/extra/hotgym/raw/gym_input.csv'
LOCAL_DATA = 'local_data'
dataOut = {}
low = 100.0
high = 0.0


def _createOutputHeader():
  return [
    ['timestamp', 'kw_energy_consumption'],
    ['datetime', 'float'],
    ['T','']
  ]


def _convertDate(dateString):
  tokens = dateString.split()
  day, month, year = [int(x) for x in tokens[0].split('/')]
  if len(tokens) == 1:
    hour = 0
    minute = 0
  else:
    hour, minute, _ = [int(x) for x in tokens[1].split(':')]
    hour %= 12
    if tokens[2] == 'PM':
      hour += 12

  return datetime.datetime(year, month, day, hour, minute)


def _toFileName(name):
  return name.replace(' ', '_') + '.csv'


def _lineToData(line):
  global low, high
  # "   ","SITE_LOCATION_NAME","TIMESTAMP","TOTAL_KWH"
  consumption = float(line[3])
  # update low and high values
  if consumption > high:
    high = consumption
  if consumption < low:
    low = consumption
  return [_convertDate(line[2]), consumption]


def _processLine(line):
  gymName = line[1]
  if gymName not in dataOut.keys():
    dataOut[gymName] = _createOutputHeader()
  dataOut[gymName].append(_lineToData(line))


def _writeDataFiles():
  writtenFiles = {}
  if not os.path.exists(LOCAL_DATA):
    os.makedirs(LOCAL_DATA)
  for name, data in dataOut.iteritems():
    filePath = os.path.join(LOCAL_DATA, _toFileName(name))
    writtenFiles[name] = filePath
    with open(filePath, 'wb') as fileOut:
      writer = csv.writer(fileOut)
      for line in data:
        writer.writerow(line)
    print "Wrote output file: %s" % filePath
  return writtenFiles



def run(inputFile=INPUT):
  with open(inputFile, 'rb') as fileHandle:
    reader = csv.reader(fileHandle)
    # Skip header line.
    reader.next()
    for line in reader:
      _processLine(line)
    # Now that all the data has been input and processed, write out the files.
    writtenFiles = _writeDataFiles()
    print "Low: %f\t\tHigh: %f" % (low, high)
    return writtenFiles
