import unittest
import os
from ..hashtable import HashTable, X17
from ..card import Card

class TestHashTable(unittest.TestCase):
    def test_add_card(self):
        self.hash_table = HashTable(hash_function_class=X17)
        self.hash_table.insert(Card("bbaa100aajkcbsvbssbsbv888;2011;167;78.23;67897491;P234;P345;S234"))
        self.assertEquals(self.hash_table.lookup(id="bbaa100aajkcbsvbssbsbv888")[0]['id'], "bbaa100aajkcbsvbssbsbv888")

    def test_add_file(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, "static/cards.txt")

        f = open(filename).readlines()
        self.hash_table = HashTable(hash_function_class=X17, initial_size=len(f) * 2)
        for l in f:
            if ';' in l:
                self.hash_table.insert(Card(l))


if __name__ == "__main__":
    unittest.main()
