from abc import ABC, abstractmethod
from typing import List, Union

from domain.model.user import User, AuthenticationUser
from domain.model.inference import Inference


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
    def get_inference_by_id(self, inference_id: str) -> Union[Inference, None]:
        pass

    @abstractmethod
    def get_inference_list_by_user_id(
        self, user_id: str
    ) -> Union[List[Inference], None]:
        pass

    @abstractmethod
    def insert_inference(self, inference: Inference) -> None:
        pass
