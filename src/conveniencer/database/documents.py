from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


class Document(ABC):
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def by(self) -> Dict[str, Any]:
        raise NotImplementedError


@dataclass
class Book(Document):
    user_id: str
    name: str
    file_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "file_id": self.file_id,
        }

    def by(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "name": self.name,
        }


@dataclass
class Link(Document):
    user_id: str
    name: str
    url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "url": self.url,
        }

    def by(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "name": self.name,
        }


@dataclass
class Photo(Document):
    user_id: str
    name: str
    photo_ids: List[str] = field(default_factory=list)
    document_ids: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "photo_ids": self.photo_ids,
            "document_ids": self.document_ids,
        }

    def by(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "name": self.name,
        }


@dataclass
class Archive(Document):
    user_id: str
    name: str
    file_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "file_id": self.file_id,
        }

    def by(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "name": self.name,
        }
