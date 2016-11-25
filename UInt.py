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


# =============================================================================
class UInt(Mot):
    """
    @To-Do
    """

    def __init__(self, n: int) -> 'UInt':
        """
        Returns an Unsigned Int of n bytes initialised at a random value
        The parameter n must be positive and not null

        :param n: number of bytes of the word
        :type n: int
        :return: Mot or Error
        """
        # n typed in the Mot constructor
        Mot.__init__(self, n)

        # Computing the first decimal value with binary setter
        self.binaire = self.binaire

    # =========================================================================
    # Getters and setters

    # Read-only
    @property
    def Maximum(self) -> int:
        """
        Getter for Maximum : the greater unsigned int of n bytes
        :return: int

        :Example:
        >>> a = UInt(3)
        >>> a.Maximum.valeur()
        16777215
        """
        U = UInt(self.nb_bytes)
        U.binaire = '1' * len(self)
        return U

    # Read-only
    @property
    def hexadecimal(self) -> str:
        """
        Getter for hexadecimal : the hexadecimal representation of this unsigned int
        :return: str

        :Example:
        >>> a = UInt(1)
        >>> a.binaire = '11111111'
        >>> a.hexadecimal
        'FF'
        """
        return super().valeur

    # =========================================================================
    # Methods
    def __add__(self, other: 'UInt') -> 'UInt':
        """
        Defines the addition of 2 UInt of same length, used as :
                self + other --> self.__add__(other)
        :param other: the unsigned int to add to
        :type other: UInt
        :return: UInt or Error

        :Example:
        >>> a = UInt(1) ; b = UInt(1) # The two must be of same length
        >>> a.binaire = '00000101' # Classic binary setting (see binaire.setter)
        >>> b.binaire = '00000001'
        >>> c = a + b # The addition returns a new UInt
        >>> c.binaire # An error can be raised :
        '00000110'
        >>> # In the case where a + b needs more bites than a and b
        """
        if type(other) != self.__class__ or len(self) != len(other):
            raise TypeError("Wrong type or length for other")
        retenue = 0
        new_bin = ''
        for i in range(len(self)):
            k = int(self.binaire[-(i + 1)]) + int(other.binaire[-(i + 1)]) + retenue
            new_bin = ['0', '1', '0', '1'][k] + new_bin
            retenue = 1 if k > 1 else 0
        if retenue:
            raise OverflowError("The sum is over the bytes available")
        H = self.__class__(self.nb_bytes)
        H.binaire = new_bin
        return H

    def __mul__(self, other: 'UInt') -> 'UInt':
        """
        Defines the multiplication of 2 unsigned int of same length, used as :
                self * other --> self.__mul__(other)
        The result has twice the length of self and other
        :param other: the unsigned int to multiply with
        :type other: UInt
        :return: UInt

        :Example:
        >>> a = UInt(1) ; b = UInt(1)
        >>> a.binaire = '00001000'
        >>> b.binaire = '00000101'
        >>> c = a*b
        >>> c.binaire
        '0000000000101000'
        """
        if type(other) != self.__class__ or len(self) != len(other):
            raise TypeError("The length and types must be the same")
        N = self.__class__(self.nb_bytes * 2)
        N.binaire = '0' * len(self) * 2
        for i in range(len(self)):
            if self.binaire[-(i + 1)] == '1':
                N = N + (other.extend(2 * self.nb_bytes) << i)
        return N

    def __lt__(self, other: 'UInt') -> bool:
        """
        Orders two UInt using : a < b -- > a.__lt__(b)
                                    True if a inferior to b, else false
                                a > b -- > b.__lt__(a)
                                    True if b inferior to a, else false
        :param other: the unsigned int to order with self
        :type other: UInt
        :return: bool
        """
        if type(other) != self.__class__ or len(self) != len(other):
            raise TypeError("other must be of same length and type")
        return self.compare(other) == '01'

    @Mot.binaire.setter
    def binaire(self, value: str):
        """ Overriding the setter to compute some values when setting"""
        Mot.binaire.fset(self, value)
        n = 0
        for i in range(len(self)):
            n += int(self.binaire[-(i + 1)]) * pow(2, i)
        self.__b10value = n

    def valeur(self) -> int:
        """
        Return the value in base 10 of this binary Unsigned Int
        :return: int
        """
        return self.__b10value

    # INUTILE =================================================================
    def __repr__(self) -> str:
        """
        Defines the repr of an Unsigned Int : adding the value in base 10
        :return: str
        """
        n = str(self.valeur())
        R = super().__repr__().split('\n')
        R[0] += '\u2553' + '\u2500' * (len(n) + 2) + '\u2556'
        R[1] += '\u2551 ' + n + ' \u2551'
        R[2] += '\u2559' + '\u2500' * (len(n) + 2) + '\u255C'
        return '\n'.join(R)