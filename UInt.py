# =============================================================================
'''
Quick description of the file
'''
# =============================================================================
__author__ = 'Simon Lassourreuille'
__version__ = ''
__date__ = '21/10/2016'
__email__ = 'simon.lassourreuille@etu.u-bordeaux.fr'
__status__ = 'Prototype'
# =============================================================================
# Imports
from Mot import Mot, same_length


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
        self.__Maximum = pow(2, len(self)+1) - 1

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
        >>> a.Maximum
        33554431
        """
        return self.__Maximum

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
        return self.__valeur

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
        '00000110'    # In the case where a + b needs more bites than a and b
        """
        return UInt(1)

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
        '0000000000101000' 8 * 5 = 40
        """
        return UInt(2)

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
        return False

    def valeur(self) -> int:
        """
        Return the value in base 10 of this binary Unsigned Int
        :return: int
        """
        n = 0
        for i in range(len(self)):
            n += int(self.binaire[-(i + 1)]) * pow(2, i)
        return n

    # INUTILE =================================================================
    def __repr__(self) -> str:
        """
        Defines the repr of an Unsigned Int : adding the value in base 10
        :return: str
        """
        n = str(self.valeur())
        R = super().__repr__().split('\n')
        R[0] += '\u2553' + '\u2500' * (len(n)+2) + '\u2556'
        R[1] += '\u2551 ' + n + ' \u2551'
        R[2] += '\u2559' + '\u2500' * (len(n)+2) + '\u255C'
        return '\n'.join(R)


if __name__ == '__main__':
    M = UInt(3)
    print(M)
    print(M.Maximum)
