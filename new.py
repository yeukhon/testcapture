import unittest

def foo():
    pass

b = {'key': 'None'}
class TestSample(unittest.TestCase):
    def setUp(self):
        self.a = 1

    def test_a_is_1(self):
        a = 1
        foo()
        self.assertEqual(self.a, a)
        self.a = 1
        b['key'] = 'hello'
#        print "{} hello {}".format(a, self.a)
#        print("do some hard work before assertion")

#if __name__ == '__main__':
#    unittest.main()
