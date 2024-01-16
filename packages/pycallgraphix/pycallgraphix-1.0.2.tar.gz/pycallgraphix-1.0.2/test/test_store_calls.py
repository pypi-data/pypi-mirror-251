import unittest
from pycallgraphix.wrapper import register_method, SingletonForCallGraph

class TestStoreCalls(unittest.TestCase):

    def test_store_calls(self):
        self.sum_recursive(1,2)
        for func in SingletonForCallGraph().my_info:
            self.assertEqual(SingletonForCallGraph().my_info[func]["callcounter"], 3)

    @register_method
    def sum_recursive(self, a, b):
        if b > 0:
            a += 1
            b -= 1
            self.print_value(prefix='current', value=a)
            return self.sum_recursive(a, b)
        else:
            self.print_value(prefix='final', value=a)
            return a
    
    @register_method
    def print_value(self, prefix, value):
        print("{} value = {}".format(prefix,value))