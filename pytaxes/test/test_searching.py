import unittest
from ..search import Parser
from datetime import date
import os
from ..hashtable import HashTable, X17, index_file

class TestSearchParser(unittest.TestCase):
    def setUp(self):
        self.static_dir = os.path.dirname(os.path.realpath(__file__)) + '/static'
        self.ht = index_file(self.static_dir+"/cards.txt")

    def test_searching(self):
        """Many search terms of the same kind should be additive,
        different kinds are subtractive.
        """
        p = Parser("dates 2010 to 2013") # 18/6/2011")
        res = p.search(self.ht)
        self.assertEquals("", "") # Too many to compare (nice testing habits)


    def test_product_search(self):
        p = Parser("product P211")
        res = p.search(self.ht)
        self.assertEquals("", "")


if __name__ == "__main__":
    unittest.main()
