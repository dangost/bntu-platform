from dataclasses import dataclass
from typing import List, Optional

from src.models.user import Student


@dataclass(frozen=True)
class Division:
    id: int
    name: str
    shortname: str
    avatar: str
    description: Optional[str] = ""

    @classmethod
    def from_row(cls, row):
        return Faculty(
            id=row[0], name=row[1], shortname=row[2], avatar=row[3], description=row[4]
        )

    @property
    def json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "shortname": self.shortname,
            "avatar": self.avatar,
            "description": self.description,
        }


@dataclass(frozen=True)
class Group:
    id: int
    leader: Student

    @property
    def json(self) -> dict:
        return {"id": self.id, "leader": self.leader.json}


@dataclass(frozen=True)
class Faculty(Division):
    pass


@dataclass(frozen=True)
class Department(Division):
    pass


@dataclass(frozen=True)
class FacultiesView:
    faculties: List[Faculty]

    @property
    def json(self) -> dict:
        return {"faculties": [faculty.json for faculty in self.faculties]}


@dataclass(frozen=True)
class DepartmentsView:
    faculty: Faculty
    departments: List[Department]

    @property
    def json(self) -> dict:
        return {
            "faculty": self.faculty.json,
            "departments": [dep.json for dep in self.departments],
        }


@dataclass(frozen=True)
class GroupsView:
    faculty: Faculty
    department: Department
    groups: List[Group]

    @property
    def json(self) -> dict:
        return {
            "faculty": self.faculty.json,
            "departments": self.department.json,
            "groups": [group.json for group in self.groups],
        }
