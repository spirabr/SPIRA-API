from typing import Optional, List
from core.model.hospital import Hospital
from core.model.model import Model, ModelCreationForm
from core.model.result import Result, ResultCreation
from core.model.user import User, UserCreation, UserWithPassword
from core.model.inference import Inference, InferenceCreation


class DatabasePort:
    """Port for the database adapter

    Args:
        database_adapter (Adapter Class) : database adapter instance

    """

    def __init__(self, database_adapter):
        self._database_adapter = database_adapter

    # user methods

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """gets the user object by the user id

        Args:
            user_id (str) : user id

        Returns:
            user object.
            if no user is found, None is returned.

        """
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
        """gets the user object by the username

        Args:
            username (str) : username

        Returns:
            user object.
            if no user is found, None is returned.

        """
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

    def get_user_by_email(self, email: str) -> Optional[User]:
        """gets the user object by the email

        Args:
            email (str) : email

        Returns:
            user object.
            if no user is found, None is returned.

        """
        user = self._database_adapter.get_user_by_email(email)
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
        """gets the user object with the password attribute by the username

        Args:
            username (str) : username

        Returns:
            user object with password attribute.
            if no user is found, None is returned.

        """
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
        """inserts a new user in the database

        Args:
            new_user (UserCreation) : new user form

        Returns:
            None

        """
        self._database_adapter.insert_user(new_user)

    # inference methods

    def get_inference_by_id(
        self, inference_id: str, user_id: str
    ) -> Optional[Inference]:
        """gets the inference object by the inference id and user id

        Args:
            inference_id (str) : inference id
            user_id (str) : user id

        Returns:
            inference object.
            if no inference is found, None is returned.

        """
        inference = self._database_adapter.get_inference_by_id(inference_id, user_id)
        if inference == None:
            return None
        return Inference(
            **{
                "id": str(inference["_id"]),
                "age": inference["age"],
                "gender": inference["gender"],
                "rgh": inference["rgh"],
                "covid_status": inference["covid_status"],
                "mask_type": inference["mask_type"],
                "local": inference["local"],
                "cid": inference["cid"],
                "bpm": inference["bpm"],
                "user_id": inference["user_id"],
                "model_id": inference["model_id"],
                "status": inference["status"],
                "created_in": inference["created_in"],
                "respiratory_frequency": inference["respiratory_frequency"],
                "respiratory_insufficiency_status": inference[
                    "respiratory_insufficiency_status"
                ],
                "location": inference["location"],
                "last_positive_diagnose_date": inference["last_positive_diagnose_date"],
                "hospitalized": inference["hospitalized"],
                "hospitalization_start": inference["hospitalization_start"],
                "hospitalization_end": inference["hospitalization_end"],
                "spo2": inference["spo2"],
            }
        )

    def get_inference_list(self, user_id: str) -> List[Inference]:
        """gets all inference objects of the user

        Args:
            user_id (str) : user id

        Returns:
            the list of inference objects

        """
        inference_list = self._database_adapter.get_inference_list(user_id)
        return [
            Inference(
                **{
                    "id": str(inference["_id"]),
                    "age": inference["age"],
                    "gender": inference["gender"],
                    "rgh": inference["rgh"],
                    "covid_status": inference["covid_status"],
                    "mask_type": inference["mask_type"],
                    "local": inference["local"],
                    "cid": inference["cid"],
                    "bpm": inference["bpm"],
                    "user_id": inference["user_id"],
                    "model_id": inference["model_id"],
                    "status": inference["status"],
                    "created_in": inference["created_in"],
                    "respiratory_frequency": inference["respiratory_frequency"],
                    "respiratory_insufficiency_status": inference[
                        "respiratory_insufficiency_status"
                    ],
                    "location": inference["location"],
                    "last_positive_diagnose_date": inference[
                        "last_positive_diagnose_date"
                    ],
                    "hospitalized": inference["hospitalized"],
                    "hospitalization_start": inference["hospitalization_start"],
                    "hospitalization_end": inference["hospitalization_end"],
                    "spo2": inference["spo2"],
                }
            )
            for inference in inference_list
        ]

    def insert_inference(self, new_inference: InferenceCreation) -> str:
        """inserts a new inference in the database

        Args:
            new_inference (InferenceCreation) : new inference form

        Returns:
            the id of the new inference

        """
        return str(self._database_adapter.insert_inference(new_inference))

    def update_inference_status(self, inference_id: str, status: str):
        """updates the status of an inference

        Args:
            inference_id (str) : inference id
            new_status (str) : new inference status

        Returns:
            None

        """
        self._database_adapter.update_inference_status(inference_id, status)

    # model methods

    def get_model_by_id(self, model_id: str) -> Optional[Model]:
        """gets the model object by the model id

        Args:
            model_id (str) : model id

        Returns:
            model object.
            if no model is found, None is returned.

        """
        model = self._database_adapter.get_model_by_id(model_id)
        if model == None:
            return None
        return Model(
            **{
                "id": str(model["_id"]),
                "name": model["name"],
                "publishing_channel": model["publishing_channel"],
            }
        )

    def get_model_list(self) -> List[Model]:
        """gets all model objects

        Args:
            None

        Returns:
            the list of model objects

        """
        model_list = self._database_adapter.get_model_list()
        return [
            Model(
                **{
                    "id": str(model["_id"]),
                    "name": model["name"],
                    "publishing_channel": model["publishing_channel"],
                }
            )
            for model in model_list
        ]

    def get_hospital_list(self) -> List[Model]:
        """gets all hospital objects

        Args:
            None

        Returns:
            the list of hospital objects

        """
        hospital_list = self._database_adapter.get_hospital_list()
        return [
            Hospital(
                **{
                    "id": str(hospital["_id"]),
                    "name": hospital["name"],
                }
            )
            for hospital in hospital_list
        ]

    def insert_model(self, new_model: ModelCreationForm):
        """inserts a new model in the database

        Args:
            new_model (ModelCreation) : new model form

        Returns:
            None

        """
        self._database_adapter.insert_model(new_model)

    def get_model_by_attribute(self, attribute, attribute_name: str):
        """gets model by attribute name

        Args:
            attribute
            attribute_name : str

        Returns:
            model object

        """
        model = self._database_adapter.get_model_by_attribute(attribute, attribute_name)
        if model == None:
            return None
        return Model(
            **{
                "id": str(model["_id"]),
                "name": model["name"],
                "publishing_channel": model["publishing_channel"],
            }
        )

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
        """inserts a new result object in the database

        Args:
            new_result (ResultCreation) : new result form

        Returns:
            None

        """
        self._database_adapter.insert_result(new_result)

    def update_result(self, result_update: ResultCreation):
        """updates a result object in the database

        Args:
            result_update (ResultUpdate) : result update form

        Returns:
            None

        """
        self._database_adapter.update_result(result_update)
