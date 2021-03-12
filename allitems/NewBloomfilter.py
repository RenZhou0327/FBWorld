# -*- coding: utf8 -*-#

import math
class Bitarray:
    def __init__(self, size):
        """ Create a bit array of a specific size """
        self.size = size
        self.bitarray = bytearray(int(math.ceil(size / 8.0)))

    def set(self, n):
        """ Sets the nth element of the bitarray """

        index = n / 8
        position = n % 8
        self.bitarray[index] = self.bitarray[index] | 1 << (7 - position)

    def get(self, n):
        """ Gets the nth element of the bitarray """

        index = n / 8
        position = n % 8
        return (self.bitarray[index] & (1 << (7 - position))) > 0




class NewBloomFilter:
    def __init__(self, size):
        self.size = size
        self.bitmap = Bitarray(size)

    def __BDKRHash(self, key):
        seeds = [31,131,1313,13131,131313,1313131,13131313,131313131,1313131313,13131313131]
        hashnumbers = []
        for seed in seeds:
            hash = 0
            for i in range(len(key)):
                hash = (hash * seed) + ord(key[i])
            hashnumbers.append(hash % self.size)
        return hashnumbers

    def bloomset(self, key):
        bloomtable = self.__BDKRHash(key)
        for i in bloomtable:
            self.bitmap.set(i)

    def bloomget(self, key):
        bloomtable = self.__BDKRHash(key)
        for i in bloomtable:
            if self.bitmap.get(i) == False:
                return False
        return True

