from abc import ABC
from dataclasses import dataclass, is_dataclass
import unittest

from core.__seedwork.domain.entities import Entity
from core.__seedwork.domain.value_objects import UniqueEntityId


@dataclass(frozen=True, slots=True)
class StubEntity(Entity):
    prop1: str = None
    prop2: str = None


class TestEntityUnit(unittest.TestCase):
    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Entity))

    def test_if_is_an_abstract_class(self):
        self.assertIsInstance(Entity(), ABC)

    def test_set_unique_entity_id_and_props(self):
        entity = StubEntity(prop1="value1", prop2="value2")
        self.assertEqual(entity.prop1, "value1")
        self.assertEqual(entity.prop2, "value2")
        self.assertIsInstance(entity.unique_entity_id, UniqueEntityId)
        self.assertEqual(entity.unique_entity_id.id, entity.id)

    def test_accept_a_valid_uuid(self):
        entity = StubEntity(
            unique_entity_id=UniqueEntityId("8e65b539-6bdb-42eb-b782-1470846e9cbf"),
            prop1="value1",
            prop2="value2",
        )
        self.assertEqual(entity.id, "8e65b539-6bdb-42eb-b782-1470846e9cbf")

    def test_to_dict_method(self):
        entity = StubEntity(
            unique_entity_id=UniqueEntityId("8e65b539-6bdb-42eb-b782-1470846e9cbf"),
            prop1="value1",
            prop2="value2",
        )
        self.assertDictEqual(
            entity.to_dict(),
            {
                "id": "8e65b539-6bdb-42eb-b782-1470846e9cbf",
                "prop1": "value1",
                "prop2": "value2",
            },
        )
