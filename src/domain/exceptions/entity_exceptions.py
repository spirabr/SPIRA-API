from os import stat
from typing import overload
from fastapi import status, HTTPException


class EntityExceptions:

    entity: str = "entity"

    @classmethod
    def get_id_not_found_exception(cls):
        return HTTPException(status.HTTP_404_NOT_FOUND, cls.entity + " not found")

    @classmethod
    def get_id_not_valid_exception(cls):
        return HTTPException(
            status.HTTP_400_BAD_REQUEST, cls.entity + " id is not valid"
        )

    @classmethod
    def get_list_exception(cls):
        return HTTPException(
            status.HTTP_400_BAD_REQUEST, "failed to retrieve " + cls.entity + " list"
        )

    @classmethod
    def get_registry_exception(cls):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to register new " + cls.entity,
            headers={"WWW-Authenticate": "Bearer"},
        )


class UserExceptions(EntityExceptions):
    entity: str = "user"


class InferenceExceptions(EntityExceptions):
    entity: str = "inference"


class ModelExceptions(EntityExceptions):
    entity: str = "model"
