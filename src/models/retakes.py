from dataclasses import dataclass


@dataclass(frozen=True)
class RetakeBody:
    subject: str
    type: str
    teacher: str

    @classmethod
    def from_json(cls, body: dict):
        return RetakeBody(
            subject=body.get("subject"),
            type=body.get("type"),
            teacher=body.get("teacher"),
        )


@dataclass(frozen=True)
class Retake:
    id: int
    subject: str
    type: str
    teacher_id: int
    teacher_fullname: str
    student_id: int
    student_fullname: str
    expiration: str

    @classmethod
    def from_row(cls, row):
        return Retake(
            id=row[0],
            subject=row[1],
            type=row[2],
            teacher_id=row[3],
            teacher_fullname=row[4] + " " + row[5],
            student_id=row[6],
            student_fullname=row[7] + " " + row[8],
            expiration=row[9],
        )

    @property
    def json(self) -> dict:
        return {
            "id": self.id,
            "subject": self.subject,
            "type": self.type,
            "teacher_id": self.teacher_id,
            "teacher_fullname": self.teacher_fullname,
            "student_id": self.student_id,
            "student_fullname": self.student_fullname,
            "expiration": self.expiration,
        }
