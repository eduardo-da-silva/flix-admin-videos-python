from typing import Dict
from rest_framework import serializers
from __seedwork.domain.validators import (
    DRFValidator,
    StrictBooleanField,
    StrictCharField,
)


class CategoryRules(serializers.Serializer):  # pylint: disable=abstract-method
    name = StrictCharField(max_length=255)
    description = StrictCharField(required=False, allow_null=True, allow_blank=True)
    is_active = StrictBooleanField(required=False)
    created_at = serializers.DateTimeField(required=False)


class CategoryValidator(DRFValidator):
    def validate(self, serializer: Dict) -> bool:
        rules = CategoryRules(data=serializer if serializer is not None else {})
        return super().validate(rules)


class CategoryValidatorFactory:
    @staticmethod
    def create():
        return CategoryValidator()
