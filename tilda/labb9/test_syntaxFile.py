import unittest
from syntaxFile import *

class SyntaxTest(unittest.TestCase):
    def testOne(self):
        self.assertEqual(checkMolekyl("Na"), "Formeln är syntaktiskt korrekt")
        self.assertEqual(checkMolekyl("H2O"), "Formeln är syntaktiskt korrekt")
        self.assertEqual(checkMolekyl("Na332"), "Formeln är syntaktiskt korrekt")
        self.assertEqual(checkMolekyl("Si(C3(COOH)2)4(H2O)7"), "Formeln är syntaktiskt korrekt")

    def testTwo(self):
        self.assertEqual(checkMolekyl("C(Xx4)5"), "Okänd atom vid radslutet 4)5")
        self.assertEqual(checkMolekyl("C(OH4)C"), "Saknad siffra vid radslutet C")
        self.assertEqual(checkMolekyl("C(OH4C"), "Saknad högerparentes vid radslutet")
        self.assertEqual(checkMolekyl("H2O)Fe"), "Felaktig gruppstart vid radslutet )Fe")
        self.assertEqual(checkMolekyl("H0"), "För litet tal vid radslutet")
        self.assertEqual(checkMolekyl("H1C"), "För litet tal vid radslutet C")
        self.assertEqual(checkMolekyl("H02C"), "För litet tal vid radslutet 2C")
        self.assertEqual(checkMolekyl("Nacl"), "Saknad stor bokstav vid radslutet cl")
        self.assertEqual(checkMolekyl("a"), "Saknad stor bokstav vid radslutet a")
        self.assertEqual(checkMolekyl("(Cl)2)3"), "Felaktig gruppstart vid radslutet )3")
        self.assertEqual(checkMolekyl(")"), "Felaktig gruppstart vid radslutet )")
        self.assertEqual(checkMolekyl("2"), "Felaktig gruppstart vid radslutet 2")


if __name__ == '__main__':
    unittest.main()