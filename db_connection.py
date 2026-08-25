import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.uri_parser import parse_uri

load_dotenv()


def get_database(allow_mutation=False):
    if allow_mutation and os.getenv('ALLOW_DB_MUTATIONS', '').lower() not in {'1', 'true', 'yes', 'on'}:
        raise RuntimeError('Database mutations are disabled. Set ALLOW_DB_MUTATIONS=true for an intentional run')

    mongo_uri = os.getenv('MONGO_URI') or os.getenv('CUSTOMCONNSTR_MONGO_URI')
    if not mongo_uri:
        raise RuntimeError('MONGO_URI must be configured before running database scripts')

    database_name = os.getenv('MONGO_DB_NAME') or os.getenv('DATABASE_NAME')
    if not database_name:
        database_name = parse_uri(mongo_uri).get('database') or 'online_course_platform'
    return MongoClient(mongo_uri)[database_name]