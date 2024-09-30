from typing import override

from dataclasses import dataclass, field
from enum import StrEnum

class Gender(StrEnum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"

    @override
    def __str__(self):
        return self.name.capitalize()

@dataclass(slots=True)
class College:
    code: str
    name: str = field(compare=False)

    @override
    def __str__(self) -> str:
        return f"({self.code}) {self.name}"

@dataclass(slots=True)
class Program:
    code: str
    name: str = field(compare=False)
    college: str = field(compare=False)

    @override
    def __str__(self) -> str:
        return f"{self.college} | ({self.code}) {self.name}"
    
@dataclass(slots=True)
class Student:
    id: str
    firstname: str = field(compare=False)
    lastname: str = field(compare=False)
    year: int = field(compare=False)
    gender: Gender = field(compare=False)
    program: str = field(compare=False)
    
    @property
    def fullname(self) -> str:
        return f"{self.lastname}, {self.firstname}"

    @override
    def __str__(self) -> str:
        return f"{self.id} | {self.fullname} | Year {self.year} | {self.gender} | {self.program}"
