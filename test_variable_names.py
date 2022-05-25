import unittest
from variable_names import VariableNamesHolder
from variable import Variable


class VariablesNamesTestCase(unittest.TestCase):
    def setUp(self) -> None:
        VariableNamesHolder()

    def tearDown(self) -> None:
        VariableNamesHolder().clear()

    def testBeforeNoVariables(self):
        self.assertEqual(VariableNamesHolder().get_number_of_variables(), 0,
                         "Nothing happened, but variables count is not 0")

    def testAddVariable(self):
        old_variables_count = VariableNamesHolder().get_number_of_variables()

        new_created_variable = Variable("myTestVariable")
        VariableNamesHolder().register_variable(new_created_variable)

        new_variables_count = VariableNamesHolder().get_number_of_variables()
        self.assertEqual(old_variables_count + 1, new_variables_count,
                         "Variables count is not correct after variable had been added")
        self.assertTrue(VariableNamesHolder().is_variable_registered("myTestVariable"))

        try:
            new_variable_index = VariableNamesHolder().get_variable_index("myTestVariable")
            stored_variable = VariableNamesHolder().get_variable(new_variable_index)
            self.assertEqual(stored_variable, new_created_variable)

        except Exception as e:
            self.fail("VariableNamesHolder().get_variable_index() raised an exception: " + str(e))

    def testAddMoreVariables(self):
        first_created_variable = Variable("yetAnotherVariable")
        VariableNamesHolder().register_variable(first_created_variable)

        second_created_variable = Variable("yetAnotherVariable")
        VariableNamesHolder().register_variable(second_created_variable)

        self.assertNotEqual(second_created_variable.id, first_created_variable.id)
        self.assertNotEqual(second_created_variable.id, -1)
        self.assertNotEqual(first_created_variable.id, -1)

    def testClear(self):
        new_created_variable = Variable("myTestVariable")
        VariableNamesHolder().register_variable(new_created_variable)

        VariableNamesHolder().clear()

        self.assertEqual(new_created_variable.id, -1, "Variable id after cleaning should be -1")
        self.assertEqual(VariableNamesHolder().get_number_of_variables(), 0,
                         "There should be no variables after cleaning")

    def testGetVariableOK(self):
        new_created_variable = Variable("myTestVariable")
        VariableNamesHolder().register_variable(new_created_variable)

        given_variable = VariableNamesHolder().get_variable(new_created_variable.id)
        self.assertEqual(given_variable, new_created_variable)

    def testGetVariableNotOKInEmpty(self):
        with self.assertRaises(Exception):
            VariableNamesHolder().get_variable(0)

    def testGetVariableNotOKInNotEmpty(self):
        new_created_variable = Variable("myTestVariable")
        VariableNamesHolder().register_variable(new_created_variable)

        with self.assertRaises(Exception):
            VariableNamesHolder().get_variable(1)

    def testGetVariableIndexOK(self):
        new_created_variable = Variable("myTestVariable")
        VariableNamesHolder().register_variable(new_created_variable)

        self.assertEqual(VariableNamesHolder().get_variable_index(new_created_variable.name), new_created_variable.id)

    def testGetVariableIndexNotOk(self):
        new_created_variable = Variable("myTestVariable")
        VariableNamesHolder().register_variable(new_created_variable)

        with self.assertRaises(Exception):
            VariableNamesHolder().get_variable_index("someCringeName")

    def testVariableRegistration(self):
        new_created_variable = Variable("myTestVariable")
        self.assertFalse(VariableNamesHolder().is_variable_registered(new_created_variable.name),
                         "Variable should be not registered right after creation")
        self.assertEqual(new_created_variable.id, -1, "Not registered variable id should be -1")
        VariableNamesHolder().register_variable(new_created_variable)
        self.assertNotEqual(new_created_variable.id, -1, "After registration variable id should not be -1")
        self.assertTrue(VariableNamesHolder().is_variable_registered(new_created_variable.name),
                        "After registration the variable should be registered")

    def testVariableNotRegistered(self):
        new_created_variable = Variable("myTestVariable")
        VariableNamesHolder().register_variable(new_created_variable)

        self.assertFalse(VariableNamesHolder().is_variable_registered("someCringeName"))


if __name__ == '__main__':
    unittest.main()
