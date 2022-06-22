from pymongo import MongoClient
from bson import ObjectId

from core.model.inference import InferenceCreation
from core.model.result import ResultCreation
from core.model.user import UserCreation


class MongoAdapter:
    def __init__(
        self,
        conn_url,
        database_name,
        user_collection_name,
        inference_collection_name,
        model_collection_name,
        result_collection_name,
    ):
        self._conn = MongoClient(conn_url)
        self._db = getattr(self._conn, database_name)
        self._users = getattr(self._db, user_collection_name)
        self._inferences = getattr(self._db, inference_collection_name)
        self._models = getattr(self._db, model_collection_name)
        self._results = getattr(self._db, result_collection_name)

    # user methods

    def get_user_by_id(self, user_id: str):
        return self._users.find_one({"_id": ObjectId(user_id)})

    def get_user_by_username(self, username: str):
        return self._users.find_one({"username": username})

    def insert_user(self, new_user: UserCreation):
        self._users.insert_one(new_user.dict())

    # model methods

    def get_model_by_id(self, model_id: str):
        return self._models.find_one({"_id": ObjectId(model_id)})

    def get_model_list(self):
        return self._models.find()

    # inference methods

    def get_inference_by_id(self, inference_id: str, user_id: str):
        return self._inferences.find_one(
            {"_id": ObjectId(inference_id), "user_id": user_id}
        )

    def get_inference_list(self, user_id: str):
        return self._inferences.find({"user_id": user_id})

    def insert_inference(self, new_inference: InferenceCreation):
        _id = self._inferences.insert_one(new_inference.dict())
        return _id.inserted_id

    # result methods

    def get_result_by_inference_id(self, inference_id: str):
        return self._results.find_one({"inference_id": inference_id})

    def insert_result(self, new_result: ResultCreation):
        self._results.insert_one(new_result.dict())
