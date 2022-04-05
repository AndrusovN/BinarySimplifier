import unittest
import random
from parsing import parse
from variable_names import VariableNamesHolder
from typing import List
from statistics_manager import StatisticsManager


def generate_random_test(variables: List[str], size: int) -> str:
    blocks_count = 2
    left_size = size - blocks_count
    operators = [" + ", " * ", " ^ "]
    result = ""
    for i in range(blocks_count):
        left_size += 1
        current_size = random.randint(1, left_size)
        if i == blocks_count - 1:
            current_size = left_size
        block = ""
        if current_size == 1:
            block = random.choice(variables)
        else:
            block = "(" + generate_random_test(variables, current_size) + ")"
        if i != 0:
            result += random.choice(operators)
        if random.randint(0, 2) > 0:
            result += f"(!{block})"
        else:
            result += block
        left_size -= current_size
    return result


def make_test_method(sample: str, variables_count: int):
    def test(self):
        result = parse(sample)
        result_text = str(result)
        self.assertTrue(result is not None)
        operations_count_sample = sample.count("!") + sample.count("+") + sample.count("*") + sample.count("^")
        operations_count_result = result_text.count("!") + result_text.count("+") \
              + result_text.count("*") + result_text.count("^")

        StatisticsManager().add_case(variables_count, operations_count_sample + 1, operations_count_result + 1)

        self.assertTrue(operations_count_result <= operations_count_sample,
                        f"Result is larger than sample!\nSample: '{sample}'\nResult: '{result_text}'")
        result1 = parse(result_text)
        self.assertEqual(result1, result,
                         f"Result is not the same!:\nFirst: '{result_text}'\nSecond: '{str(result1)}'")
    return test


def check_sample_variables(letters: List[str], sample: str):
    for item in letters:
        if sample.find(item) == -1:
            return False
    return True


def generate_sample(letters_count: int) -> str:
    assert letters_count < 26
    size = random.randint(letters_count + 2, 20)
    letters = [chr(ord('a') + i) for i in range(letters_count)]
    sample = generate_random_test(letters, size)
    while not check_sample_variables(letters, sample):
        sample = generate_random_test(letters, size)
    return sample


def build_random_cases(seed: int, count: int, max_variables: int):
    random.seed(seed)
    functions = {}
    for vars_count in range(1, max_variables + 1):
        for i in range(count):
            name = f"test_random_case_{vars_count}_vars_id_{i + 1}"
            sample = generate_sample(vars_count)
            functions[name] = make_test_method(sample, vars_count)
    return type("RandomTestCase", (unittest.TestCase,), functions)


if __name__ == '__main__':
    VariableNamesHolder([])
    test_case = build_random_cases(1791791791, 1024, 6)
    print(test_case)
    print("Tests generated")
    unittest.main(exit=False)
    StatisticsManager().print_statistics()
