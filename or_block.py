from bin_value import BinValue
import gmpy2


# A block of values like a OR b OR c etc...
class OrBlock:
    # it is a bit mask of monoms, included in this block
    # so if monom with id i is included to block, then (OrBlock.data >> i) & 1 is equal 1
    data: int

    # initialization of OrBlock
    # binVal - the single binary value to initialize block - then the whole block is equal just to one this monom
    # data - the direct value of data field to initialize it
    def __init__(self, binVal: BinValue = None, data: int = None):
        if binVal is not None:
            self.data = (1 << binVal.data)
            return
        if data is not None:
            self.data = data
            return
        else:
            raise ValueError("either data or binVal argument should be not None")

    # returns the set of BinValue monoms included in this OR block
    def make_set(self):
        pow = 0
        result = set()
        while (1 << pow) <= self.data:
            if (self.data >> pow) & 1 == 1:
                result.add(BinValue(data=pow))
            pow += 1
        return result

    # The product (operator AND) of two OR blocks
    # So it's like (a OR b OR c) AND (d OR e OR f) === (ad OR ae OR af OR bd OR be OR bf OR cd OR ce OR cf)
    def __mul__(self, other):
        data = 0
        for item1 in self.make_set():
            for item2 in other.make_set():
                value = item1 * item2
                data |= (1 << value.data)

        return OrBlock(data=data)

    def __or__(self, other):
        return OrBlock(data=(self.data | other.data))

    def __hash__(self):
        return hash(self.data)

    def __eq__(self, other):
        return other.data == self.data

    # make string from OrBlock
    def __str__(self):
        items = self.make_set()
        # Firstly find common dividers of all monoms, so the block will look as (a*b*c*d*(e + f + g + h))
        common = None
        for item in items:
            if common is None:
                common = item.data
            else:
                common &= item.data
        res = ""
        # if common is not zero, create the common monom as other bracket
        if common != 0:
            res = f"{str(BinValue(data=common))}"
        else:
            res = ""
        # generate the second bracket
        second = " + ".join([
            str(BinValue(data=(item.data ^ common))) for item in items
        ])
        # if there're many BinValues, unite them into bracket
        if len(items) > 1:
            second = f"({second})"
        # if the second bracket is only single 1, return just the common part
        if second == "1" and res != "":
            return res
        elif res == "":
            return second
        return "(" + res + " * " + second + ")"
