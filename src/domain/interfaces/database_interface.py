from abc import ABC, abstractmethod
from typing import Union, List

from domain.model.user import User, AuthenticationUser
from domain.model.model import Model


class DatabaseInterface(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: str) -> Union[User, None]:
        pass

    @abstractmethod
    def get_auth_user_by_username(
        self, username: str
    ) -> Union[AuthenticationUser, None]:
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> Union[User, None]:
        pass

    @abstractmethod
    def insert_user(self, user: AuthenticationUser) -> None:
        pass

    @abstractmethod
    def get_model_by_id(self, model_id: str) -> Union[Model, None]:
        pass

    @abstractmethod
    def get_model_list(self) -> Union[List[Model], None]:
        pass
