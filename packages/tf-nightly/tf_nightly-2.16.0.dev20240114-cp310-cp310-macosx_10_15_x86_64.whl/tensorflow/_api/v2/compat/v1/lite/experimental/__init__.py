# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.lite.experimental namespace
"""

import sys as _sys

from tensorflow._api.v2.compat.v1.lite.experimental import authoring
from tensorflow.lite.python.analyzer import ModelAnalyzer as Analyzer # line: 35
from tensorflow.lite.python.interpreter import OpResolverType # line: 303
from tensorflow.lite.python.interpreter import load_delegate # line: 125
from tensorflow.lite.python.op_hint import convert_op_hints_to_stubs # line: 1292
from tensorflow.lite.tools.optimize.debugging.python.debugger import QuantizationDebugOptions # line: 56
from tensorflow.lite.tools.optimize.debugging.python.debugger import QuantizationDebugger # line: 120

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "lite.experimental", public_apis=None, deprecation=False,
      has_lite=False)
