from src.exceptions import DivisionNotFound
from src.models.divisions import (
    FacultiesView,
    DepartmentsView,
    GroupsView,
    Faculty,
    Department,
    Group,
)
from src.models.user import Student
from src.repositories.db_repo import DatabaseClient


class DivisionsService:
    def __init__(self, db_client: DatabaseClient):
        self.__db_client = db_client

    def faculties(self) -> FacultiesView:
        rows = self.__db_client.execute(
            "select id, name, shortcut, avatar, description from faculties"
        )

        faculties = [Faculty.from_row(row) for row in rows]

        return FacultiesView(faculties=faculties)

    def departments(self, faculty_id: int) -> DepartmentsView:
        faculty_rows = self.__db_client.execute(
            "select id, name, shortcut, avatar, description from faculties "
            f"where id = {faculty_id}"
        )
        if not faculty_rows:
            raise DivisionNotFound("Faculty")
        faculty = Faculty.from_row(faculty_rows[0])

        rows = self.__db_client.execute(
            "select id, name, shortcut, avatar, description "
            f"from department where faculty_id={faculty_id};"
        )

        departments = [Department.from_row(row) for row in rows]

        return DepartmentsView(faculty=faculty, departments=departments)

    def groups(self, dep_id: int) -> GroupsView:
        dep_rows = self.__db_client.execute(
            "select id, name, shortcut, avatar, description, faculty_id from department "
            f"where id = {dep_id}"
        )
        if not dep_rows:
            raise DivisionNotFound("Faculty")
        department = Department.from_row(dep_rows[0])
        faculty_id = dep_rows[0][5]

        faculty_rows = self.__db_client.execute(
            "select id, name, shortcut, avatar, description from faculties "
            f"where id = {faculty_id}"
        )
        if not faculty_rows:
            raise DivisionNotFound("Faculty")
        faculty = Faculty.from_row(faculty_rows[0])

        rows = self.__db_client.execute(
            "select g.id, l.leader from groups g inner join leaders l on g.id = l.group_id"
        )

        groups = []
        for row in rows:
            group_id = row[0]
            student_id = row[1]

            student_row = self.__db_client.execute(
                "select s.id, firstname, surname, email, r.name, phone_number, student_id, course "
                "from students s inner join roles r on r.id = s.role_id "
                f"where student_id = {student_id};"
            )
            student = Student.from_row(student_row[0])
            groups.append(Group(id=group_id, leader=student))
        return GroupsView(faculty=faculty, department=department, groups=groups)
