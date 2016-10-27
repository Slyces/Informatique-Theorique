# =============================================================================
"""
Quick description of the file
"""
# =============================================================================
__author__ = 'Simon Lassourreuille'
__version__ = ''
__date__ = '21/10/2016'
__email__ = 'simon.lassourreuille@etu.u-bordeaux.fr'
__status__ = 'Prototype'
# =============================================================================
from Mot import Mot
import unittest
import doctest


# =============================================================================
class TestMot(unittest.TestCase):
    """ TestCase of the class Mot's features """

    def setUp(self):
        """
        Most of the tests will be performed on the binary word self.M :
        '0010101100101011'
        """
        self.M = Mot(2)
        self.M.binaire = '0010101100101011'

    def test_Mot__init__(self):
        """
        Testing the class creation, expecting it to work with ints greater than 0
        """
        # Testing a few TypeErrors
        for elem in (-4, 0, 5.0, [], {}, '', '4'):
            with self.assertRaises(TypeError):
                Mot(elem)
        # Testing a correct call
        Mot(2)

    def test_nb_bytes_getter(self):
        """
        Testing the getter of nb_bytes, expected to be equal to the parameter given to this instance
        """
        # Testing return type
        self.assertIsInstance(self.M.nb_bytes, int)
        # Testing if the value is correctly initialised
        self.assertEqual(self.M.nb_bytes, 2)

    def test_binaire_getter(self):
        """
        Testing the getter of binaire, assuming the setter is working.
        """
        # Testing return type
        self.assertIsInstance(self.M.binaire, str)
        # Testing if the value is correctly returned
        self.assertEqual(self.M.binaire, '0010101100101011')

    def test_binaire_setter(self):
        """
        Testing the setter of binaire, expected to work with :
            - strings of length 8*nb_bytes
            - only composed of 0 & 1
        """
        # Testing a few TypeError
        for element in ('001010110010101a', '', '001010110010101', 4, True, {},
                        [0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], None):
            with self.assertRaises(TypeError):
                self.M.binaire = element
        binary = '00010010'
        # Testing some correct parameters
        for i in range(1, 6):
            k = Mot(i)
            k.binaire = binary * i

    def test_valeur_getter(self):
        """
        Testing the getter of valeur
        """
        # Testing the return type
        self.assertIsInstance(self.M.valeur, str)
        # Testing the globality of the result, may be:2b2b,2B2B,0x2b2b,0x2B2B
        self.assertIn('2b2b', self.M.valeur.lower())

    def test__len__(self):
        """
        Testing len(Mot), supposed to be an int equal to len(Mot.binaire)
                                                        or 8*Mot.nb_bytes
        """
        l = len(self.M)
        # Testing the return type
        self.assertIsInstance(l, int)
        # Testing if the two ways of computation are equals
        self.assertEqual(l, len(self.M.binaire))
        self.assertEqual(l, 8 * self.M.nb_bytes)

    def test__rshift__(self):
        """
        Testing Mot.__rshift__ ( Mot >> x ), expecting it to work with positive ints
        and shift the bites to the right, filling with 0 to the left
        """
        # Testing a few TypeError
        for x in ('', [], {}, 1.2, -4, ()):
            with self.assertRaises(TypeError):
                self.M >> x
        # Testing the return type
        self.assertIsInstance(self.M >> 2, Mot)
        # Testing the actual method
        L = self.M >> 2
        self.assertEqual(L.binaire, '0000101011001010')
        L = self.M >> 8
        self.assertEqual(L.binaire, '0000000000101011')
        # Testing if x > len(M) works fine
        L = self.M >> 14587
        self.assertEqual(L.binaire, '0000000000000000')

    def test__lshift__(self):
        """
        Testing Mot.__lshift__ ( Mot << x ), expecting it to work with positive ints
        and shift the bites to the left, filling with 0 to the right
        """
        # Testing a few TypeErrors
        for x in ('', [], {}, 1.2, -4, ()):
            with self.assertRaises(TypeError):
                self.M << x
        # Testing the return type
        self.assertIsInstance(self.M << 2, Mot)
        # Testing the actual method
        L = self.M << 2
        self.assertEqual(L.binaire, '1010110010101100')
        L = self.M << 8
        self.assertEqual(L.binaire, '0010101100000000')
        # Testing if x > len(M) works fine
        L = self.M << 14587
        self.assertEqual(L.binaire, '0000000000000000')

    def test_complement(self):
        """
        Testing the Mot.complement method, expecting to return a Mot
            with binary representation's 0 & 1 inverted
        """
        # Testing the return type
        self.assertIsInstance(self.M.complement(), Mot)
        # Testing the actual method
        L = self.M.complement()
        self.assertEqual(L.binaire, '1101010011010100')
        self.M.binaire = '0000000000000000'
        L = self.M.complement()
        self.assertEqual(L.binaire, '1111111111111111')
        self.M.binaire = '1111111111111111'
        L = self.M.complement()
        self.assertEqual(L.binaire, '0000000000000000')

    def test_compare(self):
        """
        Testing the Mot.compare method, going through the bites left to right and
        returning the 2 first different bites encountered, starting with the
        instance of Mot calling the function. This function expects two Mot
        of the same length.
        """
        # Self.M.binaire = '0010101100101011'
        L = Mot(2)
        L.binaire = '0010101100001011'
        # Testing the return type
        self.assertIsInstance(self.M.compare(L), str)
        # Testing the actual method
        self.assertEqual(self.M.compare(L), '10')
        L.binaire = '0011101100101011'
        self.assertEqual(self.M.compare(L), '01')
        self.assertEqual(L.compare(self.M), '10')
        self.assertEqual(self.M.compare(self.M), '00')
        self.assertEqual(L.compare(L), '00')
        # Testing if adding 1 empty byte at the left has no effect
        L.relativExtension(1)
        self.assertEqual(self.M == L, False)
        H = self.M.relativExtension(1)
        self.assertEqual(self.M == H, True)

    def test_extend(self):
        """
        Testing the Mot.extend method, returning a Mot of max(n, N, 1) bytes
            filled with 0 to the left if needed
        """
        # Testing the return type
        self.assertIsInstance(self.M.extend(2), Mot)
        # Testing a few TypeError
        for n in ('', [], {}, 1.2, ()):
            with self.assertRaises(TypeError):
                self.M.extend(n)
        # Testing if n < M.nb_bytes has no effect
        for n in (-178954,-4,0,1,2):
            self.assertEqual(self.M.binaire,self.M.extend(n).binaire)
            self.assertEqual(self.M.nb_bytes, self.M.extend(n).nb_bytes)

        # Testing the filling to the left
        self.assertEqual(self.M.extend(6).binaire,
                         '000000000000000000000000000000000010101100101011')
        self.assertEqual(self.M.extend(6).nb_bytes, 6)

    def test_reduce(self):
        """
        Testing the Mot.reduce method, returning a Mot of min(n, N, 1) bytes
            loosing the right part if needed
        """
        # Testing the return type
        self.assertIsInstance(self.M.reduce(2), Mot)
        # Testing a few TypeError
        for n in ('', [], {}, 1.2, ()):
            with self.assertRaises(TypeError):
                self.M.reduce(n)
        # Testing if n > nb_bytes works and has no effect
        for n in (178954, 4, 2):
            self.assertEqual(self.M.binaire, self.M.reduce(n).binaire)
            self.assertEqual(self.M.nb_bytes, self.M.reduce(n).nb_bytes)

        # Testing if n < 1 has the same effect than n = 1
        for n in (0, -4, -1456):
            self.assertEqual(self.M.reduce(1).binaire, self.M.reduce(n).binaire)
            self.assertEqual(self.M.reduce(n).nb_bytes, 1)

        # Testing if the right part is removed
        M = Mot(6)
        M.binaire = '010011000100101010011001110001010011101100101011'
        results = ('0100110001001010100110011100010100111011',
                   '01001100010010101001100111000101',
                   '010011000100101010011001',
                   '0100110001001010',
                   '01001100')
        for i in range(5):
            L = M.reduce(5-i)
            self.assertEqual(L.nb_bytes, 5-i)
            self.assertEqual(L.binaire,results[i])

    def test_cast(self):
        """
        Testing the Mot.cast method
        """
        # Testing the return type
        self.assertIsInstance(self.M.cast(2), Mot)
        M = Mot(6)
        M.binaire = '010011000100101010011001110001010011101100101011'
        # Testing the 'smart' call to reduce
        for n in (-14,-5,0,1,2,4,5):
            self.assertEqual(M.cast(n).binaire, M.reduce(n).binaire)
            self.assertEqual(M.cast(n).nb_bytes, M.reduce(n).nb_bytes)
        # Testing the 'smart' call to extend
        for n in (6,7,12,205):
            self.assertEqual(M.cast(n).nb_bytes, M.extend(n).nb_bytes)
            self.assertEqual(M.cast(n).binaire, M.extend(n).binaire)

    def test_relativExtension(self):
        """
        Testing the Mot.relivExtension method
        """
        M = Mot(6)
        M.binaire = '010011000100101010011001110001010011101100101011'
        # Testing the return type
        self.assertIsInstance(M.relativExtension(0), Mot)
        # Testing if 0 has no effect
        self.assertEqual(M.relativExtension(0).binaire, M.binaire)
        self.assertEqual(M.relativExtension(0).nb_bytes, M.nb_bytes)
        # Testing some values that should work fine
        for n in (-174,-25,-9,-4,-2,0,1,3,7,9,12,254):
            self.assertEqual(M.relativExtension(n).nb_bytes, M.cast(6+n).nb_bytes)
            self.assertEqual(M.relativExtension(n).binaire, M.cast(6+n).binaire)

    def test__eq__(self):
        """
        Testing the Mot.__eq__ (M == L) method
        """
        # Testing return type
        self.assertIsInstance(self.M == self.M, bool)
        # Testing A == A : true
        self.assertEqual(self.M == self.M, True)
        # Testing different length comparison
        L = Mot(2)
        L.binaire = '1000000000000000'
        self.assertEqual(self.M == L, False)
        # Testing if adding 1 empty byte at the left has no effect
        L.relativExtension(1)
        self.assertEqual(self.M == L, False)


if __name__ == '__main__':
    print("=" * 80 + "\nFirst going through the doc examples :")
    doctest.testmod()
    print("\n" + "=" * 80 + "\nNow unit testing (may overlap with doc_tests):")
    unittest.main()
