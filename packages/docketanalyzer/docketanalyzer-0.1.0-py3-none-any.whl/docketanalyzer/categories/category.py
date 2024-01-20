from enum import Enum
from typing import Optional


class Category(Enum):
    """Base class for all categories."""
    def __new__(
        cls,
        value: str,
        description: Optional[str] = None
    ):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._description_ = description
        return obj

    @property
    def description(self):
        return self._description_
