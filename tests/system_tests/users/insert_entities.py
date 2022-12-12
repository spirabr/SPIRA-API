from pymongo import MongoClient
from bson import ObjectId
import os
from passlib.context import CryptContext

if __name__=="__main__":
  print(os.environ["context_scheme"])
  conn = MongoClient(os.environ["M_CONN_URL"])
  conn.drop_database("test_db")
  db = getattr(conn, "test_db")
  users = getattr(db, 'users')
  pwd_context = CryptContext(
      schemes=os.environ["context_scheme"], deprecated=os.environ["deprecated"]
  )

  users.insert_one({"_id": ObjectId(),"username": "testuser", "email": 'test@usp.br', "password": pwd_context.hash("abcdef")})

  print(users.find_one())

  