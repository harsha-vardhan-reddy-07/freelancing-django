from django.db import models

from db_connect import db

users_collection = db['users']

freelancer_collection = db['freelancer']

project_collection = db['projects']

application_collection = db['applications']