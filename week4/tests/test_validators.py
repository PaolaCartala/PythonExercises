import unittest
from unittest.mock import patch

from mytodolists.validators import CustomValidators
from mytodolists.custom_exceptions import InputNotValidError


class TestCustomValidators(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_validator_whitespaces(self):

        self.assertEqual(CustomValidators().validator_whitespaces('    test   '), 'test')
        self.assertEqual(CustomValidators().validator_whitespaces('    '), False)
        self.assertEqual(CustomValidators().validator_whitespaces(1), False)

    def test_params_validator(self):
        with patch.object(
            CustomValidators, 'validator_whitespaces'
        ) as mocked_validator:
            mocked_validator.side_effect = ('test title', 'test desc')
            self.assertEqual(
                CustomValidators().params_validator('test title', 'test desc', ['tag1', 'tag2']),
                ('test title', 'test desc')
            )

            mocked_validator.side_effect = (False, 'test desc')
            self.assertRaises(
                InputNotValidError, CustomValidators().params_validator,
                '    test', 'test desc', ['tag1', 'tag2']
            )


if __name__ == '__main__':
    unittest.main()
