import json

from src.common.crypto import sha256
from src.models.divisions import GroupFullView
from src.models.files import UserFile
from src.models.posts import Post, PostContainer, PostUserView
from src.models.user import User, Student, Teacher
from src.repositories.db_repo import DatabaseClient
from src.exceptions import IncorrectCurrentPassword, PostBodyIsEmpty, S3FileNotFound, PostNotFound
from src.repositories.minio_client import MinioClient


class UserService:
    def __init__(self, db_client: DatabaseClient, minio: MinioClient):
        self.__db_client = db_client
        self.__minio = minio

    def change_password(self, user: User, current_pass: str, new_pass: str) -> None:
        current_hash = sha256(current_pass)
        new_hash = sha256(new_pass)

        email = self.__db_client.execute(
            f"select email from users where id={user.id} and password_hash='{current_hash}'",
            return_function=lambda r: r[0][0] if len(r) > 0 and len(r[0]) > 0 else None,
        )
        if email != user.email:
            raise IncorrectCurrentPassword()

        self.__db_client.execute(
            f"update users set password_hash='{new_hash}' where id={user.id}",
            commit=True,
        )

    def change_avatar(self, user: User, path: str) -> None:
        self.__db_client.execute(
            f"update users set avatar='{path}' where id={user.id}", commit=True
        )

    def create_post(self, user: User, post: Post) -> None:
        groups = post.scope.groups

        if post.scope.faculties or post.scope.departments:
            results = self.__db_client.execute(
                f"select id from groups where "
                f"faculty_id in ({str(post.scope.faculties)[1:-1]}) "
                f"or departament_id in ({str(post.scope.departments)[1:-1]})"
            )
            for result in results:
                groups.append(result[0])

        container = post.container.to_json()
        if not container:
            raise PostBodyIsEmpty()
        self.__db_client.execute(
            f"insert into posts (user_id, container, scope) "
            f"values ({user.id}, '{json.dumps(container)}', '{json.dumps(groups)}')",
            commit=True,
        )

    def get_user_posts(self, visitor: User, user_id: int) -> list[PostContainer]:
        if visitor.role == "Student":
            group = self.__db_client.execute(
                f"select group_id from students where id = {visitor.id};",
                return_function=lambda r: r[0][0]
                if len(r) > 0 and len(r[0]) > 0
                else None,
            )
        else:
            group = None

        results = self.__db_client.execute(
            f"select container, scope, datetime, users.firstname, users.surname, users.id, users.avatar from posts "
            "inner join users on posts.user_id = users.id "
            f"where user_id={user_id} order by datetime desc"
        )

        if not results:
            raise PostNotFound()

        posts = []
        for container, scope, date, user_name, surname, user_id, avatar in results:
            if group in scope or group is None:
                files = []
                for file_id in container.get("files", []):
                    try:
                        filename, size, path = self.__db_client.execute(
                            f"select filename, size_mb, path from files where id={file_id} limit 1",
                            return_function=lambda r: r[0]
                            if len(r) > 0 and len(r[0][0]) > 0
                            else None,
                        )
                    except Exception:
                        raise S3FileNotFound()
                    download_link = self.__minio.get_file(path)
                    files.append(UserFile(filename, size, download_link))
                text = container.get("text")
                date = date.strftime("%d/%m %H:%M")
                posts.append(
                    PostContainer(
                        text=text, files=files, date=date,
                        user=PostUserView(user_id=user_id, full_name=f"{user_name} {surname}", avatar=avatar)
                    )
                )
        return posts

    def get_student_feed(self, student_id: int) -> list[PostContainer]:
        group_id = self.__db_client.execute(
                f"select group_id from students where id = {student_id};",
                return_function=lambda r: r[0][0]
                if len(r) > 0 and len(r[0]) > 0
                else None,
            )
        results = self.__db_client.execute(
            "select container, scope, datetime, users.firstname, users.surname, users.id, users.avatar "
            "from posts "  # oaoaoaoaoaoaoao eto pizdec :((((
            "inner join users on posts.user_id = users.id "
            "order by datetime desc"
        )

        posts = []
        for container, scope, date, user_name, surname, user_id, avatar in results:
            if group_id not in scope:
                continue
            files = []
            for file_id in container.get("files", []):
                try:
                    filename, size, path = self.__db_client.execute(
                        f"select filename, size_mb, path from files where id={file_id} limit 1",
                        return_function=lambda r: r[0]
                        if len(r) > 0 and len(r[0][0]) > 0
                        else None,
                    )
                except Exception:
                    raise S3FileNotFound()
                download_link = self.__minio.get_file(path)
                files.append(UserFile(filename, size, download_link))
            text = container.get("text")
            date = date.strftime("%d/%m %H:%M")
            full_name = user_name + " " + surname
            posts.append(
                PostContainer(
                    text=text, files=files, date=date,
                    user=PostUserView(
                        user_id=user_id, full_name=full_name, avatar=avatar
                    )
                )
            )
        return posts

    def get_student(self, student_id: int) -> Student:
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

        return student

    def get_teacher(self, teacher_id: int) -> Teacher:
        teacher_row = self.__db_client.execute(
            "select t.id, t.firstname, t.surname, t.email, r.name, t.avatar, t.phone_number, "
            "d.id, d.shortcut, f.id, f.shortcut, t.schedule, t.job_title "
            "from teachers t "
            "inner join roles r on t.role_id = r.id "
            "inner join department d on t.departament_id = d.id "
            "inner join faculties f on d.faculty_id = f.id "
            f"where t.id = {teacher_id};"
        )
        teacher = Teacher.from_row(teacher_row[0])
        return teacher
