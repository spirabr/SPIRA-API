import inject
from typing import Union, List

from domain.model.user import User, AuthenticationUser
from domain.model.inference import Inference
from domain.model.model import Model
from domain.model.result import Result
from domain.interfaces.database_interface import DatabaseInterface


class DatabasePort:
    @inject.autoparams()
    def __init__(self, database: DatabaseInterface):
        self._database = database

    # user methods

    def get_user_by_id(self, user_id: str) -> Union[User, None]:
        return self._database.get_user_by_id(user_id)

    def get_auth_user_by_username(
        self, username: str
    ) -> Union[AuthenticationUser, None]:
        return self._database.get_auth_user_by_username(username)

    def get_user_by_username(self, username: str) -> Union[User, None]:
        return self._database.get_user_by_username(username)

    def insert_user(self, user: AuthenticationUser) -> None:
        return self._database.insert_user(user)

    # inference methods

    def get_inference_list_by_user_id(
        self, user_id: str
    ) -> Union[List[Inference], None]:
        return self._database.get_inference_list_by_user_id(user_id)

    def get_inference_by_id(self, inference_id: str) -> Union[Inference, None]:
        return self._database.get_inference_by_id(inference_id)

    def insert_inference(self, inference: Inference) -> None:
        return self._database.insert_inference(inference)

    # model methods

    def get_model_by_id(self, model_id: str) -> Union[Model, None]:
        return self._database.get_model_by_id(model_id)

    def get_model_list(self) -> Union[List[Model], None]:
        return self._database.get_model_list()

    # result methods

    def get_result_by_inference_id(self, inference_id: str) -> Union[Result, None]:
        return self._database.get_result_by_inference_id(inference_id)
