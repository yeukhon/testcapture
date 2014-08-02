import unittest

class TestSample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = 1
        cls.b = 2

    def setUp(self):
        self.c = 3
        self.d = 4

    def test_a_plus_b_equals_3(self):
        self.assertEqual(self.a + self.b, 3)

    def test_c_plus_d_equals_7(self):
        # Pretend we do some non-trivial work here
        expected = self.c + self.d
        self.assertEqual(expected, 7)

    def test_multiple_asserts_on_a_b(self):
        # Sometimes a test case has multiple assertions
        self.assertEqual(self.a, 1)
        self.assertNotEqual(self.b, 1)
        self.assertEqual(self.a + self.b, 3)
        self.assertTrue( self.a + self.b == 3)

if __name__ == "__main__":
    unittest.main()
