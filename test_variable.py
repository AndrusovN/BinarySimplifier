import unittest
from variable import Variable


class VariableTestCase(unittest.TestCase):
    def testInitialization(self):
        name = "myTestVariable"
        var = Variable(name)
        self.assertEqual(var.name, name)
        self.assertEqual(var.id, -1)

    def testEqualsReflexity(self):
        var = Variable("myTestVariable")
        self.assertEqual(var, var)

    def testNotEquals(self):
        first = Variable("myTestVariable")
        second = Variable("someOtherVariable")
        self.assertNotEqual(first, second)

    def testHashEquals(self):
        var = Variable("myTestVariable")
        self.assertEqual(hash(var), hash(var))

    def testStrIsName(self):
        name = "myTestVariable"
        var = Variable(name)
        self.assertEqual(str(var), name)

    def testIntIsId(self):
        var = Variable("myTestVariable")
        self.assertEqual(var.id, int(var))
        var.id = 179
        self.assertEqual(var.id, int(var))


if __name__ == '__main__':
    unittest.main()
