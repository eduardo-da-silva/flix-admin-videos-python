from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional
from core.__seedwork.domain.entities import Entity
from core.__seedwork.domain.exceptions import EntityValidationException

# from core.__seedwork.domain.validators import ValidatorRules
from core.category.domain.validators import CategoryValidatorFactory


@dataclass(kw_only=True, frozen=True, slots=True)
class Category(Entity):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = field(default_factory=datetime.now)
    # update_at: Optional[datetime] = field(default_factory=lambda: datetime.now())

    # def __new__(cls, **kwargs):
    #     cls.validate(
    #         name=kwargs.get("name"),
    #         description=kwargs.get("description"),
    #         is_active=kwargs.get("is_active"),
    #         created_at=kwargs.get("created_at"),
    #     )
    #     return super(Category, cls).__new__(cls)

    def __post_init__(self):
        if not self.created_at:
            object.__setattr__(self, "created_at", datetime.now())
        self.validate()

    def update(self, *, name: str, description: str) -> None:
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "description", description)
        self.validate()

    def activate(self):
        object.__setattr__(self, "is_active", True)

    def deactivate(self):
        object.__setattr__(self, "is_active", False)

    # @classmethod
    # def validate(cls, name: str, description: str, is_active: bool = None):
    #     ValidatorRules.values(name, "name").required().string().max_length(255)
    #     ValidatorRules.values(description, "description").string()
    #     ValidatorRules.values(is_active, "is_active").boolean()

    def validate(self):
        validator = CategoryValidatorFactory.create()
        is_valid = validator.validate(self.to_dict())
        if not is_valid:
            raise EntityValidationException(validator.errors)
