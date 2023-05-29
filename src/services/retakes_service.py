from src.exceptions import TeacherNotFound
from src.models.retakes import Retake, RetakeBody
from src.repositories.db_repo import DatabaseClient


class RetakesService:
    def __init__(self, db_client: DatabaseClient):
        self.__db_client = db_client

    def get_student_retakes(self, student_id: int) -> list[Retake]:
        return self.__get_retake_sql(f"s.id={student_id}")

    def get_teacher_retakes(self, teacher_id: int) -> list[Retake]:
        return self.__get_retake_sql(f"t.id={teacher_id}")

    def __get_retake_sql(
        self, where: str
    ) -> list[Retake]:  # where = "t.id={teacher_id}"
        rows = self.__db_client.execute(
            "select r.id, r.subject, r.type, t.id, t.firstname, t.surname, "
            "s.id, s.firstname, s.surname, to_char(r.expire_at, 'DD/MM') "
            "from retakes r "
            "inner join students s on r.student_id = s.id "
            "inner join teachers t on r.teacher_id = t.id "
            f"where expire_at > now() and {where};"
        )
        if not rows:
            return []
        return [Retake.from_row(row) for row in rows]

    def create_retake(self, user_id: int, retake: RetakeBody) -> None:
        teacher_name, teacher_surname = retake.teacher.lower().split(" ")
        teacher_row = self.__db_client.execute(
            "select id from teachers "
            f"where (lower(firstname) = '{teacher_name}' or lower(firstname) = '{teacher_surname}')"
            f"and (lower(surname) = '{teacher_surname}' or lower(surname) = '{teacher_name}')"
            f"limit 1;"
        )

        if not teacher_row or not teacher_row[0]:
            raise TeacherNotFound()

        teacher_id = teacher_row[0][0]

        self.__db_client.execute(
            "insert into retakes(subject, teacher_id, student_id, type)"
            f"values ('{retake.subject}', {teacher_id}, {user_id}, '{retake.type}')",
            commit=True,
        )
