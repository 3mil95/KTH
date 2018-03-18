import unittest
from syntaxFile import *

class SyntaxTest(unittest.TestCase):
    def testChapetalletter(self):
        self.assertEqual(checkMolekyl("He"), "Formeln är syntaktiskt korrekt!")
        self.assertEqual(checkMolekyl("cr12"), "Saknad stor bokstav")

    def testEndNumber(self):
        self.assertEqual(checkMolekyl("Ab1"), "För litet tal vid radslutet")
        self.assertEqual(checkMolekyl("Ab0"), "För litet tal vid radslutet")
        self.assertEqual(checkMolekyl("Mn4"), "Formeln är syntaktiskt korrekt!")


if __name__ == '__main__':
    unittest.main()