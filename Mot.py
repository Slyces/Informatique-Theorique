# =============================================================================
"""
Class Mot for the << DM Info Théorique >>
"""
# =============================================================================
__author__ = 'Simon Lassourreuille'
__version__ = ''
__date__ = '21/10/2016'
__email__ = 'simon.lassourreuille@etu.u-bordeaux.fr'
__status__ = 'Prototype'

# =============================================================================
# Imports
from random import randrange as rr


# =============================================================================

class Mot(object):
    def __init__(self, n: int) -> 'Mot':
        """
        Returns a word of n bytes initialised at a random value
        The parameter n must be positive and not null

        :param n: number of bytes of the word
        :type n: int
        :return: Mot or Error
        """
        if type(n) != int or n <= 0:
            raise TypeError('Wrong type for n')

        # Init of nb_bytes
        self.__nb_bytes = n
        self.__binaire = ''
        self.__valeur = ''

        # Init of binary repr, using the binaire setter
        binaire = ''
        for i in range(n * 8):
            binaire += str(rr(2))
        self.binaire = binaire

    # =========================================================================
    # Getters and setters

    # nbBytes read only
    @property
    def nb_bytes(self) -> int:
        """
        Getter for the read-only nb_bytes
        ---> which is initialised in the constructor

        :return: int

        :Example:
        >>> A = Mot(2)
        >>> A.nb_bytes
        2
        """
        return self.__nb_bytes

    # binaire read/write
    @property
    def binaire(self) -> str:
        """
            Getter for binaire, a binary representation of the Word
            :return: str
        """
        return self.__binaire

    @binaire.setter
    def binaire(self, string: str) -> None:
        """@To-Do
        Setter for binaire with restrictions :
        :param string: new value of the word's n bytes
        :type string: str
        :return: None | Error

        string for a word A must have a length equal to len(A)
        string can only be composed of '1' & '0'

        :Example:
        >>> A = Mot(2)
        >>> A.binaire = '1010101001010101'
        >>> A.binaire
        '1010101001010101'
        """
        if len(string) != len(self) or type(string) != str:
            raise TypeError("Wrong type or length for string")
        for char in string:
            if char != '0' and char != '1':
                raise TypeError("String must be composed of 0 & 1 only")
        self.__binaire = string
        # New binary : new hexadecimal too !
        # Init of the hexadecimal value
        self.__valeur = ''
        for i in range(0, len(self), 4):
            # Slicing the binary word in slices of 4 bits
            string = self.binaire[i:i + 4]
            n = 0
            for j in range(4):
                n += int(string[j]) * [8, 4, 2, 1][j]
            self.__valeur += ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B',
                              'C', 'D', 'E', 'F'][n]

    # valeur read only
    @property
    def valeur(self) -> int:
        """
        Getter for valeur, an hexadecimal representation of the Word
        :return: str
        """
        return self.__valeur

    # =========================================================================
    # Methods
    def __len__(self) -> int:
        """
        Return the length of the binary representation of this word
            number of bits
        :return: int
        """
        return 8 * self.nb_bytes

    def __rshift__(self, n: int) -> 'Mot':
        """
        Shifts a Word by n bits to the right
        :param n: number of bits shifted
        :type n: int
        :return: Mot

        :Example:
        >>> a = Mot(1)
        >>> a.binaire = '10110000'
        >>> a >>= 2
        >>> a.binaire
        '00101100'
        """
        if type(n) != int or n < 0:
            raise TypeError('Wrong type for n')
        if n > len(self):
            n = len(self)
        if n == 0:
            return self

        H = self.__class__(self.nb_bytes)
        H.binaire = '0' * n + self.binaire[:-n]
        return H

    def __lshift__(self, n: int) -> 'Mot':
        """
        Shifts a Word by n bits to the left
        :param n: number of bits shifted
        :return: Mot

        :Example:
        >>> a = Mot(1)
        >>> a.binaire = '00101100'
        >>> a <<= 4
        >>> a.binaire
        '11000000'
        """
        if type(n) != int or n < 0:
            raise TypeError('Wrong type for n')
        if n > len(self):
            n = len(self)
        if n == 0:
            return self

        H = self.__class__(self.nb_bytes)
        H.binaire = self.binaire[n:] + '0' * n
        return H

    def complement(self) -> 'Mot':
        """
        Does a complement to 1, inverting 0 to 1 and 1 to 0
        :return: Mot

        :Example:
        >>> a = Mot(1) ; a.binaire = '10110000'
        >>> a = a.complement()
        >>> a.binaire
        '01001111'
        """
        # Returns a new Mot
        H = self.__class__(self.nb_bytes)
        complement = ''
        for char in self.binaire:
            if char == '0':
                complement += '1'
            else:
                complement += '0'
        H.binaire = complement
        return H

    def compare(self, other: 'Mot') -> str:
        """
        Compare 2 words of same length bit to bit from left to right
        return the first difference found with this syntax :
        'ab' where a is the bite of this word and b the bite of the other
        if there is no difference, return '00'

        :param other: Word to compare to
        :type other: Mot
        :return: str | Error
            -> '10' or '01' or '00'

        :Example:
        >>> a = Mot(1) ; b = Mot(1) ; c = Mot(1)
        >>> a.binaire = '10110000'
        >>> b.binaire = '10011111'
        >>> c.binaire = '11000000'
        >>> a.compare(b)
        '10'
        >>> b.compare(a)
        '01'
        >>> a.compare(c)
        '01'
        >>> a.compare(a)
        '00'
        """
        if type(other) != self.__class__ or len(self) != len(other):
            raise TypeError("Other must be of same class and length")
        for i in range(len(self)):
            if self.binaire[i] != other.binaire[i]:
                return self.binaire[i] + other.binaire[i]
        return '00'

    def extend(self, N: int) -> 'Mot':
        """
        With n the number of bytes of this Word
        Return a Word of max(n, N, 1)bytes, filled with 0 to the left if needed
        :param N: number of bytes to extend to if possible
        :type N: int
        :return: Mot

        :Example:
        >>> a = Mot(1)
        >>> a.nb_bytes
        1
        >>> a = a.extend(9)
        >>> a.nb_bytes
        9
        >>> b = a.extend(4) # 4 is inferior to the actual number of bytes of a
        >>> b.nb_bytes
        9
        """
        if type(N) != int:
            raise TypeError("N must be an int")
        # Extending to something lower than nb_bytes has no effect
        if N <= self.nb_bytes:
            return self
        H = self.__class__(N)
        H.binaire = '00000000' * (N - self.nb_bytes) + self.binaire
        return H

    def reduce(self, N: int) -> 'Mot':
        """
        With n the number of bytes of this Word
        Return a Word of max(1, min(n,N)) bytes, loosing the right part if needed
        :param N: number of bytes to reduce to if possible
        :type N: int
        :return: Mot

        :Example:
        >>> a = Mot(4)
        >>> a.nb_bytes
        4
        >>> b = a.reduce(1)
        >>> b.nb_bytes
        1
        """
        if type(N) != int:
            raise TypeError("N must be an int")
        # Reducing to something greater than nb_bytes has no effect
        if N >= self.nb_bytes:
            return self
        H = self.__class__(max(N, 1))
        H.binaire = self.binaire[:len(H)]
        return H

    def cast(self, N: int) -> 'Mot':
        """
        Smart extending / reducing according to the parameter
        With n the number of bytes of this Word,
        if N >= n : extend to N
        if N < n : reduce to N
        :param N: number of bytes to extend to / reduce to
        :type N: int
        :return: Mot
        """
        if type(N) != int:
            raise TypeError("Wrong type for N")
        if N >= self.nb_bytes:
            return self.extend(N)
        else:
            return self.reduce(N)

    def relativExtension(self, N: int) -> 'Mot':
        """
        With n the number of bytes of this word
        Extend or reduce this word depending on N's sign
        if N is positive, add N bytes to the word (extend to n + N)
        if N is strictly negative, remove N bytes (reduce to n - N)
            --> can not reduce below 1
        :param N: number of bytes to add or remove
        :type N: int
        :return: Mot

        :Example:
        >>> a = Mot(3)
        >>> a.binaire = '101110100110011000001101'
        >>> a = a.relativExtension(-1)
        >>> a.binaire
        '1011101001100110'
        >>> a = a.relativExtension(2)
        >>> a.binaire
        '00000000000000001011101001100110'
        >>> a = a.relativExtension(-8)
        >>> a.binaire
        '00000000'
        """
        if type(N) != int:
            raise TypeError("Wrong type for N")
        if N >= 0:
            return self.extend(self.nb_bytes + N)
        else:
            return self.reduce(self.nb_bytes + N)

    def __eq__(self, other: 'Mot') -> bool:
        """
        Defined if both Word are of same length
        return True if they have the same binary representation
        return False otherwise

        :param other: Word to compare to
        :type other: Mot
        :return: bool | Error
        """
        if type(other) != self.__class__ or len(self) != len(other):
            raise TypeError('Wrong type or length for other')
        return self.compare(other) == '00'

    # INUTILE
    def __repr__(self) -> str:
        """
        Encodes the representation of the object Mot
        :return: str
        """
        representation = '\u2553'
        for i in range(len(self.binaire)):
            representation += '\u2500' * 3
            if i % 8 == 7:
                representation += '\u2556 \u2553'
            else:
                representation += '\u252C'
        representation = representation[:-2] + '\n' + '\u2551'
        for i in range(len(self.binaire)):
            representation += ' ' + self.binaire[i] + ' '
            if i % 8 == 7:
                representation += '\u2551 \u2551'
            else:
                representation += "\u2502"
        representation = representation[:-2] + '\n\u2559'
        for i in range(len(self.binaire)):
            representation += '\u2500' * 3
            if i % 8 == 7:
                representation += '\u255C \u2559'
            else:
                representation += '\u2534'
        return representation[:-2]


if __name__ == '__main__':
    import doctest

    print("Testing the doc examples")
    doctest.testmod()
    print("Testings done")
    M = Mot(4)
    M.binaire = '01001100010010101001100111000101'
    print(M)

    print(M.relativExtension(1))
    print(M.relativExtension(-1))
