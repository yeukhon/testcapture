import types
import unittest

import sample_tests

class MK_TestSample(sample_tests.TestSample):
    @classmethod
    def setUpClass(cls):
        super(MK_TestSample, cls).setUpClass()
        print("This is the mk version of setUpClass")
        print("a is: %s" % cls.a)
        print("b is: %s" % cls.b)

#sample_tests.TestSample.setUpClass = mk_setUpClass
#suite = unittest.TestLoader().loadTestsFromTestCase(sample_tests.TestSample)
suite = unittest.TestLoader().loadTestsFromTestCase(MK_TestSample)
unittest.TextTestRunner(verbosity=2).run(suite)
