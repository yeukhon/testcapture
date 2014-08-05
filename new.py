import unittest

b = {}
class TestSample(unittest.TestCase):
    def setUp(self):
        self.a = 1

    def test_a_is_1(self):
        a = 1
#        print "{} hello {}".format(a, self.a)
#        print("do some hard work before assertion")
        self.assertEqual(self.a, 1)
        b[49] = self.a
        self.assertEqual(self.a, a)

#if __name__ == '__main__':
#    unittest.main()
