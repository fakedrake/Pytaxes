#XXX: add statistics with sparsity, conflicts, size etc
CARD_NUM = 200000

class SimpleHashFunction(object):
    def __init__(self, max_index=CARD_NUM):
        self.max_index = max_index

    def __call__(self, id, len=None):
        if len is None:
            len = self.max_index
        hash = 0
        for i in id:
            hash += ord(i)
            hash += (hash << 10)%len
            hash %= len
            hash ^= (hash >> 6)

        hash += (hash << 3)%len
        hash ^= (hash >> 11)
        hash += (hash << 15) %len

        return hash %len

class X17 (object):
    def __init__(self, max_index=CARD_NUM):
        self.max_index = max_index

    def __call__(self, id, max=None):
        if max is None:
            max = self.max_index

        hash = len(id)
        while len(id)>1:
            hash = ( ( ( ( hash * 17 ) + ( ord(id[0]) - ord(' ') ) ) * 17 ) + ( ord(id[1]) - ord(' ') ) ) % self.max_index
            id = id[2:]

        if len == 1:
            hash = (( hash * 17 ) + ( ord(key[0]) - ord(' ') )) % self.max_index;

        return hash

def double_size(hash, current_length):
    """Remember that this is to return the EXTRA size"""
    return current_length;


class HashTable(object):
    """The hash table. A card should be able to match a touple"""

    def __init__(self, initial_size=CARD_NUM, hash_function_class=SimpleHashFunction, allocator=double_size):
        self.cards = [None]*initial_size
        self.hasher = hash_function_class(initial_size)
        self.allocator = allocator
        self.conflicts = 0
        self.content_size = 0

    def get_card(self, id):
        key = self.hasher(id)
        try:
            # On a card but not the correct one
            while self.cards[key] and self.cards[key]['id'] != id:
                key += 1
        except IndexError:
            return None

        if not self.cards[key]:
            return None

        return self.cards[key]

    def lookup(self, **kw):
        """Return a list of the results."""
        if 'id' in kw:
            ret = self.get_card(kw['id'])
            if ret:
                ret = [ret]
        else:
            ret = [card for card in self.cards if card is not None]

        for i in kw.iteritems():
            ret = [card for card in ret if card.matches(i)]

        return ret

    def insert(self, card):
        """Insert a card"""
        hash = self.hasher(card['id'])
        self.content_size += 1
        try:
            if self.cards[hash]:
                self.conflicts += 1
                while self.cards[hash]:
                    hash += 1
        except IndexError:
            while hash >= len(self.cards):
                self.cards += [None]*self.allocator(hash, len(self.cards))

        self.cards[hash] = card

def index_file(filename):
    """This is a wrapper to index a file 'optimally'. Note that this
    ignores the number at the top and indexes everything it can get
    it's hands on.
    """
    from card import Card
    lines = open(filename).readlines()
    ht = HashTable(hash_function_class=X17, initial_size=len(lines) * 2)
    for l in lines:
        if ';' in l:
            ht.insert(Card(l))

    return ht

if __name__ == "__main__":
    from card import Card
    ht = HashTable(hash_function_class = X17)
    ht.insert(Card("bbaa100aajkcbsvbssbsbv888;2011;167;78.23;67897491;P234;P345;S234"))
