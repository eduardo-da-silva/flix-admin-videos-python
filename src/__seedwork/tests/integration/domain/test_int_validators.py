import unittest
from rest_framework import serializers
from __seedwork.domain.validators import DRFValidator, StrictBooleanField, StrictCharField


class StubSerializer(serializers.Serializer):   # pylint: disable=abstract-method
    name = serializers.CharField()
    price = serializers.IntegerField()


class TestDRFValidatorIntegration(unittest.TestCase):
    def test_validation_with_error(self):
        validator = DRFValidator()
        serializer = StubSerializer(data={})
        is_valid = validator.validate(serializer)
        self.assertFalse(is_valid)
        self.assertEqual(
            validator.errors,
            {"name": ["This field is required."], "price": ["This field is required."]},
        )

    def test_validation_without_errors(self):
        validator = DRFValidator()
        serializer = StubSerializer(data={"name": "some value", "price": 10})
        is_valid = validator.validate(serializer)
        self.assertTrue(is_valid)
        self.assertDictEqual(
            validator.validated_data,
            {"name": "some value", "price": 10},
        )


class TestStrictCharFieldUnit(unittest.TestCase):
    def test_if_is_invalid_when_not_str_values(self):
        class StubStrictCharFieldSerializer(serializers.Serializer):    # pylint: disable=abstract-method
            name = StrictCharField()

        serializer = StubStrictCharFieldSerializer(data={'name': 5})
        serializer.is_valid()
        self.assertEqual(serializer.errors,  {
            'name': [serializers.ErrorDetail(string='Not a valid string.', code='invalid')]
        })

        serializer = StubStrictCharFieldSerializer(data={'name': True})
        serializer.is_valid()
        self.assertEqual(serializer.errors,  {
            'name': [serializers.ErrorDetail(string='Not a valid string.', code='invalid')]
        })

    def test_if_none_value_is_valid(self):
        class StubStrictCharFieldSerializer(serializers.Serializer):        # pylint: disable=abstract-method
            name = StrictCharField(required=False, allow_null=True)

        serializer = StubStrictCharFieldSerializer(data={'name': None})
        self.assertTrue(serializer.is_valid())


class TestStrictBooleanFieldUnit(unittest.TestCase):
    def test_if_is_invalid_when_not_boolean_values(self):
        class StubStrictBooleanFieldSerializer(serializers.Serializer):  # pylint: disable=abstract-method
            active = StrictBooleanField()

        serializer = StubStrictBooleanFieldSerializer(data={'active': 1})
        serializer.is_valid()
        self.assertEqual(serializer.errors,  {
            'active': [serializers.ErrorDetail(string='Must be a valid boolean.', code='invalid')]
        })

        serializer = StubStrictBooleanFieldSerializer(data={'active': 0})
        serializer.is_valid()
        self.assertEqual(serializer.errors,  {
            'active': [serializers.ErrorDetail(string='Must be a valid boolean.', code='invalid')]
        })

        serializer = StubStrictBooleanFieldSerializer(data={'active': 'True'})
        serializer.is_valid()
        self.assertEqual(serializer.errors,  {
            'active': [serializers.ErrorDetail(string='Must be a valid boolean.', code='invalid')]
        })

        serializer = StubStrictBooleanFieldSerializer(data={'active': 'False'})
        serializer.is_valid()
        self.assertEqual(serializer.errors,  {
            'active': [serializers.ErrorDetail(string='Must be a valid boolean.', code='invalid')]
        })

    def test_if_value_is_valid(self):
        class StubStrictBooleanFieldSerializer(serializers.Serializer):     # pylint: disable=abstract-method
            active = StrictBooleanField(required=False, allow_null=True)

        serializer = StubStrictBooleanFieldSerializer(data={'active': True})
        self.assertTrue(serializer.is_valid())

        serializer = StubStrictBooleanFieldSerializer(data={'active': False})
        self.assertTrue(serializer.is_valid())

        serializer = StubStrictBooleanFieldSerializer(data={'active': None})
        self.assertTrue(serializer.is_valid())
