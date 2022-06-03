import unittest
from core.category.domain.validators import CategoryValidator, CategoryValidatorFactory


class TestCategoryValidatorUnit(unittest.TestCase):
    validator: CategoryValidator

    def setUp(self) -> None:
        self.validator = CategoryValidatorFactory().create()
        return super().setUp()

    def test_invalidation_cases_for_name_field(self):
        is_valid = self.validator.validate(None)
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['name'], ['This field is required.'])

        is_valid = self.validator.validate({})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['name'], ['This field is required.'])

        is_valid = self.validator.validate({'name': ''})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['name'], ['This field may not be blank.'])

        is_valid = self.validator.validate({'name': None})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['name'], ['This field may not be null.'])

        is_valid = self.validator.validate({'name': 5})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['name'], ['Not a valid string.'])

        is_valid = self.validator.validate({'name': 't' * 256})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['name'], ['Ensure this field has no more than 255 characters.'])

    def test_invalidation_cases_for_description_field(self):
        is_valid = self.validator.validate({'description': 5})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['description'], ['Not a valid string.'])

    def test_invalidation_cases_for_is_active_field(self):
        is_valid = self.validator.validate({'is_active': None})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['is_active'], ['This field may not be null.'])

        is_valid = self.validator.validate({'is_active': 0})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['is_active'], ['Must be a valid boolean.'])

    def test_invalidation_cases_for_created_at_field(self):
        is_valid = self.validator.validate({'created_at': None})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['created_at'], ['This field may not be null.'])

        is_valid = self.validator.validate({'created_at': 5})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['created_at'], [
                             'Datetime has wrong format. Use one of these formats instead: ' +
                             'YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].'])

    def test_valid_cases(self):
        valid_data = [
            {'name': 'Movie'},
            {'name': 'Movie', 'description': None},
            {'name': 'Movie', 'description': ''},
            {'name': 'Movie', 'is_active': True},
            {'name': 'Movie', 'is_active': False},
            {'name': 'Movie', 'description': 'Some description'},
            {'name': 'Movie', 'description': 'Some description', 'is_active': True},
            {'name': 'Movie', 'description': 'Some description', 'is_active': False},
        ]

        for data in valid_data:
            is_valid = self.validator.validate(data)
            self.assertTrue(is_valid)
