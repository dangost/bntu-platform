import base64
from io import BytesIO
from typing import Union

from src.common.crypto import sha256
from src.exceptions import S3FileNotFound
from src.models.files import UserFile
from src.models.user import User
from src.repositories.db_repo import DatabaseClient
from src.repositories.minio_client import MinioClient, Folders


class FilesService:
    def __init__(self, db_client: DatabaseClient, minio_client: MinioClient):
        self.__db_client = db_client
        self.__minio = minio_client

    def get_user_files(self, user_id: int) -> list[UserFile]:
        pass

    def get_image(self, file_id: int) -> (str, BytesIO):
        result = self.__db_client.execute(
            f"select filename, path from files where id={file_id};"
        )
        if not result or not result[0]:
            raise S3FileNotFound()
        filename, path = result[0]
        image_data = BytesIO(self.__minio.get_image(path))
        return filename, image_data

    def upload_file(
        self,
        user: User,
        filename: str,
        data: Union[str, bytes],
        folder: str = Folders.FILES,
    ) -> (int, str):
        if isinstance(data, str):
            data = base64.b64decode(data.encode("UTF-8"))
        size_bytes = len(data)
        size_mb = str(size_bytes / (1000 * 1000))[0:4]
        file_hash = sha256(data)
        path = self.__minio.upload_file(data, folder, filename, size_bytes)

        # TODO figure out with inherits foreign keys
        self.__db_client.execute(
            f"insert into files(filename, path, size_mb, upload_from, file_hash) "
            f"values ('{filename}', '{path}', '{size_mb}', 2, '{file_hash}')",
            commit=True,
        )
        result = self.__db_client.execute(
            "select id, path from files order by id desc limit 1",
            return_function=lambda r: (r[0][0], r[0][1])
            if len(r) == 1 and len(r[0]) == 2
            else None,
        )
        file_id, path = result
        return file_id, path
