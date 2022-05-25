import os
from fastapi import APIRouter, status, HTTPException
from data.database import Database
from dotenv import load_dotenv
from bson.objectid import ObjectId

from .utils.helpers import user_helper

router = APIRouter(prefix="/users", tags=["users"])

load_dotenv(".env")
database = Database(os.environ["ME_CONFIG_MONGODB_URL"])
db = database.get_db(os.environ["MONGO_DB_NAME"])


@router.get("/{user_id}")
def get_user_by_id(user_id: str):
    try:
        user = user_helper(db.users.find_one({"_id": ObjectId(user_id)}))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="user id not valid"
        )
    if user != None:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
