from fastapi import APIRouter
from data.database import Database
from dotenv import load_dotenv
import os
from .users import router as users_router

load_dotenv(".env")
database = Database(os.environ["ME_CONFIG_MONGODB_URL"])
db = database.get_db(os.environ["MONGO_DB_NAME"])

router = APIRouter(prefix="/v1", tags=["v1"])

router.include_router(users_router)
