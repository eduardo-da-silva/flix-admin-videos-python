from typing import Dict
from __seedwork.domain.validators import (
    DRFValidator,
    StrictBooleanField,
    StrictCharField,
)
from rest_framework import serializers


class CategoryRules(serializers.Serializer):
    name = StrictCharField(max_length=255)
    description = StrictCharField(required=False, allow_null=True, allow_blank=True)
    is_active = StrictBooleanField(required=False)
    created_at = serializers.DateTimeField(required=False)


class CategoryValidator(DRFValidator):
    def validate(self, data: Dict) -> bool:
        rules = CategoryRules(data=data if data is not None else {})
        return super().validate(rules)


class CategoryValidatorFactory:
    @staticmethod
    def create():
        return CategoryValidator()
