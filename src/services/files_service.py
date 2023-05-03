import base64

from src.common.crypto import sha256
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

    def upload_file(
        self, user: User, filename: str, data: str | bytes, folder: str = Folders.FILES
    ):
        if isinstance(data, str):
            data = base64.b64decode(data.encode("UTF-8"))
        size_bytes = len(data)
        size_mb = str(size_bytes / (1000 * 1000))[0:4]
        file_hash = sha256(data)
        path = self.__minio.upload_file(data, folder, filename, size_bytes)

        self.__db_client.execute(
            f"insert into files(filename, path, size_mb, upload_from, file_hash) "
            f"values ('{filename}', '{path}', '{size_mb}', {user.id}, '{file_hash}')",
            commit=True,
        )
