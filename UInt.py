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
from Mot import Mot


# =============================================================================
class UInt(Mot):
    """
    @To-Do
    """

    def __init__(self, n: int) -> 'UInt':
        """ @To-Do """
        Mot.__init__(self, n)
        pass

    # =========================================================================
    # Getters and setters

    # Read-only
    @property
    def Maximum(self) -> int:
        """
        Getter for Maximum : the greater unsigned int of n bytes
        :return: int

        :Example:
        >>> a = UInt(4)
        >>> a.Maximum
        16777215
        """
        return 1

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
        return 'FF'

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
        '0000000000101000' 8 + 32 = 40
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


if __name__ == '__main__':
    import doctest

    doctest.testmod()
