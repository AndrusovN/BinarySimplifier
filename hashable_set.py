import gmpy2


# Realizes a bitset to contain a hashable set of integers
class HashableSet:
    data: int

    def __init__(self, data=0, values=None):
        self.data = data
        if values is not None:
            for item in values:
                self.data |= (1 << item)

    def __contains__(self, item: int):
        return bool((self.data >> item) & 1)

    def __or__(self, other):
        return HashableSet(self.data | other.data)

    def __hash__(self):
        return hash(self.data)

    def __and__(self, other):
        return HashableSet(self.data & other.data)

    def __len__(self):
        return gmpy2.popcount(self.data)

    def __getattr__(self, item: int):
        return (self.data >> item) & 1

    def __eq__(self, other):
        return self.data == other.data

    def __setitem__(self, key, value):
        if value == 1:
            self.data |= 1 << key
        else:
            if self[key] == 1:
                self.data ^= 1 << key

    def __iter__(self):
        current_value = self.data
        step = 0
        while current_value > 0:
            if current_value & 1 == 1:
                yield step
            current_value //= 2
            step += 1