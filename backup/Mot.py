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
# Imports
from random import randrange as rr

# =============================================================================
class Mot(object):
    '''
    Mot est un mot binaire de n caractères
    '''

    def __init__(self, n):
        assert isinstance(n, int) and n > 0, "nbBytes setting error"

        self.__nbBytes = n
        self.__binaire = ''.join([str(rr(2)) for i in range(n*8)])

    # =========================================================================
    # Getters and setters

    # nbBytes read only
    @property
    def nb_bytes(self):
        return self.__nbBytes

    # binaire read/write
    @property
    def binaire(self):
        return self.__binaire

    @binaire.setter
    def binaire(self, string):
        """
        binaire setter :
        """
        assert isinstance(string, str), "binaire must be set to str"
        assert [char in ('0','1') for char in string], "binaire must be composed of 0 & 1"
        assert len(string) == len(self), "binaire length must be nbBytes"
        self.__binaire = string
    
    # valeur read only
    @property
    def valeur(self):
        return hex(int(self.binaire, 2))[2:]

    # =========================================================================
    # Methods

    def __len__(self):
        return len(self.binaire)

    def __lshift__(self, n):
        assert isinstance(n, int) and n > 0, "n must be an int superior to 0"

        return self.binaire[n:] + n*'0'

    def __rshift__(self, n):
        """
        This functions shifts n bits to the right
        :param n: number of bits to shift to the right
        :type n: int
        :return: Mot

        :Example:
        >>> M = Mot(2) # 2 bytes long word
        >>> M.binaire = "1111000011110000"
        >>> M >> 2
        '0011110000111100'
        """
        assert isinstance(n, int) and n > 0, "n must be an int superior to 0"
        return n*'0' + self.binaire[:-n]

    def complement(self):
        return ''.join([('1','0')[int(char)] for char in self.binaire])

    def compare(self, pier):
        assert isinstance(pier, Mot) and len(pier)==len(self), "must compare 2 Words of same length"
        for i in range(len(self)):
            if self.binaire[i] != pier.binaire[i] :
                return self.binaire[i] + pier.binaire[i]
        return '00'

    def extend(self, k):
        assert isinstance(k, int), "k must be an integer"
        word = Mot(max(k,self.nb_bytes,1))
        word.binaire = (len(word)-len(self))*'0' + self.binaire
        return word

    def reduce(self, k):
        assert isinstance(k, int), "k must be an integer"
        word = Mot(max(1, min(k, self.nb_bytes)))
        word.binaire = self.binaire[:len(word)]
        return word

    def cast(self, k):
        assert isinstance(k, int), "k must be an integer"
        if k >= self.nb_bytes : return self.extend(k)
        else : return self.reduce(k)

    def relativeExtension(self, k):
        assert isinstance(k, int), "k must be an integer"
        if k >= 0 : return self.extend(k+p)
        else : return self.reduce(k+p)



if __name__ == '__main__' :
    a,b,c = Mot(1),Mot(1),Mot(1)
    a.binaire = '10110000'
    b.binaire = '10011111'
    c.binaire = '11000000'

    print(a.compare(b))
    print(a.compare(c))
    print(a.compare(a))

    k = Mot(2)
    print('k :',k.binaire)
    h = k.extend(4)
    print('len h:',len(h))
    print('len k :',len(k))
    print('k.extend(2):',h.binaire)

    k = Mot(4)
    print('k:',k.binaire)
    l = k.reduce(2)
    print('l:', l.binaire)

    print('=============================')
    import doctest
    doctest.testmod()

