from pymongo import MongoClient
from bson import ObjectId
import os
from passlib.context import CryptContext

if __name__=="__main__":
  conn = MongoClient(os.environ["M_CONN_URL"])
  conn.drop_database(os.environ["DATABASE_NAME"])
  db = getattr(conn, os.environ["DATABASE_NAME"])
  models = getattr(db, os.environ["model_collection_name"])
  pwd_context = CryptContext(
      schemes=os.environ["context_scheme"], deprecated=os.environ["deprecated"]
  )

  models.insert_one({"_id": ObjectId("629e4f781ed5308d4b8212bc"),"name": "testmodel", "receiving_channel": "testtopic"})