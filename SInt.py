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
from UInt import UInt


# =============================================================================
class SInt(UInt):
    """
    @To-Do
    """

    def __init__(self, n: int) -> 'SInt':
        """ @To-Do """
        UInt.__init__(self, n)
        pass

    # =========================================================================
    # Getters and setters

    # Read-only
    @property
    def Maximum(self) -> int:
        """
        Getter for Maximum : the greater signed int of n bytes
        :return: int

        :Example:
        >>> a = UInt(4)
        >>> a.Maximum
        WRITE THE VALUE HERE
        """
        return 1

    # Read-only
    @property
    def Minimum(self) -> int:
        """
        Getter for Minimum : the lower signed int of n bytes
        :return: int

        :Example:
        >>> a = UInt(4)
        >>> a.Minimum
        WRITE THE VALUE HERE
        """
        return 1

    # Read-only
    @property
    def signe(self) -> int:
        """
        Getter for the sign of this signed int : 1 if negative, 0 if positive
        :return: int

        :Example:
        >>> a = SInt(1)
        >>> a.binaire = '11111111' #TEL QUE NEGATIF
        >>> a.signe
        1 # NEGATIF
        >>> a.binaire = '11111111' #TEL QUE POSITIF
        >>> a.signe
        0 # POSITIF
        """
        return 0

    # =========================================================================
    # Methods

if __name__ == '__main__':
    import doctest

    doctest.testmod()
