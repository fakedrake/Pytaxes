#XXX: add statistics with sparsity, conflicts, size etc
from itertools import chain
from card import Card

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
            hash = (( hash * 17 ) + ( ord(id[0]) - ord(' ') )) % self.max_index;

        return hash

def double_size(hash, current_length):
    """Remember that this is to return the EXTRA size"""
    return current_length;


class HashTable(object):
    """The hash table. A card should be able to match a touple"""

    def __init__(self, initial_size=CARD_NUM, hash_function_class=SimpleHashFunction, allocator=double_size, duplicate_silence=True):
        self.infos = ["New hash table created"]
        self.warnings = []
        self.errors = []
        self.successes = []
        self.cards = [None]*initial_size
        self.hasher = hash_function_class(initial_size)
        self.allocator = allocator
        self.conflicts = 0
        self.content_size = 0
        self.slots = set()
        self.duplicate_silence = duplicate_silence

    def get_key(self, id):
        """Given an id get the slot where it should be or -1 if not found."""
        key = self.hasher(id)
        try:
            # On a card but not the correct one or on a deleted one
            while self.cards[key] and (self.cards[key] == "deleted" or self.cards[key].id != id):
                key += 1
        except IndexError:
            return -1

        # If we ended up on an empty slot
        if not self.cards[key]:
            return -1

        return key

    def get_card(self, id):
        """Get the card defined by id, if not found return None"""
        key = self.get_key(id)
        if key >= 0:
            return self.cards[key]

        return None

    def lookup(self, **kw):
        """Return a list of the resulting cards(including only the
        relevant purchases). IDs are searched fast but anything else
        requires iiteration."""
        # Attempt to find it quickly
        if 'id' in kw:
            ret = self.get_card(kw['id'])
            if ret:
                ret = [ret]
            else:
                ret = []
        else:
            ret = [self.cards[slot] for slot in self.slots]

        for i in kw.iteritems():
            ret = filter(lambda x: x, [c.matches(i) for c in ret])

        if not ret:
            self.infos.append("No cards match your search.")

        return ret

    def insert(self, card, log=True):
        """Insert a purchase"""
        i = 0
        # Initial hash
        hash = self.hasher(card.id)
        self.content_size += 1

        # Find an empty space
        try:
            if self.cards[hash] and self.cards[hash] != "deleted":
                self.conflicts += 1
                while self.cards[hash] != "deleted" and self.cards[hash]:
                    if self.cards[hash].id == card.id:
                        self.cards[hash].purchase(card)
                        return
                    # i+=1
                    # hash += i**2
                    hash += 1

        except IndexError:
            # Out of bounds
            while hash >= len(self.cards):
                self.cards += [None]*self.allocator(hash, len(self.cards))
                if log:
                    self.warnings.append("Extending hash table")

        # Now we know where to put it
        if log:
            self.successes.append("Card %s added, conflicted %d times" % (card.id, i))

        self.slots.add(hash)
        self.cards[hash] = card

    def delete(self, id):
        """Delete card defined by id"""
        slot = self.get_key(id)
        if slot < 0:
            self.errors.append("Attempt to remove card %s failed: no such card." % id)
            return

        self.successes.append("Successfully removed card %s." % id)
        self.slots.remove(slot)
        self.cards[slot] = "deleted"

    def extract_messages(self):
        """Returns a dict of the messages in the stack and clears the
        stack
        """
        ret = dict(errors=self.errors,
                    warnings=self.warnings,
                    infos=self.infos,
                    successes=self.successes)
        self.infos = []
        self.warnings = []
        self.errors = []
        self.successes = []
        return ret



def index_file(filename, input_file=None, duplicate_silence=True):
    """This is a wrapper to index a file 'optimally'. Note that this
    ignores the number at the top and indexes everything it can get
    it's hands on.
    """
    if input_file is None:
        input_file = open(filename)

    lines = input_file.readlines()
    ht = HashTable(hash_function_class=X17, initial_size=len(lines) * 2, duplicate_silence=duplicate_silence)
    for n,l in enumerate(lines):
        if ';' in l:
            ht.insert(Card(l), False)
        else:
            ht.warnings.append("Ignoring line %d as it didnt seem to have a ';'" % n)

    ht.successes.append("Imported file %s!" % filename)
    return ht

if __name__ == "__main__":
    from card import Card
    ht = HashTable(hash_function_class = X17)
    ht.insert(Card("bbaa100aajkcbsvbssbsbv888;2011;167;78.23;67897491;P234;P345;S234"))
