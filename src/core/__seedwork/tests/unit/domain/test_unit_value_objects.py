from abc import ABC
from dataclasses import FrozenInstanceError, dataclass, is_dataclass
import unittest
from unittest.mock import patch
import uuid
from core.__seedwork.domain.exceptions import InvalidUuidException
from core.__seedwork.domain.value_objects import UniqueEntityId, ValueObject


@dataclass(frozen=True)
class StubOneProp(ValueObject):
    prop: str


@dataclass(frozen=True)
class StubTwoProps(ValueObject):
    prop1: str
    prop2: str


class TestValueObjectUnit(unittest.TestCase):
    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(ValueObject))

    def test_if_is_an_abstract_class(self):
        self.assertIsInstance(ValueObject(), ABC)

    def test_init_prop(self):
        vo1 = StubOneProp(prop="value")
        self.assertEqual(vo1.prop, "value")

        vo2 = StubTwoProps(prop1="value1", prop2="value2")
        self.assertEqual(vo2.prop1, "value1")
        self.assertEqual(vo2.prop2, "value2")

    def test_convert_to_str(self):
        vo1 = StubOneProp(prop="value")
        self.assertEqual(vo1.prop, str(vo1))

        vo2 = StubTwoProps(prop1="value1", prop2="value2")
        self.assertEqual('{"prop1": "value1", "prop2": "value2"}', str(vo2))

    def test_if_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            vo1 = StubOneProp(prop="value")
            vo1.prop = "NewProp"


class TestUniqueEntityIdUnit(unittest.TestCase):
    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(UniqueEntityId))

    def test_throw_exception_when_uuid_is_invalid(self):
        with patch.object(
            UniqueEntityId,
            "_UniqueEntityId__validate",
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate,  # pylint: disable=protected-access
        ) as mock_validate:
            with self.assertRaises(InvalidUuidException) as assert_error:
                UniqueEntityId("fakeId")
            mock_validate.assert_called_once()
            self.assertEqual(assert_error.exception.args[0], "ID must be a valid UUID")

    def test_accept_uuid_passed_in_constructor(self):
        with patch.object(
            UniqueEntityId,
            "_UniqueEntityId__validate",
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate,  # pylint: disable=protected-access
        ) as mock_validate:
            value_object = UniqueEntityId("8e65b539-6bdb-42eb-b782-1470846e9cbf")
            mock_validate.assert_called_once()
            self.assertEqual(value_object.id, "8e65b539-6bdb-42eb-b782-1470846e9cbf")

        uuid_value = uuid.uuid4()
        value_object = UniqueEntityId(uuid_value)
        self.assertEqual(value_object.id, str(uuid_value))

    def test_generate_id_when_no_passed_id_in_constructor(self):  # pylint: disable=no-self-use
        with patch.object(
            UniqueEntityId,
            "_UniqueEntityId__validate",
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate,  # pylint: disable=protected-access
        ) as mock_validate:
            value_object = UniqueEntityId()
            uuid.UUID(value_object.id)
            mock_validate.assert_called_once()

    def test_if_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            value_object = UniqueEntityId()
            value_object.id = "8e65b539-6bdb-42eb-b782-1470846e9cbf"

    def test_convert_to_str(self):
        value_object = UniqueEntityId()
        self.assertEqual(value_object.id, str(value_object))
