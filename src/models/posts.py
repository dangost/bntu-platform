from dataclasses import dataclass
from typing import Optional

from src.models.files import UserFile


@dataclass(frozen=True)
class PostScope:
    faculties: Optional[list[str]]
    departments: Optional[list[str]]
    groups: Optional[list[str]]

    @classmethod
    def from_json(cls, body: dict):
        return PostScope(
            faculties=body.get("faculties", []),
            departments=body.get("departments", []),
            groups=body.get("groups", []),
        )


@dataclass(frozen=True)
class PostContainerUpload:
    text: Optional[str]
    files: Optional[list[int]]

    @classmethod
    def from_json(cls, body: dict):
        return PostContainerUpload(
            text=body.get("text", ""), files=body.get("files", [])
        )

    def to_json(self):
        return {"text": self.text, "files": self.files}


@dataclass(frozen=True)
class PostUserView:
    user_id: int
    full_name: str
    avatar: str

    def to_json(self) -> dict:
        return {
            "user_id": self.user_id,
            "full_name": self.full_name,
            "avatar": self.avatar,
        }


@dataclass(frozen=True)
class PostContainer:
    text: Optional[str]
    files: Optional[list[UserFile]]
    date: str
    user: Optional[PostUserView] = None

    def to_json(self):
        return {
            "text": self.text,
            "date": self.date,
            "files": [file.to_json() for file in self.files],
            "user": self.user.to_json() if self.user else None,
        }


@dataclass(frozen=True)
class Post:
    container: PostContainerUpload
    scope: PostScope

    @classmethod
    def from_json(cls, body):
        return Post(
            container=PostContainerUpload.from_json(body.get("container", {})),
            scope=PostScope.from_json(body.get("scope", {})),
        )
