from dataclasses import dataclass


@dataclass(frozen=True)
class UserFile:
    filename: str
    size_mb: str
    download_link: str

    def to_json(self) -> dict:
        return {
            "filename": self.filename,
            "size": self.size_mb,
            "download_link": self.download_link
        }
