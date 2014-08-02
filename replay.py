import imp
import os
import importlib
import unittest
import sys

CURR_DIR = os.path.abspath(os.path.dirname(__file__))
sample_tests = imp.load_source('sample_test', CURR_DIR + "/sample_tests.py")

"""
pk = importlib.import_module(sample_tests.__name__)
sample_tests = pk
print dir(pk)
"""

class MK_TestSample(sample_tests.TestSample):
    @classmethod
    def setUpClass(cls):
        super(MK_TestSample, cls).setUpClass()
        print("This is the mk version of setUpClass")
        print("a is: %s" % cls.a)
        print("b is: %s" % cls.b)

suite = unittest.TestLoader().loadTestsFromTestCase(MK_TestSample)
unittest.TextTestRunner(verbosity=2).run(suite)
