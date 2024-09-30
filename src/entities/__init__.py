from typing import override

from enum import StrEnum

class Gender(StrEnum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"

    @override
    def __str__(self):
        return self.name.capitalize()

