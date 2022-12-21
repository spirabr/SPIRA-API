from pymongo import MongoClient
from bson import ObjectId
import os
from passlib.context import CryptContext

if __name__=="__main__":
  conn = MongoClient(os.environ["M_CONN_URL"])
  db = getattr(conn, os.environ["DATABASE_NAME"])
  models = getattr(db, os.environ["model_collection_name"])
  models.insert_one({"_id": ObjectId("629e4f781ed5308d4b8212bc"),"name": "testmodel", "publishing_channel": "testtopic"})