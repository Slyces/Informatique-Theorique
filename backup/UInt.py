# =============================================================================
'''
Quick description of the file
'''
# =============================================================================
__author__ = 'Simon Lassourreuille'
__version__ = ''
__date__ = '16/10/2016'
__email__ = 'simon.lassourreuille@etu.u-bordeaux.fr'
__status__ = 'Prototype'
# =============================================================================
from backup.Mot import Mot

# =============================================================================
class UInt(Mot):

    def __init__(self, n):
        Mot.__init__(self, n)
        self.__max = 2^len(self) - 1
        self.__hexa = self.valeur

    # =========================================================================
    # Attributes with getter & setters

    # Maximum read only
    @property
    def Maximum(self):
        return self.__max

    # hexa read only
    @property
    def hexa(self):
        return self.__hexa

    # =========================================================================
    # Methods

    def __add__(self, pier):
        assert isinstance(pier, UInt), "Can't add two different types"
        assert self.nb_bytes == pier.nb_bytes, "Must be of same length"
        assert int(self.binaire,2)+int(pier.binaire,2) < self.Maximum, "Sum over max"
        new_int = UInt(self.nb_bytes)
        new_int.binaire = bin(int(self.binaire,2)+int(pier.binaire,2))[2:]
        return new_int

    def __mul__(self, pier):
        assert isinstance(pier, UInt), "Can't multiply two different types"
        assert self.nb_bytes == pier.nb_bytes, "Must be of same length"
        new_int = UInt(self.nb_bytes*2)
        new_int.binaire = bin(int(self.binaire, 2) * int(pier.binaire, 2))[2:]
        return new_int

    def __lt__(self, pier):
        assert isinstance(pier, UInt), "Can't compare two different types"
        assert self.nb_bytes == pier.nb_bytes, "Must be of same length"
        return {'10':False,'01':True,'00':False}[self.compare(pier)]

    # Temporary
    def __repr__(self):
        return str(int(self.binaire, 2))

if __name__ == '__main__':
    a = UInt(2)
    b = UInt(2)
    print('a : {}, b : {}, a < b : {}'.format(a,b,a<b))