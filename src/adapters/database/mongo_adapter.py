from pymongo import MongoClient
from bson import ObjectId

from core.model.inference import InferenceCreation
from core.model.model import ModelCreationForm
from core.model.result import ResultCreation, ResultUpdate
from core.model.user import UserCreation


class MongoAdapter:
    """Adapter for the mongoDB database

    Args:
        conn_url (str) : connection url to mongoDB container
        database_name (str) : name of the database used
        user_collection_name (str) : name of the collection referring to users
        inference_collection_name (str) : name of the collection referring to inferences
        model_collection_name (str) : name of the collection referring to models
        result_collection_name (str) : : name of the collection referring to results

    """

    def __init__(
        self,
        conn_url: str,
        database_name: str,
        user_collection_name: str,
        inference_collection_name: str,
        model_collection_name: str,
        result_collection_name: str,
    ):
        self._conn: MongoClient = MongoClient(conn_url)
        self._db = getattr(self._conn, database_name)
        self._users = getattr(self._db, user_collection_name)
        self._inferences = getattr(self._db, inference_collection_name)
        self._models = getattr(self._db, model_collection_name)
        self._results = getattr(self._db, result_collection_name)

    # user methods

    def get_user_by_id(self, user_id: str):
        """gets the user document by the user id

        Args:
            user_id (str) : user id

        Returns:
            user document.
            if no user is found, None is returned.

        """
        return self._users.find_one({"_id": ObjectId(user_id)})

    def get_user_by_username(self, username: str):
        """gets the user document by the username

        Args:
            username (str) : username

        Returns:
            user document.
            if no user is found, None is returned.

        """
        return self._users.find_one({"username": username})

    def get_user_by_email(self, email: str):
        """gets the user document by the email

        Args:
            email (str) : email

        Returns:
            user document.
            if no user is found, None is returned.

        """
        return self._users.find_one({"email": email})

    def insert_user(self, new_user: UserCreation):
        """inserts a new user document in the users collection

        Args:
            new_user (UserCreation) : new user form

        Returns:
            None

        """
        self._users.insert_one(new_user.dict())

    # model methods

    def get_model_by_id(self, model_id: str):
        """gets the model document by the model id

        Args:
            model_id (str) : model id

        Returns:
            model document.
            if no model is found, None is returned.

        """
        return self._models.find_one({"_id": ObjectId(model_id)})

    def get_model_list(self):
        """gets all model documents

        Args:
            None

        Returns:
            an iterator in the model documents

        """
        return self._models.find()

    def insert_model(self, new_model: ModelCreationForm):
        """inserts a new model document in the models collection

        Args:
            new_model (ModelCreationForm) : new model form

        Returns:
            None

        """
        self._models.insert_one(new_model.dict())

    def get_model_by_attribute(self, attribute, attribute_name: str):
        """gets the model document by the attribute

        Args:
            attribute
            attribute_name (str)

        Returns:
            model document.
            if no model is found, None is returned.

        """
        return self._models.find_one({attribute_name: attribute})

    # inference methods

    def get_inference_by_id(self, inference_id: str, user_id: str):
        """gets the inference document by the inference id and user id

        Args:
            inference_id (str) : inference id
            user_id (str) : user id

        Returns:
            inference document.
            if no inference is found, None is returned.

        """
        return self._inferences.find_one(
            {"_id": ObjectId(inference_id), "user_id": user_id}
        )

    def get_inference_list(self, user_id: str):
        """gets all inference documents of the user

        Args:
            user_id (str) : user id

        Returns:
            an iterator in the inference documents

        """
        return self._inferences.find({"user_id": user_id})

    def insert_inference(self, new_inference: InferenceCreation):
        """inserts a new inference document in the inferences collection

        Args:
            new_inference (InferenceCreation) : new inference form

        Returns:
            The ObjectId of the new document

        """
        _id = self._inferences.insert_one(new_inference.dict())
        return _id.inserted_id

    def update_inference_status(self, inference_id: str, new_status: str):
        """updates the status of an inference document

        Args:
            inference_id (str) : inference id
            new_status (str) : new inference status

        Returns:
            None

        """
        self._inferences.update_one(
            {"_id": ObjectId(inference_id)}, {"$set": {"status": new_status}}
        )

    # result methods

    def get_result_by_inference_id(self, inference_id: str):
        """gets the result document of an inference by the inference id

        Args:
            inference_id (str) : inference id

        Returns:
            result document.
            if no result is found, None is returned.

        """
        return self._results.find_one({"inference_id": inference_id})

    def insert_result(self, new_result: ResultCreation):
        """inserts a new result document in the results collection

        Args:
            new_result (ResultCreation) : new result form

        Returns:
            None

        """
        self._results.insert_one(new_result.dict())

    def update_result(self, result_update: ResultUpdate):
        """updates a result document

        Args:
            result_update (ResultUpdate) : result update form

        Returns:
            None

        """
        self._results.update_one(
            {"inference_id": result_update.inference_id}, {"$set": result_update.dict()}
        )
