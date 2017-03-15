# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2014, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

import math

import numpy
from pyproj import Proj, transform
from nupic.encoders.coordinate import CoordinateEncoder



class CartesianCoordinateEncoder(CoordinateEncoder):
  """
  Given a GPS coordinate and a speed reading, the
  Geospatial Coordinate Encoder returns an SDR representation
  of that position.
  """

  def __init__(self,
               scale,
               timestep,
               w=21,
               n=1000,
               name=None,
               verbosity=0):
    """
    See `nupic.encoders.base.Encoder` for more information.

    @param scale (int) Scale of the map, as measured by
                       distance between two coordinates
                       (in dimensional units)
    @param timestep (int) Time between readings (in seconds)
    """
    super(CartesianCoordinateEncoder, self).__init__(w=w,
                                                      n=n,
                                                      name=name,
                                                      verbosity=verbosity)

    self.scale = scale
    self.timestep = timestep


  def getDescription(self):
    """See `nupic.encoders.base.Encoder` for more information."""
    return [('speed', 0), ('x', 1), ('y', 2), ('z', 3)]


  def getScalars(self, inputData):
    """See `nupic.encoders.base.Encoder` for more information."""
    return numpy.array([0] * len(self.getDescription()))


  def encodeIntoArray(self, inputData, output):
    """
    See `nupic.encoders.base.Encoder` for more information.

    @param inputData (tuple) Contains speed (float), x (float), y (float),
                             z (float)
    @param output (numpy.array) Stores encoded SDR in this numpy array
    """
    z = 0
    if len(inputData) == 4:
      (speed, x, y, z) = inputData
    else:
      (speed, x, y) = inputData
    print len(inputData)
    print "Z: {}".format(z)
    coordinate = self.coordinateForPosition(x, y, z)
    radius = self.radiusForSpeed(speed)
    super(CartesianCoordinateEncoder, self).encodeIntoArray(
     (coordinate, radius), output)


  def coordinateForPosition(self, x, y, z):
    """
    Returns coordinate for given GPS position.

    @param x (float) Cartesian X value of position
    @param y (float) Cartesian Y value of position
    @param z (float) Cartesian Z value position
    @return (numpy.array) Coordinate that the given Cartesian position
                          maps to
    """
    coordinate = numpy.array((x, y, z))
    print coordinate
    coordinate = coordinate / self.scale
    print coordinate.astype(int)
    return coordinate.astype(int)


  def radiusForSpeed(self, speed):
    """
    Returns radius for given speed.

    Tries to get the encodings of consecutive readings to be
    adjacent with some overlap.

    @param speed (float) Speed (in meters per second)
    @return (int) Radius for given speed
    """
    overlap = 1.5
    coordinatesPerTimestep = speed * self.timestep / self.scale
    radius = int(round(float(coordinatesPerTimestep) / 2 * overlap))
    minRadius = int(math.ceil((math.sqrt(self.w) - 1) / 2))
    return max(radius, minRadius)


  def dump(self):
    print "CartesianCoordinateEncoder:"
    print "  w:   %d" % self.w
    print "  n:   %d" % self.n


  @classmethod
  def read(cls, proto):
    encoder = super(CartesianCoordinateEncoder, cls).read(proto)
    encoder.scale = proto.scale
    encoder.timestep = proto.timestep
    return encoder


  def write(self, proto):
    super(CartesianCoordinateEncoder, self).write(proto)
    proto.scale = self.scale
    proto.timestep = self.timestep
