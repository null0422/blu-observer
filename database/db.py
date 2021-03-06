import os
from pymongo import MongoClient


DB_HOST = os.environ['DB_OBSERVER_HOST']
DB_PORT = os.environ['DB_OBSERVER_PORT']
DB_NAME = os.environ['DB_OBSERVER_NAME']
DB_USER = os.environ['DB_OBSERVER_USER']
DB_PASSWORD = os.environ['DB_OBSERVER_PASSWORD']

class DataBase(object):
  def __init__(self):
    # self.client = MongoClient('mongodb://localhost:27017/')
    self.client = MongoClient('mongodb://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + ':' + DB_PORT)
    self.db = self.client[DB_NAME]


