from __future__ import annotations

from typing import Mapping, override

from dataclasses import dataclass, field
from enum import StrEnum

from mysql.connector.types import RowItemType

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

    @classmethod
    def from_db_row(cls, row: Mapping[str, RowItemType]) -> College:
        return cls(
            code=str(row["code"]),
            name=str(row["name"])
        )
    
    def to_db_row(self) -> dict[str, str]:
        return {
            "code": self.code,
            "name": self.name
        }
    
    @override
    def __str__(self) -> str:
        return f"({self.code}) {self.name}"

@dataclass(slots=True)
class Program:
    code: str
    name: str = field(compare=False)
    college: str = field(compare=False)

    @classmethod
    def from_db_row(cls, row: Mapping[str, RowItemType]) -> Program:
        return cls(
            code=str(row["code"]),
            name=str(row["name"]),
            college=str(row["college"])
        )
    
    def to_db_row(self) -> dict[str, str]:
        return {
            "code": self.code,
            "name": self.name,
            "college": self.college
        }

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
    
    @classmethod
    def from_db_row(cls, row: Mapping[str, RowItemType]) -> Student:
        return cls(
            id=str(row["id"]),
            firstname=str(row["firstname"]),
            lastname=str(row["lastname"]),
            year=int(str(row["year"])),
            gender=Gender(str(row["gender"])),
            program=str(row["program"])
        )
    
    def to_db_row(self) -> dict[str, str | int]:
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "year": self.year,
            "gender": self.gender.value,
            "program": self.program
        }

    @property
    def fullname(self) -> str:
        return f"{self.lastname}, {self.firstname}"

    @override
    def __str__(self) -> str:
        return f"{self.id} | {self.fullname} | Year {self.year} | {self.gender} | {self.program}"
