from typing import Optional

from src.exceptions import DivisionNotFound
from src.models.divisions import (
    FacultiesView,
    DepartmentsView,
    GroupsView,
    Faculty,
    Department,
    Group, GroupFullView,
)
from src.models.user import Student
from src.repositories.db_repo import DatabaseClient


class DivisionsService:
    def __init__(self, db_client: DatabaseClient):
        self.__db_client = db_client

    def faculties(self) -> FacultiesView:
        query = "select id, name, shortcut, avatar, description from faculties"
        rows = self.__db_client.execute(query)

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
                "select s.id, s.firstname, s.surname, s.email, r.name, s.avatar, "
                "s.phone_number, s.student_id, s.course, s.group_id, d.id, "
                "d.shortcut, f.id, f.shortcut "
                "from students s "
                "inner join roles r on s.role_id = r.id "
                "inner join groups g on s.group_id = g.id "
                "inner join department d on g.departament_id = d.id "
                "inner join faculties f on d.faculty_id = f.id "
                f"where s.id = {student_id};"
            )
            student = Student.from_row(student_row[0])
            groups.append(Group(id=group_id, leader=student))
        return GroupsView(faculty=faculty, department=department, groups=groups)

    def get_group(self, group_id: int) -> GroupFullView:
        students_rows = self.__db_client.execute(
            "select s.id, s.firstname, s.surname, s.email, r.name, s.avatar, "
            "s.phone_number, s.student_id, s.course, s.group_id, d.id, "
            "d.shortcut, f.id, f.shortcut "
            "from students s "
            "inner join roles r on s.role_id = r.id "
            "inner join groups g on s.group_id = g.id "
            "inner join department d on g.departament_id = d.id "
            "inner join faculties f on d.faculty_id = f.id "
            f"where s.group_id = {group_id};"
        )

        group_rows = self.__db_client.execute(
            "select g.id, l.leader, u.firstname, u.surname, f.id, f.shortcut, "
            "d.id, d.shortcut, g.course "
            "from groups g "
            "inner join leaders l on g.id = l.group_id "
            "inner join users u on u.id = l.leader "
            "inner join faculties f on g.faculty_id = f.id "
            "inner join department d on g.departament_id = d.id "
            f"where g.id = {group_id};"
        )

        return GroupFullView.from_row(group_rows[0], students_rows)
