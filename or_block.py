from bin_value import BinValue
import gmpy2
from hashable_set import HashableSet


# A block of values like a OR b OR c etc...
class OrBlock:
    # it is a bit mask of monoms, included in this block
    # so if monom with id i is included to block, then (OrBlock.data >> i) & 1 is equal 1
    monoms_set: HashableSet

    # initialization of OrBlock
    # binVal - the single binary value to initialize block - then the whole block is equal just to one this monom
    # data - the direct value of data field to initialize it
    def __init__(self, binVal: BinValue = None, data: HashableSet = None):
        if binVal is not None:
            self.monoms_set = HashableSet(values={binVal.monom.data})
            return
        if data is not None:
            self.monoms_set = data
            return
        else:
            raise ValueError("either data or binVal argument should be not None")

    # The product (operator AND) of two OR blocks
    # So it's like (a OR b OR c) AND (d OR e OR f) === (ad OR ae OR af OR bd OR be OR bf OR cd OR ce OR cf)
    def __mul__(self, other):
        data = HashableSet()
        for item1 in self.monoms_set:
            for item2 in other.monoms_set:
                value = BinValue(data=HashableSet(data=item1)) * BinValue(data=HashableSet(data=item2))
                data[value.monom.data] = 1

        return OrBlock(data=data)

    def __or__(self, other):
        return OrBlock(data=(self.monoms_set | other.monoms_set))

    def __hash__(self):
        return hash(self.monoms_set)

    def __eq__(self, other):
        return other.monoms_set == self.monoms_set

    # make string from OrBlock
    def __str__(self):
        # Firstly find common dividers of all monoms, so the block will look as (a*b*c*d*(e + f + g + h))
        common = None
        for item in self.monoms_set:
            if common is None:
                common = BinValue(data=HashableSet(item)).monom
            else:
                common &= BinValue(data=HashableSet(item)).monom
        res = ""
        # if common is not zero, create the common monom as other bracket
        if common != HashableSet(data=0):
            res = f"{str(BinValue(data=common))}"
        else:
            res = ""
        # generate the second bracket
        second = " + ".join([
            str(BinValue(data=HashableSet(data=(item ^ common.data)))) for item in self.monoms_set
        ])
        # if there're many BinValues, unite them into bracket
        if len(self.monoms_set) > 1:
            second = f"({second})"
        # if the second bracket is only single 1, return just the common part
        if second == "1" and res != "":
            return res
        elif res == "":
            return second
        return "(" + res + " * " + second + ")"
