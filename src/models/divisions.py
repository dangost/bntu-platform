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
class GroupFullView:
    id: int
    leader_id: int
    leader_name: str
    faculty_id: int
    faculty_short: str
    dep_id: int
    dep_short: int
    course: int
    students: Optional[List[Student]] = None

    @classmethod
    def from_row(cls, row, students_rows):
        return GroupFullView(
            id=row[0],
            leader_id=row[1],
            leader_name=row[2] + " " + row[3],
            faculty_id=row[4],
            faculty_short=row[5],
            dep_id=row[6],
            dep_short=row[7],
            course=row[8],
            students=[Student.from_row(s_row) for s_row in students_rows] if students_rows else [],
        )

    @property
    def json(self) -> dict:
        return {
            "id": self.id,
            "leader_id": self.leader_id,
            "leader_name": self.leader_name,
            "faculty_id": self.faculty_id,
            "faculty_short": self.faculty_short,
            "dep_id": self.dep_id,
            "dep_short": self.dep_short,
            "course": self.course,
            "students": [student.json for student in self.students] if self.students else []
        }


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
