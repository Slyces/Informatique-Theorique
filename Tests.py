# =============================================================================
'''
Quick description of the file
'''
# =============================================================================
__author__ = 'Simon Lassourreuille'
__version__ = ''
__date__ = '24/11/2016'
__email__ = 'simon.lassourreuille@etu.u-bordeaux.fr'
__status__ = 'Prototype'
# =============================================================================
import unittest
import doctest
import Mot
import UInt
import SInt
from TestMot import TestMot
from TestUInt import TestUInt
from TestSInt import TestSInt

if __name__ == '__main__':
    doctest.testmod(Mot)
    doctest.testmod(SInt)
    doctest.testmod(UInt)

    unittest.main()