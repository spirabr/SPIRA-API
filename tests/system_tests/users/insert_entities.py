from pymongo import MongoClient
from bson import ObjectId
import os

if __name__=="__main__":
  conn = MongoClient(os.environ["M_CONN_URL"])
  db = getattr(conn, "test_db")
  users = getattr(db, 'users')
  users.insert_one({"_id": ObjectId(),"usrname": "testuser", "password":"$2b$12$GDKvKclqoVN1ExHIcIR5UODd3v3q5zfA2yK6reVJ.SAq385.a0OuW"})

  