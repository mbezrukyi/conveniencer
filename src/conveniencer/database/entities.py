from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


class Entity(ABC):
    @abstractmethod
    def by(self) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def data(self) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def replace(self) -> Dict[str, Any]:
        raise NotImplementedError


@dataclass
class Book(Entity):
    name: str
    file_id: Optional[str] = None

    @property
    def by(self) -> Dict[str, Any]:
        return {"name": self.name}

    @property
    def data(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "file_id": self.file_id,
        }

    @property
    def replace(self) -> Dict[str, Any]:
        return {"file_id": self.file_id}


@dataclass
class Link(Entity):
    name: str
    url: Optional[str] = None

    @property
    def by(self) -> Dict[str, Any]:
        return {"name": self.name}

    @property
    def data(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "url": self.url,
        }

    @property
    def replace(self) -> Dict[str, Any]:
        return {"url": self.url}


@dataclass
class Photo(Entity):
    name: str
    photo_ids: List[str] = field(default_factory=list)
    document_ids: List[str] = field(default_factory=list)

    @property
    def by(self) -> Dict[str, Any]:
        return {"name": self.name}

    @property
    def data(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "photo_ids": self.photo_ids,
            "document_ids": self.document_ids,
        }

    @property
    def replace(self) -> Dict[str, Any]:
        return {
            "photo_ids": self.photo_ids,
            "document_ids": self.document_ids,
        }


@dataclass
class Archive(Entity):
    name: str
    file_id: Optional[str] = None

    @property
    def by(self) -> Dict[str, Any]:
        return {"name": self.name}

    @property
    def data(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "file_id": self.file_id,
        }

    @property
    def replace(self) -> Dict[str, Any]:
        return {"file_id": self.file_id}
