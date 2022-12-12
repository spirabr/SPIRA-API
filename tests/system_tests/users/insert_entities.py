from pymongo import MongoClient
from bson import ObjectId
import os

if __name__=="__main__":
  conn = MongoClient(os.environ["M_CONN_URL"])
  db = getattr(conn, "test_db")
  users = getattr(db, 'users')
  users.insert_one({"_id": ObjectId(),"username": "testuser", "password":"$2b$12$lEzFDjlCDRLc3js6lORnXOq5L8LQRuJQ1MXFWBNuCHgd3iugeRksO"})

  