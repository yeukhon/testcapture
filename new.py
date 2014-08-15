import unittest

def foo(arg1, arg2):
    pass

A = "this is A"
b = {'key': 'None'}

def monitor_on(fname, lineno, variable_name, variable):
    print("{}:{}@{} > {}".format(fname, variable_name,
        lineno, variable))

class TestSample(unittest.TestCase):
    def setUp(self):
        self.a = "this is self.a"

    def test_a_is_1(self):
        print("before variable A")
        A = "this is new local A"
        print("--- before self.a")
        self.a = "this is new self.a"
        print("--- before subscript assignment")
        b["key"] = "new key"
        print("before assertEqual")
        self.assertEqual(b["key"], "new key")
        print("last statement")

#if __name__ == '__main__':
#    unittest.main()
