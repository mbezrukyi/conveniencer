from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional


class Entity(ABC):
    @abstractmethod
    def data(self) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def update_by(self) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def update_data(self) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def remove_by(self) -> Dict[str, Any]:
        raise NotImplementedError


@dataclass
class Book(Entity):
    name: str
    file_id: Optional[str] = None

    @property
    def data(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "file_id": self.file_id,
        }

    @property
    def update_by(self) -> Dict[str, Any]:
        return {"name": self.name}

    @property
    def update_data(self) -> Dict[str, Any]:
        return {"file_id": self.file_id}

    @property
    def remove_by(self) -> Dict[str, Any]:
        return {"name": self.name}


@dataclass
class Link(Entity):
    name: str
    url: Optional[str] = None

    @property
    def data(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "url": self.url,
        }

    @property
    def update_by(self) -> Dict[str, Any]:
        return {"name": self.name}

    @property
    def update_data(self) -> Dict[str, Any]:
        return {"url": self.url}

    @property
    def remove_by(self) -> Dict[str, Any]:
        return {"name": self.name}
