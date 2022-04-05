from bin_value import BinValue
import gmpy2


class OrBlock:
    data: int

    def __init__(self, binVal: BinValue = None, orBlock1 = None, orBlock2 = None, data: int = None):
        if binVal is not None:
            self.data = (1 << binVal.data)
            return
        if data is not None:
            self.data = data
            return
        if orBlock1 is None or orBlock2 is None:
            raise ValueError("arguments are None")
        self.data = orBlock1.data | orBlock2.data

    def make_set(self):
        pow = 0
        result = set()
        while (1 << pow) <= self.data:
            if (self.data >> pow) & 1 == 1:
                result.add(BinValue(data=pow))
            pow += 1
        return result

    def __mul__(self, other):
        data = 0
        for item1 in self.make_set():
            for item2 in other.make_set():
                value = item1 * item2
                data |= (1 << value.data)

        return OrBlock(data=data)

    def __hash__(self):
        return hash(self.data)

    def __eq__(self, other):
        return other.data == self.data

    def __str__(self):
        items = self.make_set()
        common = None
        for item in items:
            if common is None:
                common = item.data
            else:
                common &= item.data
        res = ""
        if common != 0:
            res = f"{str(BinValue(data=common))}"
        else:
            res = ""
        second = " + ".join([
            str(BinValue(data=(item.data ^ common))) for item in items
        ])
        if len(items) > 1:
            second = f"({second})"
        if second == "1" and res != "":
            return res
        elif res == "":
            return second
        return "(" + res + " * " + second + ")"
