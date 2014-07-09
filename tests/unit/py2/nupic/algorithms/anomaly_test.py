#!/usr/bin/env python
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2014, Numenta, Inc.  Unless you have purchased from
# Numenta, Inc. a separate commercial license for this software code, the
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

"""Tests for anomaly-related algorithms."""

import unittest2 as unittest

from numpy import array

from nupic.algorithms import anomaly



class AnomalyTest(unittest.TestCase):


  def testComputeAnomalyScoreNoActiveOrPredicted(self):
    score = anomaly.computeAnomalyScore(array([]), array([]))
    self.assertAlmostEqual(score, 0.0)


  def testComputeAnomalyScoreNoActive(self):
    score = anomaly.computeAnomalyScore(array([]), array([3, 5]))
    self.assertAlmostEqual(score, 1.0)


  def testComputeAnomalyScorePerfectMatch(self):
    score = anomaly.computeAnomalyScore(array([3, 5, 7]), array([3, 5, 7]))
    self.assertAlmostEqual(score, 0.0)


  def testComputeAnomalyScoreNoMatch(self):
    score = anomaly.computeAnomalyScore(array([2, 4, 6]), array([3, 5, 7]))
    self.assertAlmostEqual(score, 1.0)


  def testComputeAnomalyScorePartialMatch(self):
    score = anomaly.computeAnomalyScore(array([2, 3, 6]), array([3, 5, 7]))
    self.assertAlmostEqual(score, 2.0 / 3.0)



if __name__ == "__main__":
  unittest.main()
