import uuid
from datetime import timedelta
from io import BytesIO
from typing import Union

from minio import Minio
from minio.error import S3Error

from src.exceptions import S3CannotUploadFile, S3ImageNotFound, S3FileIsNotImage


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
        base_url: str = "127.0.0.1",
        host: str = "127.0.0.1",
        port: int = 9000,
    ):
        self.__client = Minio(
            endpoint=f"{host}:{port}",
            access_key=access_key,
            secret_key=secret_key,
            secure=False,
        )

        self.__base_url = base_url

        if not self.__client.bucket_exists("data"):
            self.__client.make_bucket("data")

    def upload_file(
        self, data: Union[bytes, BytesIO], folder: str, filename: str, size: int = -1
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
        try:
            obj = self.__client.get_object("data", object_name=path)
            data = obj.data
            if "image" not in obj.headers.get("Content-Type"):
                raise S3FileIsNotImage()

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
            url = str(url).replace("minio", self.__base_url)
        except S3Error as e:
            raise S3ImageNotFound(str(e))
        return url
