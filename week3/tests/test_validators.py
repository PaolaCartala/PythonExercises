import unittest

from mytodolists.validators import validator_whitespaces


class TestValidators(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_validator_whitespaces(self):

        self.assertEqual(validator_whitespaces('    test   '), 'test')
        self.assertEqual(validator_whitespaces('    '), False)
        self.assertEqual(validator_whitespaces(1), False)


if __name__ == '__main__':
    unittest.main()
