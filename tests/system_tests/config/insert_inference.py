from pymongo import MongoClient
from bson import ObjectId
import os
from passlib.context import CryptContext

if __name__=="__main__":
  conn = MongoClient(os.environ["M_CONN_URL"])
  db = getattr(conn, os.environ["DATABASE_NAME"])
  inferences = getattr(db, os.environ["inference_collection_name"])
  inferences.insert_one({
    "_id": ObjectId('638f56f70acda5864ee0203a'),
    "model_id": '629e4f781ed5308d4b8212bc',
    "rgh": '12345678',
    "mask_type": 'THICK',
    "gender": 'Feminino',
    "covid_status": 'TRUE',
    "local": 'Outro',
    "age": 23,
    "cid": '12345',
    "bpm": '17',
    "respiratory_frequency": '13',
    "respiratory_insufficiency_status": 'true',
    "location": "location",
    "last_positive_diagnose_date": '2022-12-01',
    "hospitalized": 'true',
    "hospitalization_start": '2022-12-02',
    "hospitalization_end": '2022-12-05',
    "spo2": '23',
    "status": 'completed',
    "user_id": '639686c4ba1604f1387a6c00',
    "created_in": '2022-12-06 14:51:35.771148'
  })

  inferences.insert_one({
    "_id": ObjectId('638f56f70acda5864ee0203b'),
    "model_id": '629e4f781ed5308d4b8212bc',
    "rgh": '12345678',
    "mask_type": 'THICK',
    "gender": 'Feminino',
    "covid_status": 'TRUE',
    "local": 'Outro',
    "age": 23,
    "cid": '12345',
    "bpm": '17',
    "respiratory_frequency": '13',
    "respiratory_insufficiency_status": 'true',
    "location": "location",
    "last_positive_diagnose_date": '2022-12-01',
    "hospitalized": 'true',
    "hospitalization_start": '2022-12-02',
    "hospitalization_end": '2022-12-05',
    "spo2": '23',
    "status": 'completed',
    "user_id": '639686c4ba1604f1387a6c01',
    "created_in": '2022-12-06 14:51:35.771148'
  })