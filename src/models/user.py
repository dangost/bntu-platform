from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: int
    firstname: str
    surname: str
    email: str
    role: str
    phone_number: str

    @classmethod
    def from_row(cls, row):
        return User(
            id=row[0],
            firstname=row[1],
            surname=row[2],
            email=row[3],
            role=row[4],
            phone_number=row[5],
        )

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "firstname": self.firstname,
            "surname": self.surname,
            "email": self.email,
            "role": self.role,
            "phone_number": self.phone_number,
        }


@dataclass(frozen=True)
class Student(User):
    student_id: int
    course: int

    @classmethod
    def from_row(cls, row):
        return Student(
            id=row[0],
            firstname=row[1],
            surname=row[2],
            email=row[3],
            role=row[4],
            phone_number=row[5],
            student_id=row[6],
            course=row[7],
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
            "student_id": self.student_id,
            "course": self.course,
        }
