import unittest
from ..search import Parser
from datetime import date

class TestSearchParser(unittest.TestCase):
    def test_plain_strings(self):
        parser = Parser("id aaa ooo vendor carefour")
        self.assertEquals(parser['id'], ['aaa', "ooo"])
        self.assertEquals(parser['vendor'], ['carefour'])

    def test_single_date(self):
        d = date(1991,7,22)
        parser = Parser("dates 22/7/1991")
        self.assertIn((d,d), parser['date'])

    def test_date_range(self):
        d1,d2 = date(1991,7,22), date(1991,8,22)
        parser = Parser("dates 22/7/1991 to 22/8/1991")
        self.assertIn((d1,d2), parser['date'])

    def test_mixed_dates_ranges_years(self):
        range = (date(1991,7,22), date(1991,8,22))
        d = (date(2010, 8, 6), date(2010, 8, 6))
        year = (date(2011, 1, 1), date(2011, 12, 31))
        parser = Parser("dates 22/7/1991 to 22/8/1991 6/8/2010 2011")
        self.assertIn(range, parser['date'])
        self.assertIn(d, parser['date'])
        self.assertIn(year, parser['date'])

    def test_date_error(self):
        range = (date(1991,7,22), date(1991,8,22))
        d = (date(2010, 8, 6), date(2010, 8, 6))
        year = (date(2011, 1, 1), date(2011, 12, 31))
        parser = Parser("dates 22/7/1991 to  hello world 22/8/1991   6/8/2010 2011")
        self.assertIn(range, parser['date'])
        self.assertIn(d, parser['date'])
        self.assertIn(year, parser['date'])
        self.assertIn("Could not read date: hello (please use d/m/y format)", parser.errors)

    def test_cost(self):
        parser = Parser("cost happy happy lillyday 34")
        self.assertIn(34, parser['cost'])
        self.assertIn("Expected number for cost: happy", parser.errors)

if __name__ == "__main__":
    unittest.main()
