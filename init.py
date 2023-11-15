from passlib.context import CryptContext
from pymongo import MongoClient
import os, sys

context_scheme=os.environ["context_scheme"]
deprecated=os.environ["deprecated"]
username = os.environ["BOOTSTRAP_MONGO_USER"]
password = os.environ["BOOTSTRAP_MONGO_PASSWORD"]
email = "spira-root@nowhere.com"
db_name = os.environ["DATABASE_NAME"]
user_col= os.environ["user_collection_name"]
model_col = os.environ["model_collection_name"]
inf_col = os.environ["inference_collection_name"]
results_col = os.environ["result_collection_name"]
hosp_col = os.environ["hospital_collection_name"]
conn_url=os.environ["M_CONN_URL"]

def main():
    pwd_context = CryptContext(schemes=[context_scheme], deprecated=deprecated)
    hashed_pwd=pwd_context.hash("password")


    conn=MongoClient(conn_url)
    db=getattr(conn, db_name)
    users=getattr(db, user_col)
    inferences=getattr(db, inf_col)
    models=getattr(db, model_col)
    results=getattr(db, results_col)
    hospitals=getattr(db, hosp_col)


    entry = {
        "email": email,
        "password": hashed_pwd,
        "username": username,
    }


    print("Attempting to crease user {}".format(entry["username"]), file=sys.stdout )

    users.insert_one(entry)
    print("Success", file=sys.stdout)

    print("Attempting to crease hospital {}".format(entry["hospital"]), file=sys.stdout )
    hospital = {
        "name": "einstein",
        "id": whatever,
    }
    hospitals.insert_one(hospital)

    print("Success", file=sys.stdout)

main()
