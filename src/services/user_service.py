import json

from src.common.crypto import sha256
from src.models.files import UserFile
from src.models.posts import Post, PostContainer
from src.models.user import User
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
            f"select container, scope from posts where user_id={user_id}"
        )

        if not results:
            raise PostNotFound()

        posts = []
        for container, scope in results:
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

                posts.append(PostContainer(text=text, files=files))
        return posts
