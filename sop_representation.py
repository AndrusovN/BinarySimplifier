from zhegalkins_polynom import ZhegalkinsPolynom
from and_block import AndBlock
from variable_names import VariableNamesHolder
from hashable_set import HashableSet
from or_block import OrBlock


class SOPRepresentation:
    blocks: set

    def __init__(self, polynom: ZhegalkinsPolynom, blocks: set = None):
        if blocks is not None:
            self.blocks = blocks
            return
        self.blocks = set()
        totalOnes = HashableSet((1 << VariableNamesHolder().get_count()) - 1)
        for i in range(1 << VariableNamesHolder().get_count()):
            values = HashableSet(i)
            if polynom(bitmask=values):
                self.blocks.add(AndBlock(values, totalOnes ^ values))

    def __str__(self):
        max_id = (-1, False)
        max_set = {-1}
        for var_id in range(len(VariableNamesHolder().variable_names)):
            positive_items = set()
            negative_items = set()
            for block in self.blocks:
                if block.contains(var_id, False):
                    positive_items.add(block)
                if block.contains(var_id, True):
                    negative_items.add(block)
            if len(positive_items) > len(max_set):
                max_set = positive_items
                max_id = var_id, True
            if len(negative_items) > len(max_set):
                max_set = negative_items
                max_id = var_id, False
        if max_id == (-1, False):
            result = ""
            for item in self.blocks:
                if len(result) > 0:
                    result += " + "
                result += str(item)
            return result

        united_blocks = {block.deepcopy().remove_variable(max_id[0], not max_id[1]) for block in max_set}
        united_blocks_sop = SOPRepresentation(None, blocks=united_blocks)
        result = f"{'!' if not max_id[1] else ''}{VariableNamesHolder().get_variable_name(max_id[0])} * ({str(united_blocks_sop)})"

        left_blocks = {block if block not in max_set else None for block in self.blocks}
        left_blocks.remove(None)

        if len(left_blocks) > 0:
            left_blocks_sop = SOPRepresentation(None, blocks=left_blocks)
            result += " + "
            result += str(left_blocks_sop)

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

    def to_or_block(self):
        if len(self.blocks) == 0:
            raise Exception("Empty SOP cannot be converted to a OrBlock")
        for item in self.blocks:
            pass

