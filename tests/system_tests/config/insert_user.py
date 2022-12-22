from pymongo import MongoClient
from bson import ObjectId
import os
from passlib.context import CryptContext

if __name__=="__main__":
  conn = MongoClient(os.environ["M_CONN_URL"])
  conn.drop_database(os.environ["DATABASE_NAME"])
  db = getattr(conn, os.environ["DATABASE_NAME"])
  users = getattr(db, os.environ["user_collection_name"])
  pwd_context = CryptContext(
      schemes=os.environ["context_scheme"], deprecated=os.environ["deprecated"]
  )

  users.insert_one({"_id": ObjectId("639686c4ba1604f1387a6c00"), "username": "testuser", "email": 'test@usp.br', "password": pwd_context.hash("abcdef")})