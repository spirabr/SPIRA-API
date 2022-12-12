from pymongo import MongoClient
from bson import ObjectId
import os
from passlib.context import CryptContext

if __name__=="__main__":
  conn = MongoClient(os.environ["M_CONN_URL"])
  db = getattr(conn, "test_db")
  users = getattr(db, 'users')
  pwd_context = CryptContext(
      schemes=os.environ["context_scheme"], deprecated=os.environ["deprecated"]
  )

  users.insert_one({"_id": ObjectId(),"username": "testuser", "password":pwd_context.hash("123")})

  