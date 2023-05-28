from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class User:
    id: int
    firstname: str
    surname: str
    email: str
    role: str
    phone_number: str
    avatar: str

    @classmethod
    def from_row(cls, row):
        return User(
            id=row[0],
            firstname=row[1],
            surname=row[2],
            email=row[3],
            role=row[4],
            avatar=row[5],
            phone_number=row[6]
        )

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "firstname": self.firstname,
            "surname": self.surname,
            "email": self.email,
            "role": self.role,
            "phone_number": self.phone_number,
            "avatar": self.avatar
        }


@dataclass(frozen=True)
class Student(User):
    departament_id: int
    dep_shortname: str
    faculty_id: int
    faculty_shortname: str
    student_id: int
    course: int
    group: str

    @classmethod
    def from_row(cls, row):
        return Student(
            id=row[0],
            firstname=row[1],
            surname=row[2],
            email=row[3],
            role=row[4],
            avatar=row[5],
            phone_number=row[6],
            student_id=row[7],
            course=row[8],
            group=row[9],
            departament_id=row[10],
            dep_shortname=row[11],
            faculty_id=row[12],
            faculty_shortname=row[13]
        )

    @property
    def json(self) -> dict:
        return {
            "id": self.id,
            "firstname": self.firstname,
            "surname": self.surname,
            "email": self.email,
            "role": self.role,
            "phone_number": self.phone_number,
            "avatar": self.avatar,
            "student_id": self.student_id,
            "course": self.course,
            "group": self.group,
            "departament_id": self.departament_id,
            "dep_shortname": self.dep_shortname,
            "faculty_id": self.faculty_id,
            "faculty_shortname": self.faculty_shortname
        }


@dataclass(frozen=True)
class Teacher(User):
    departament_id: int
    departament_name: str
    faculty_id: int
    faculty_shortname: str
    schedule: Optional[dict]
    job_title: str

    @classmethod
    def from_row(cls, row):
        return Teacher(
            id=row[0],
            firstname=row[1],
            surname=row[2],
            email=row[3],
            role=row[4],
            avatar=row[5],
            phone_number=row[6],
            departament_id=row[7],
            departament_name=row[8],
            faculty_id=row[9],
            faculty_shortname=row[10],
            schedule=row[11],
            job_title=row[12],
        )

    @property
    def json(self) -> dict:
        return {
            "id": self.id,
            "firstname": self.firstname,
            "surname": self.surname,
            "email": self.email,
            "role": self.role,
            "phone_number": self.phone_number,
            "avatar": self.avatar,
            "departament_id": self.departament_id,
            "departament_name": self.departament_name,
            "faculty_id": self.faculty_id,
            "faculty_shortname": self.faculty_shortname,
            "schedule": self.schedule,
            "job_title": self.job_title,
        }