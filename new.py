import unittest

def foo(arg1, arg2):
    pass

A = "this is A"
b = {'key': 'None'}
class TestSample(unittest.TestCase):
    def setUp(self):
        self.a = "this is self.a"

    def test_a_is_1(self):
        foo(A, self.a)
#        print "{} hello {}".format(a, self.a)
#        print("do some hard work before assertion")

#if __name__ == '__main__':
#    unittest.main()
