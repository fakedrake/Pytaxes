import unittest
import os
from ..hashtable import HashTable, X17, index_file
from ..card import Card
from ..search import Parser

class TestHashTable(unittest.TestCase):
    def setUp(self):
        self.static_dir = os.path.dirname(os.path.realpath(__file__)) + '/static'

    def test_add_card(self):
        self.hash_table = HashTable(hash_function_class=X17)
        self.hash_table.insert(Card("bbaa100aajkcbsvbssbsbv888;2011;167;78.23;67897491;P234;P345;S234"))
        self.assertEquals(self.hash_table.lookup(id="bbaa100aajkcbsvbssbsbv888")[0]['id'], "bbaa100aajkcbsvbssbsbv888")

    def add_file(self):
        ht = index_file(self.static_dir+"/cards1.txt")
        self.assertEquals("abctvj32131kljatefmljk364", ht.lookup(id="abctvj32131kljatefmljk364")[0]['id'])

    def test_simple_search(self):
        ht = index_file(self.static_dir + "/search_test.txt")
        parse = Parser("vendor carfour aplha products money server")
        cards = parse.search(ht)
        for c in cards:
            self.assertIn(c['vendor'], ['carfour', 'alpha'])
            self.assertIn('money', c['products'])

    def test_delete(self):
        ht = index_file(self.static_dir + "/search_test.txt")
        ht.delete("abctvj22202kljatefkkll363")
        ht.delete("nonexistent")
        self.assertEquals([], ht.lookup(id="abctvj22202kljatefkkll363"))

if __name__ == "__main__":
    unittest.main()
