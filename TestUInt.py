# =============================================================================
'''
Quick description of the file
'''
# =============================================================================
__author__ = 'Simon Lassourreuille'
__version__ = ''
__date__ = '27/10/2016'
__email__ = 'simon.lassourreuille@etu.u-bordeaux.fr'
__status__ = 'Prototype'
# =============================================================================
from UInt import UInt
import unittest
from random import randint as rdi
from Mot import Mot


# =============================================================================
class TestUInt(unittest.TestCase):
    """ TestCase of the class Mot's features """

    def test__init__(self):
        """
        Testing the class creation, expecting it to work with ints greater than 0
        """
        # Testing a few TypeErrors
        for elem in (-4, 0, 5.0, [], {}, '', '4'):
            with self.assertRaises(TypeError):
                UInt(elem)
        # Testing a correct call
        UInt(2)

    def test_Maximum_getter(self):
        """
        Testing the Maximum attribute's getter
        """
        for n,max in {1:255, 2:65535, 3:16777215, 4:4294967295}.items():
            # Numbers obtained using int('11111111'*i, 2)
            self.assertEqual(UInt(n).Maximum, max)

    def test_hexadecimal(self):
        """
        Testing the hexadecimal attribute's getter
        """
        for i in range(5):
            # Tests done using the Python builtins functions
            U = UInt(rdi(1,15))
            Hex = hex(int(U.binaire,2))[2:].upper()
            self.assertEqual(U.hexadecimal,(len(U.hexadecimal)-len(Hex))*'0'+Hex)

    def test__add__(self):
        """
        Testing the addition of 2 Unsigned Ints
        """
        U = UInt(4)
        U.binaire = '0'*24 + '1'*8
        # Testing type of params
        V = UInt(4)
        V.binaire = '0'*16 + '00000001' + '0'*8
        for elem in (1,-1,'',2,[],{},2.5, Mot(1)):
            with self.assertRaises(TypeError):
                U + elem
        # Testing the return type
        self.assertIsInstance(U + V, UInt)
        # First testing if this works with same length UInts
        for i in range(5):
            k = rdi(1,5)
            U = UInt(k)
            V = UInt(k)
            S = U.valeur() + V.valeur()
            if S > U.Maximum :
                with self.assertRaises(ArithmeticError):
                    U + V
            else :
                W = U + V
                self.assertEqual(W.valeur(), S)
        # Testing with different length
        for i in range(5):
            U = UInt(rdi(1,5))
            V = UInt(rdi(1,5))
            S = U.valeur() + V.valeur()
            if S > U.Maximum and S > V.Maximum:
                with self.assertRaises(ArithmeticError):
                    U + V
            else:
                W = U + V
                self.assertEqual(W.valeur(), S)
        # Testing the arithmetic error
        U = UInt(4)
        V = UInt(4)
        U.binaire = '1'*len(U)
        V.binaire = '0'*(len(V)-1) + '1'
        with self.assertRaises(ArithmeticError):
            U + V

    def test__mul__(self):
        """
        Testing the multiplication of 2 unsigned ints
        """
        U = UInt(4)
        # Testing type of params
        V = UInt(4)
        for elem in (1, -1, '', 2, [], {}, 2.5, Mot(1)):
            with self.assertRaises(TypeError):
                U * elem
        # Testing the return type
        self.assertIsInstance(U * V, UInt)
        # First testing if this works with same length UInts
        for i in range(5):
            k = rdi(1, 5)
            U = UInt(k)
            V = UInt(k)
            W = U * V
            self.assertEqual(W.valeur(),U.valeur() * V.valeur())
        # Testing with different length
        for i in range(5):
            U = UInt(rdi(1, 5))
            V = UInt(rdi(1, 5))
            W = U * V
            self.assertEqual(W.valeur(),U.valeur() * V.valeur())

    def test__lt__(self):
        """
        Testing the comparison of 2 unsigned ints
        """
        U = UInt(4)
        # Testing type of params
        for elem in (1, -1, '', 2, [], {}, 2.5, Mot(1)):
            with self.assertRaises(TypeError):
                U < elem
        # Testing the return type
        V = UInt(4)
        self.assertIsInstance(U < V, bool)
        # Testing the comparison of same lengths ints
        k = rdi(1,5)
        ints = [UInt(k) for i in range(5)]
        for i in range(5):
            for j in range(5):
                self.assertEqual(ints[i] < ints[j],
                                 ints[i].valeur()<ints[j].valeur())
        # Testing the comparison of different lengths ints
        ints = [UInt(rdi(1,5)) for i in range(5)]
        for i in range(5):
            for j in range(5):
                self.assertEqual(ints[i] < ints[j],
                                 ints[i].valeur() < ints[j].valeur())

    def test_valeur(self):
        """
        Testing the valeur method
        """
        # Testing return type
        self.assertIsInstance(UInt(4).valeur(), int)
        # Testing with Python builtins
        for i in range(15):
            U = UInt(rdi(1,15))
            self.assertEqual(U.valeur(),int(U.binaire,2))

if __name__ == '__main__':
    unittest.main()
