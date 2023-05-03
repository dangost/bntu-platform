import uuid
from datetime import timedelta
from io import BytesIO

from minio import Minio
from minio.error import S3Error

from src.exceptions import S3CannotUploadFile, S3ImageNotFound


class Folders:
    FILES = "Files"
    IMAGES = "Images"

    @staticmethod
    def content_type(value: str) -> str:
        d = {Folders.FILES: "application/octet-stream", Folders.IMAGES: "image/jpg"}
        return d.get(value, "application/octet-stream")


class MinioClient:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        host: str = "127.0.0.1",
        port: int = 9000,
    ):
        self.__client = Minio(
            endpoint=f"{host}:{port}",
            access_key=access_key,
            secret_key=secret_key,
            secure=False,
        )

        if not self.__client.bucket_exists("data"):
            self.__client.make_bucket("data")

    def upload_file(
        self, data: bytes | BytesIO, folder: str, filename: str, size: int = -1
    ) -> str:
        path = f"{folder}/{str(uuid.uuid4()).replace('-', '')[0:10]}"
        if "." in filename:
            _, ext = filename.split(".")
            path += f".{ext}"

        if size == -1:
            size = len(data)
        if isinstance(data, bytes):
            data = BytesIO(data)

        try:
            self.__client.put_object(
                bucket_name="data",
                object_name=path,
                content_type=Folders.content_type(folder),
                data=data,
                length=size,
                metadata={"filename": filename},
            )
        except S3Error as e:
            raise S3CannotUploadFile(str(e))
        return path

    def get_image(self, path: str) -> bytes:
        if Folders.IMAGES not in path:
            raise S3ImageNotFound()
        try:
            data = self.__client.get_object("data", object_name=path).data
        except S3Error as e:
            raise S3ImageNotFound(str(e))
        return data

    def get_file(self, path: str) -> str:
        if Folders.FILES not in path:
            raise S3ImageNotFound()
        try:
            url = self.__client.get_presigned_url(
                "GET", "data", path, expires=timedelta(hours=12)
            )
        except S3Error as e:
            raise S3ImageNotFound(str(e))
        return url
