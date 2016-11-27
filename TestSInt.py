from UInt import UInt
from Mot import Mot
import unittest
from random import randrange as rr
from SInt import SInt

class TestSInt(unittest.TestCase):
    """ TestCase of the class SInt's features """

    def test__init__(self):
        """
        Testing the class creation, expecting it to work with ints greater than 0
        """
        # Signature : output type
        #   -> Wrong types
        for elem in (-4, 0, 5.0, [], {}, '', '4'):
            with self.assertRaises(TypeError):
                SInt(elem)
        # -> Correct types
        SInt(2)

        # Signature : output type
        self.assertIsInstance(SInt(3), SInt)

    def test_signe_getter(self):
        """
        Testing the sign's getter
        """
        S = SInt(4)
        # Signature : output type
        self.assertIsInstance(S.signe, str)
        for i in range(4):
            S = SInt(4)
            self.assertEqual(S.signe in ('1', '0'), True)

    def test_Maximum_getter(self):
        """
        Testing the Maximum attribute's getter
        """
        # Signature : output type
        self.assertIsInstance(SInt(1).Maximum, SInt)
        # Axiome : result
        for n, Max in {0: 127, 1: 32767, 2: 8388607, 3: 2147483647}.items():
            # Numbers obtained using int('01111111' + '11111111'*i, 2); i [0,3]
            self.assertEqual(SInt(n + 1).Maximum.valeur(), Max)
            # Axiome : abs(S.Max) = abs(S.Min) - 1
            self.assertEqual(SInt(n + 1).Maximum.valeur(),
                             -1*SInt(n + 1).Minimum.valeur()-1)

    def test_Minimum_getter(self):
        """
        Testing the Minimum attribute's getter
        """
        # Signature : output type
        self.assertIsInstance(SInt(1).Minimum, SInt)
        # Axiome : result
        for n, Max in {0: 128, 1: 32768, 2: 8388608, 3: 2147483648}.items():
            # Numbers obtained using int('10000000'+'00000000'*i, 2)+1; i [0,3]
            self.assertEqual(SInt(n + 1).Minimum.valeur(), -Max)

    def test_valeur(self):
        """
        Testing the valeur method returning the signed int's value
        """
        # Axiome : output type
        self.assertIsInstance(SInt(3).valeur(), int)

        # Axiome : result
        binary = [''.join([str(rr(2)) for i in range(8)]) for i in range(40)]
        # Using the Axiome's property
        for bins in binary:
            S = SInt(1)
            val = int(bins, 2)
            S.binaire = bins
            if bins[0] == '0':
                self.assertEqual(S.valeur(), val)
            else :
                self.assertEqual(S.valeur(), [-1, 1][val < 128] * (2**8 - val))

    def test__rshift__(self):
        """
        Testing __rshift__ : method shifting bites to the right
        """
        # Signature : input type
        S = SInt(3)
        for x in ('', [], {}, 1.2, -4, ()):
            with self.assertRaises(TypeError):
                S >> x

        # Signature : output type
        self.assertIsInstance(S >> 4, SInt)

        # Axiome : result
        for n in range(1, 4):
            for i in (1, 3, 4, 12, 1456):
                # Shifting just like in 'Mot', but the sign
                # must remain at the first position
                # Also must still verify x << n == x * 2**(n+1), n < len(x)
                S = SInt(n)
                M = Mot(n)
                M.binaire = '0' + S.binaire[1:]
                self.assertEqual(S.signe + (M >> i).binaire[1:], (S >> i).binaire)

    def test_extend(self):
        """
        Testing extend : method adding zeros to the left
        """
        # Signature : input type
        S = SInt(3)
        for x in ('', [], {}, 1.2, ()):
            with self.assertRaises(TypeError):
                S.extend(x)

        # Signature : output type
        self.assertIsInstance(S.extend(4), SInt)

        # Axiome : result
        for n in range(-2, 7):
            for i in range(3):
                S = SInt(3)
                self.assertEqual(S.signe, S.extend(n).signe)
                self.assertEqual(S.binaire[-len(S) - 1:], (S.extend(n)).binaire[-len(S):])

    def test_compare(self):
        """
        Testing the compare method: testing 2 SInt and returning '10','01','00'
        """
        for i in range(50):
            A = SInt(1)
            B = SInt(1)
            self.assertEqual(A < B, A.valeur() < B.valeur())

    def test_complement(self):
        """
        Testing the 'complement à deux' method :
            'complement à deux'(x) = 'complement à un'(x) + 1
        """
        # Signature : return type
        S = SInt(4)
        self.assertIsInstance(S.complement(), SInt)

        # Axiome : value
        for i in range(10):
            S = SInt(4)
            self.assertEqual(int(S.complement().binaire, 2), 2**len(S) - int(S.binaire, 2))

    def test__abs__(self):
        """
        Testing the __abs__ method :
            a = x.__abs__ or a = abs(x)
            -> a.valeur() == abs(x.valeur())
                -> a.valeur() == x.valeur() if x.signe == 0
                -> a.valeur() == -x.valeur() if x.signe == 1
        """
        # Signature : return type
        S = SInt(4)
        self.assertIsInstance(abs(S), SInt)

        # Axiome : length
        self.assertEqual(abs(S).nbBytes, S.nbBytes)

        # Axiome : positive
        self.assertEqual(abs(S).signe, '0')

        # Axiome : value
        for i in range(10):
            S = SInt(4)
            if S.signe == '1':
                ABS = abs(S)
                self.assertEqual(2 ** len(S) - int(ABS.binaire, 2), int(S.binaire, 2))

    def test__add__(self):
        """
        Testing the __add__ method :
            s = x.__add__(y) or s = x + y
            with s.valeur() == x.valeur() + y.valeur()
        """
        # Signature : return type
        S = SInt(1)
        S.binaire = '00000111'
        self.assertIsInstance(S + S, SInt)

        # Axiome : length
        self.assertEqual((S + S).nbBytes, S.nbBytes)

        # Axiome : result
        for i in range(25):
            S1 = SInt(1)
            S2 = SInt(1)
            real_sum = S1.valeur() + S2.valeur()
            if real_sum > 127 or real_sum < -128 :
                with self.assertRaises(OverflowError):
                    S1 + S2
            else :
                self.assertEqual((S1+S2).valeur(), real_sum)

    def test__sub__(self):
        """
        Testing the __sub__ method :
            s = x.__sub__(y) or s = x - y
            with s.valeur() == x.valeur() - y.valeur()
        """
        for i in range(25):
            S1 = SInt(1)
            S2 = SInt(1)
            real_sum = S1.valeur() - S2.valeur()
            if real_sum > 127 or real_sum < -128 or S2 == S2.Minimum:
                with self.assertRaises(OverflowError):
                    S1 - S2
            else :
                self.assertEqual((S1 - S2).valeur(), real_sum)

    def test__mul__(self):
        """
        Testing the __mul__ method :
            m = x.__mul__(y) or m = x * y
            with m.valeur() == x.valeur() * y.valeur()
        """
        for i in range(25):
            S1 = SInt(2)
            S2 = SInt(2)
            real_mul = S1.valeur() * S2.valeur()
            self.assertEqual((S1 * S2).valeur(), real_mul)

    def test__divmod__(self):
        """
        Testing __divmod__ method :
            (d,r) = a.__divmod__(b)
            - > d.value() == a.value() // b.value()
            - > r.value() == a.value() % b.value()
        """
        verbose = 0 # to print the detail for this function

        def test_floordiv(A,B):
            floordiv1 = A.valeur() // B.valeur()
            if verbose >= 1 :
                print(
                    """On regarde : A = {a}\n             B = {b}\n               On s'attend à avoir {aval} // {bval} = {afbval}""".format(
                        a=A.binaire, b=B.binaire, aval=A.valeur(), bval=B.valeur(), afbval=floordiv1
                    ))
            floordiv2 = (A // B).valeur()
            if verbose >= 1:
                print("               Et on a : A // B = {afbvaldeux}\n".format(afbvaldeux=floordiv2))
            return floordiv1,floordiv2

        def test_mod(A,B):
            mod1 = A.valeur() % B.valeur()
            if verbose >= 1:
                print(
                    """On regarde : A = {a}\n             B = {b}\n               On s'attend à avoir {aval} % {bval} = {afbval}""".format(
                        a=A.binaire, b=B.binaire, aval=A.valeur(), bval=B.valeur(), afbval=mod1
                    ))
            mod2 = (A % B).valeur()
            if verbose >= 1:
                print("               Et on a : A % B = {afbvaldeux}\n".format(afbvaldeux=mod2))
            return mod1, mod2

        for i in range(15):
            # Creating 2 numbers A & B, positive, A > B
            n = 1
            A,B = SInt(1), SInt(1)
            a,b = rr(127)+1,rr(127)+1
            A.binaire = bin(max(a,b))[2:].zfill(8)
            B.binaire = bin(min(a,b))[2:].zfill(8)
            # First case : divmod(A,B) : + > +

            if verbose >= 1:
                print("================================================================================")
                print("On teste +A // +B")
            self.assertEqual(*test_floordiv(A, B))
            if verbose >= 1:
                print("Test de +A // +B réussi !!\n\n")

                print("On teste +A % +B")
            self.assertEqual(*test_mod(A, B))
            if verbose >= 1:
                print("Test de A % B réussi !!")
                print("================================================================================")

            # First case : divmod(B,A) : + < +
            if verbose >= 1:
                print("================================================================================")
                print("On teste +B // +A")
            self.assertEqual(*test_floordiv(B, A))
            if verbose >= 1:
                print("Test de +B // +A réussi !!")

                print("On teste +B % +A")
            self.assertEqual(*test_mod(B, A))
            if verbose >= 1:
                print("Test de B % A réussi !!")
                print("================================================================================")

            # First case : divmod(-A,B) : - > + # SOLUTION : -A // B == -(A // B + 1)
                print("================================================================================")
                print("On teste -A // +B")
            self.assertEqual(*test_floordiv(-A, B))
            if verbose >= 1:
                print("Test de -A // +B réussi !!")

                print("On teste -A % +B")
            self.assertEqual(*test_mod(-A, B))
            if verbose >= 1:
                print("Test de -A % B réussi !!")
                print("================================================================================")

            # First case : divmod(A,-B) : + > -
                print("================================================================================")
                print("On teste +A // -B")
            self.assertEqual(*test_floordiv(A, -B)) # SOLUTION : A // -B == -(A // B + 1)
            if verbose >= 1:
                print("Test de +A // -B réussi !!")

                print("On teste +A % -B")
            self.assertEqual(*test_mod(A, -B))
            if verbose >= 1:
                print("Test de A % -B réussi !!")
                print("================================================================================")

            # First case : divmod(-B, A) : - < +
                print("================================================================================")
                print("On teste -B // A")
            self.assertEqual(*test_floordiv(-B, A)) # SOLUTION : -B // A == -1 TOUT LE TEMPS
            if verbose >= 1:
                print("Test de -B // +A réussi !!")

                print("On teste -B % +A")
            self.assertEqual(*test_mod(-B, A))
            if verbose >= 1:
                print("Test de -B % +A réussi !!")
                print("================================================================================")

            # First case : divmod(B, -A) : + < -
                print("================================================================================")
                print("On teste +B // -A")
            self.assertEqual(*test_floordiv(B, -A))
            if verbose >= 1:
                print("Test de +B // -A réussi !!")

                print("On teste +B % -A")
            self.assertEqual(*test_mod(B, -A))
            if verbose >= 1:
                print("Test de B % -A réussi !!")
                print("================================================================================")

            # First case : divmod(-A,-B) : - > -
                print("================================================================================")
                print("On teste -A // -B")
            self.assertEqual(*test_floordiv(-A, -B))
            if verbose >= 1:
                print("Test de -A // -B réussi !!")

                print("On teste -A % -B")
            self.assertEqual(*test_mod(-A, -B))
            if verbose >= 1:
                print("Test de -A % -B réussi !!")
                print("================================================================================")

            # First case : divmod(-B,-A) : - < -
                print("================================================================================")
                print("On teste -B // -A")
            self.assertEqual(*test_floordiv(-B, -A))
            if verbose >= 1:
                print("Test de -B // -A réussi !!")

                print("On teste -B % -A")
            self.assertEqual(*test_mod(-B, -A))
            if verbose >= 1:
                print("Test de -B % -A réussi !!")
                print("================================================================================")

    def test__floordiv__(self):
        """
        Testing __floordiv__ method :
            -> f = a.__floordiv__(b) or f = a // b
            -> f.value() == a.value() // b.value()
        """
        #TESTED IN DIVMOD
        pass

    def test__mod__(self):
        """
        Testing __mod__ method :
            -> m = a.__mod__(b) or m = a % b
            -> m.valeur() == a.valeur() % b.valeur()
        """
        # TESTED IN DIVMOD
        pass


if __name__ == '__main__':
    unittest.main()
