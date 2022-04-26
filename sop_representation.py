from zhegalkins_polynom import ZhegalkinsPolynom
from and_block import AndBlock
from variable_names import VariableNamesHolder
from hashable_set import HashableSet


class SOPRepresentation:
    blocks: set

    def __init__(self, polynom: ZhegalkinsPolynom):
        self.blocks = set()
        totalOnes = HashableSet((1 << VariableNamesHolder().get_count()) - 1)
        for i in range(1 << VariableNamesHolder().get_count()):
            values = HashableSet(i)
            if polynom(bitmask=values):
                self.blocks.add(AndBlock(values, totalOnes ^ values))

    def __str__(self):
        result = ""
        for item in self.blocks:
            if len(result) > 0:
                result += " + "
            result += str(item)
        return result

    def simplify(self):
        result_blocks = set()
        for block1 in self.blocks:
            found = False
            for block2 in self.blocks:
                result = block2.try_match(block1)
                if result is not None:
                    result_blocks.add(AndBlock(result[0], result[1]))
                    found = True
                    break
            if not found:
                result_blocks.add(block1)
        success = len(result_blocks) < len(self.blocks)
        self.blocks = result_blocks
        return success

    def remove_useless(self):
        result_blocks = set()
        for block1 in self.blocks:
            found = False
            for block2 in self.blocks:
                if block2 == block1:
                    continue
                if block1.is_subset(block2):
                    found = True
                    break
            if not found:
                result_blocks.add(block1)
        self.blocks = result_blocks

    def simplify_maximum(self):
        success = self.simplify()
        while success:
            success = self.simplify()
        self.remove_useless()
