from typing import Optional, List
from core.model.model import Model
from core.model.result import Result, ResultCreation
from core.model.user import User, UserCreation, UserWithPassword
from core.model.inference import Inference, InferenceCreation


class DatabasePort:
    def __init__(self, database_adapter):
        self._database_adapter = database_adapter

    # user methods

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        user = self._database_adapter.get_user_by_id(user_id)
        if user == None:
            return None
        return User(
            **{
                "id": str(user["_id"]),
                "username": user["username"],
                "email": user["email"],
            }
        )

    def get_user_by_username(self, username: str) -> Optional[User]:
        user = self._database_adapter.get_user_by_username(username)
        if user == None:
            return None
        return User(
            **{
                "id": str(user["_id"]),
                "username": user["username"],
                "email": user["email"],
            }
        )

    def get_user_by_username_with_password(
        self, username: str
    ) -> Optional[UserWithPassword]:
        user = self._database_adapter.get_user_by_username(username)
        if user == None:
            return None
        return UserWithPassword(
            **{
                "id": str(user["_id"]),
                "username": user["username"],
                "email": user["email"],
                "password": user["password"],
            }
        )

    def insert_user(self, new_user: UserCreation):
        self._database_adapter.insert_user(new_user)

    # inference methods

    def get_inference_by_id(
        self, inference_id: str, user_id: str
    ) -> Optional[Inference]:
        inference = self._database_adapter.get_inference_by_id(inference_id, user_id)
        if inference == None:
            return None
        return Inference(
            **{
                "id": str(inference["_id"]),
                "age": inference["age"],
                "sex": inference["sex"],
                "user_id": inference["user_id"],
                "model_id": inference["model_id"],
                "status": inference["status"],
            }
        )

    def get_inference_list(self, user_id: str) -> List[Inference]:
        inference_list = self._database_adapter.get_inference_list(user_id)
        return [
            Inference(
                **{
                    "id": str(inference["_id"]),
                    "age": inference["age"],
                    "sex": inference["sex"],
                    "user_id": inference["user_id"],
                    "model_id": inference["model_id"],
                    "status": inference["status"],
                }
            )
            for inference in inference_list
        ]

    def insert_inference(self, new_inference: InferenceCreation) -> str:
        return str(self._database_adapter.insert_inference(new_inference))

    def update_inference_status(self, inference_id: str, status: str):
        self._database_adapter.update_inference_status(inference_id, status)

    # model methods

    def get_model_by_id(self, model_id: str) -> Optional[Model]:
        model = self._database_adapter.get_model_by_id(model_id)
        if model == None:
            return None
        return Model(
            **{
                "id": str(model["_id"]),
                "name": model["name"],
                "receiving_channel": model["receiving_channel"],
                "publishing_channel": model["publishing_channel"],
            }
        )

    def get_model_list(self) -> List[Model]:
        model_list = self._database_adapter.get_model_list()
        return [
            Model(
                **{
                    "id": str(model["_id"]),
                    "name": model["name"],
                    "receiving_channel": model["receiving_channel"],
                    "publishing_channel": model["publishing_channel"],
                }
            )
            for model in model_list
        ]

    # result methods

    def get_result_by_inference_id(self, inference_id: str) -> Result:
        result = self._database_adapter.get_result_by_inference_id(inference_id)
        return Result(
            **{
                "id": str(result["_id"]),
                "inference_id": result["inference_id"],
                "output": result["output"],
                "diagnosis": result["diagnosis"],
            }
        )

    def insert_result(self, new_result: ResultCreation):
        self._database_adapter.insert_result(new_result)

    def update_result(self, result_update: ResultCreation):
        self._database_adapter.update_result(result_update)
