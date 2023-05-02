import unittest
import calc
 
 
class Test(unittest.TestCase):
 
    def test_sum(self):
        self.assertEqual(calc.sum(4, 7), 11)
 
    def test_sub(self):
        self.assertEqual(calc.sub(10, 5), 5)
 
    def test_mul(self):
        self.assertEqual(calc.mul(3, 7), 21)
 
    def test_div(self):
        self.assertEqual(calc.div(10, 2), 5)
 
 
if __name__ == '__main__':
    unittest.main()