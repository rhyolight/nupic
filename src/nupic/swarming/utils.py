# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
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

import copy


def identityConversion(value, _keys):
  return value



def rCopy(d, f=identityConversion, discardNoneKeys=True, deepCopy=True):
  """Recursively copies a dict and returns the result.

  Args:
    d: The dict to copy.
    f: A function to apply to values when copying that takes the value and the
        list of keys from the root of the dict to the value and returns a value
        for the new dict.
    discardNoneKeys: If True, discard key-value pairs when f returns None for
        the value.
    deepCopy: If True, all values in returned dict are true copies (not the
        same object).
  Returns:
    A new dict with keys and values from d replaced with the result of f.
  """
  # Optionally deep copy the dict.
  if deepCopy:
    d = copy.deepcopy(d)

  newDict = {}
  toCopy = [(k, v, newDict, ()) for k, v in d.iteritems()]
  while len(toCopy) > 0:
    k, v, d, prevKeys = toCopy.pop()
    prevKeys = prevKeys + (k,)
    if isinstance(v, dict):
      d[k] = dict()
      toCopy[0:0] = [(innerK, innerV, d[k], prevKeys)
                     for innerK, innerV in v.iteritems()]
    else:
      #print k, v, prevKeys
      newV = f(v, prevKeys)
      if not discardNoneKeys or newV is not None:
        d[k] = newV
  return newDict

