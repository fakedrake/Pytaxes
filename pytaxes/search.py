"""This should parse a string and create keyword arguments for the
lookup. All return a list of strings except date and cost(int).

The search format is:

<domain> <space searated terms> [<domain> <terms> ...]

where <domain> can be 'date', 'id', 'cost', 'products'. Some variation
when it comes to search domain name may be tolerated. The id domain is
implied if none is porvided.

I am quite proud of date support. You can either have percise dates in
d/m/y form or just a year. You can also use 'to' or '-' or '->'
(surrounded by spaces) to get a date range (year or percice or
mixed). Dates are always expressed as tuples that represent inclusive
ranges. A year is from 1/1 to 31/12 and single dates are the same date
in both sides of the tuple."""

from datetime import date, datetime
from itertools import chain, izip_longest

class Parser(object):
    pairs = [ ('date', ['date', 'dates']),
              ('id', ['id', 'ids']),
              ('cost',['cost', 'costs']),
              ('products', ['product', 'products', 'service', 'services']),
              ('vendor', ['vendor', 'vendors']) ]
    rangers = ['to', '-', '->']

    def __init__(self, string, default_filler='id'):
        words = [i for i in string.split() if i != '']
        splitters = [i for i in chain(*[l for k, l in self.pairs])]
        self.data = {i:[] for i,x in self.pairs}
        self.errors = []

        filler = default_filler
        for w in words:
            if w in splitters:
                for k,s in self.pairs:
                    if w in s:
                        filler = k
                        break
            else:
                self.data[filler].append(w)

    def parse_date(self, string, upto=False):
        """Parse the date given by string. Return None on failure."""
        try:
            # If we have just a year
            if '/' not in string:
                if not upto:
                    return date(int(string),1,1)
                else:
                    return date(int(string),12,31)

            return datetime.strptime(string, "%d/%m/%Y").date()
        except ValueError:
            self.errors.append("Could not read date: %s (please use d/m/y format)" % string)
            return None


    def format_dates(self, wlist):
        """ We we go along turning things into tuples. with
        themselves. When we find a ranger we turn the next one into a
        tuple with None. Then we iterate the new list the other way
        and the none tuples we merge with the next tuple.
        """
        tmp = []
        merge = False
        for i in wlist:
            if i in self.rangers:
                merge = True
                continue

            s = self.parse_date(i, False)
            if s is None:
                continue

            e = self.parse_date(i, True)
            if e is None:
                continue

            if not merge:
                tmp.append((s, e))
            else:
                merge = False
                tmp[-1] = (tmp[-1][0], e)

        if merge:
            tmp[-1] = (tmp[-1][0], datetime.date.today())

        return tmp

    def __getitem__(self, key):
        if 'date' == key:
            return self.format_dates(self.data['date'])

        # XXX implement cost ranges
        if 'cost' == key:
            ret = []
            for i in self.data['cost']:
                try:
                    ret.append(float(i))
                except ValueError:
                    self.errors.append("Expected number for cost: %s" % i)
            return ret

        return self.data[key]

    def search(self, hash_table):
        """Actually search for stuff. Given a hash table this returns
        a list of cards that match the search terms. All search terms
        of the same are inclusive except products. All searches from
        different domains are exclusive.

        This means that searching for

        id aaa bbb vendor carefour xxxclub products lapdance tampons

        means that out of the cards aaa match the ones that have either
        carefour or xxxclub vendor and out of those match those that have
        bought both tampons and lapdance.
        """
        if not [i for i in chain(*self.data.values())]:
            return hash_table.lookup()

        results = []
        for d in ['id', 'vendor', 'date', 'cost']:
            tmp = set()
            for v in self[d]:
                tmp.update(set(hash_table.lookup(**{d:v})))

            results.append(tmp)

        results.append(set(self['products']))

        ret = results[0]
        for i in results:
            if i:
                if ret:
                    ret &= i
                else:
                    ret |= i

        return list(ret)
