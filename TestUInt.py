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

if __name__ == '__main__':
    print("=" * 80 + "\nFirst going through the doc examples :")
    doctest.testmod()
    print("\n" + "=" * 80 + "\nNow unit testing (may overlap with doc_tests):")
    unittest.main()