from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional
from xml.dom.minidom import Entity


@dataclass(kw_only=True, frozen=True, slots=True)
class Category(Entity):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = field(default_factory=lambda: datetime.now())

    def update(
        self, *, name: Optional[str] = None, description: Optional[str] = None
    ) -> None:
        new_name = name if name is not None else self.name
        object.__setattr__(self, "name", new_name)
        new_description = description if description is not None else self.description
        object.__setattr__(self, "description", new_description)

    def activate(self):
        object.__setattr__(self, "is_active", True)

    def deactivate(self):
        object.__setattr__(self, "is_active", False)
