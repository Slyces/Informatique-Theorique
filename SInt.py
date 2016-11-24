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
# Imports
from Mot import Mot
from UInt import UInt


# =============================================================================
class SInt(UInt):
    """
    Binary representation of a signed int :
    [_010111010010101]
    the first bit is for the sign
    if the first bit is 0, the number is positive :
        then its value is the value of the remaining bites
    if the first bit is 1, the number is negative :
        then its value is (-1)*complement(remaining bites)
    """

    def __init__(self, n: int) -> 'SInt':
        """ @To-Do """
        # n typed in the UInt constructor
        UInt.__init__(self, n)

    # =========================================================================
    # Getters and setters

    # Read-only
    @property
    def Maximum(self) -> 'SInt':
        """
        Getter for Maximum : the greater signed int of n bytes
        :return: SInt

        :Example:
        >>> a = SInt(1)
        >>> a.Maximum.valeur()
        127
        """
        S = SInt(self.nb_bytes)
        S.binaire = '0' + '1' * (len(self) - 1)
        return S

    # Read-only
    @property
    def Minimum(self) -> 'SInt':
        """
        Getter for Minimum : the lower signed int of n bytes
        :return: SInt

        :Example:
        >>> a = SInt(1)
        >>> a.Minimum.valeur()
        -128
        """
        S = SInt(self.nb_bytes)
        S.binaire = '1' + '0' * (len(self) - 1)
        return S

    # Read-only
    @property
    def signe(self) -> str:
        """
        Getter for the sign of this signed int : '1' if negative, '0' if positive
            --> Warning ! The result is a string !
        :return: str

        :Example:
        >>> a = SInt(1)
        >>> a.binaire = '10110011' #TEL QUE NEGATIF
        >>> a.signe
        '1'
        >>> a.binaire = '01100101' #TEL QUE POSITIF
        >>> a.signe
        '0'
        """
        return self.binaire[0]

    # =========================================================================
    # Methods
    def __rshift__(self, n: int) -> 'SInt':
        """
        This method shifts the bites to the rights but keeps the sign
        at the right place
        :param n: how many times we will shift of 1 bite to the right
                      (how many bites will be shifted)
        :return: SInt
        """
        if type(n) != int or n < 0:
            raise TypeError("Wrong type for n : positive integer needed")
        n = min(n, len(self) - 1)
        S = SInt(self.nb_bytes)
        S.binaire = self.signe + '0' * n + self.binaire[1:-n]
        return S

    def extend(self, N: int) -> 'SInt':
        """
        See Mot's extend doc ;
        improved to keep the sign bite at the left when adding '0'
        :param N: length of the new SInt
        :return: SInt
        """
        if type(N) != int:
            raise TypeError("N must be an int")
        # Extending to something lower than nb_bytes has no effect
        if N <= self.nb_bytes:
            return self
        S = SInt(N)
        S.binaire = self.signe + '0' * (N * 8 - len(self) - 1) + self.binaire
        return S

    def complement(self)->'SInt':
        """
        Every bite of the SInt is converted to its opposite (1 <-> 0)
        Then we add 1 to the result
        :return: SInt
        :Example:
        >>> S = SInt(1)
        >>> S.binaire = '10001010'
        >>> S.complement().binaire
        '01110110'
        """
        S = SInt(self.nb_bytes)
        S.binaire = '0' * (len(self) - 1) + '1'
        S += super(SInt, self).complement()
        return S

    def __abs__(self) -> 'SInt':
        """
        Abs takes an SInt of nbBytes = n in input and outputs :
        x if x is positive
        (-x) if x is negative
        error if x = x.Minimum
        :return: SInt | OverflowError
        """
        if self.binaire == self.Minimum.binaire:
            raise OverflowError('abs(x) does not work if x is the minimum'
                                ', try to encode your SInt on 1 more byte')
        return self if self.signe == '0' else self.complement()

    def valeur(self) -> int:
        """ Returns the value of the SignedInt"""
        if self.signe == '0':
            return super().valeur()
        if self == self.Minimum:
            return -2 ** (len(self) - 1)
        return - abs(self).valeur()

    def __add__(self, other: 'SInt') -> 'SInt':
        """ Addition of 2 SInt, no overflow """
        # Recoding the addition
        if type(other) != self.__class__ or len(self) != len(other):
            raise TypeError("Wrong type or length for other")
        retenue = [0 for i in range(len(self) + 1)]
        new_bin = ''
        for i in range(len(self)):
            k = int(self.binaire[-(i + 1)]) + int(other.binaire[-(i + 1)]) + retenue[i]
            new_bin = ['0', '1', '0', '1'][k] + new_bin
            retenue[i + 1] = 1 if k > 1 else 0
        if self.signe == other.signe and retenue[-1] != retenue[-2]:
            raise OverflowError("The sum is over the bytes available")
        H = self.__class__(self.nb_bytes)
        H.binaire = new_bin
        return H

    def __sub__(self, other: 'SInt') -> 'SInt':
        """ Subtraction of 2 SInt """
        return self + other.complement()

    def __mul__(self, other: 'SInt') -> 'SInt':
        """ Multiplication of 2 Signed Ints"""
        if self.signe == other.signe == '0':
            return super().__mul__(other)
        if self.signe == other.signe:
            return abs(self) * abs(other)
        return -(abs(self) * abs(other))

    def __neg__(self) -> 'SInt':
        """ As defined in an axiome, self.complement() == neg(self)"""
        return self.complement()

    def __divmod__(self, other: 'SInt') -> 'SInt':
        """ Defines the divmod of a and b, returns a pair (a//b,a%b)"""
        if type(self) != type(other):
            raise TypeError("Wrong type or length for other")

        size = max(self.nb_bytes, other.nb_bytes)
        Divid, Divis = abs(self).cast(size), abs(other).cast(size)
        Quotient = SInt(size)
        one = SInt(size)
        one.binaire = '0' * (size * 8 - 1) + '1'
        Quotient.binaire = '0' * 8 * size
        print("Dividende :\n{}\n".format(Divid))
        print("Diviseur :\n{}".format(Divis))
        while Divis < Divid or Divis == Divid:
            Quotient += one
            Divid -= Divis
            print("-----------------------------------------------\nQuotient :\n{}".format(Quotient))
            print("Reste :\n{}\n-----------------------------------------------".format(Divid))
        print("End of the While")
        # Here, the remain is the dividende
        Remainer = Divid
        if self.signe != other.signe:  # Problems occur only with different signs
            if Remainer.valeur() == 0:  # When abs(a) % abs(b) == 0, there is specific instructions
                Quotient = -Quotient
            else:
                Quotient = -(Quotient + one)
                # ---------------------------------------------------------------------------------
                print("New Quotient because signs != :\n{}".format(Quotient))
                q_b = Quotient * other
                print("Quotient * B :\n{}".format(q_b))
                selcasted = self.cast(2 * size)
                print("self.casted :\n{}".format(selcasted))
                subb = selcasted - q_b
                print("Sub : self.casted - Quotient * B\n{}".format(subb))
                subb8 = subb << size * 8
                print("Sub << size * 8\n".format(subb8))
                test = subb8.cast(size)
                print("Remainer :\n{}".format(test))

                Remainer = ((self.cast(2 * size) - (Quotient * other)) << size * 8).cast(size)
                # ---------------------------------------------------------------------------------
        if self.signe == other.signe == '1':
            Remainer = - Remainer
        return Quotient, Remainer

    def __floordiv__(self, other: 'SInt') -> 'SInt':
        """ Defines self // other """
        return self.__divmod__(other)[0]

    def __mod__(self, other: 'SInt') -> 'SInt':
        """ Defines self % other """
        return self.__divmod__(other)[1]