from abc import ABC, abstractmethod
from typing import Union

from domain.model.user import User, UserForm


class DatabaseInterface(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: str) -> Union[User, None]:
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> Union[User, None]:
        pass
