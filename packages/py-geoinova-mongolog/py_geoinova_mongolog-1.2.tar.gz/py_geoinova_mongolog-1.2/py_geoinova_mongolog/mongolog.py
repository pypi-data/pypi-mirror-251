import datetime
import logging
import pymongo

from urllib.parse import quote

class MongoLogHandler(logging.Handler):
    @staticmethod
    def register(host, user, password):
        logger = logging.getLogger()
        mongo_handler = MongoLogHandler(host, user, password)
        logger.addHandler(mongo_handler)

    def __init__(self, host, user, password, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        password = quote(password)
        uri = f"mongodb://{user}:{password}@{host}:27017/admin"
        cliente = pymongo.MongoClient(uri)

        db = cliente["logs"]
        self.collection = db["log"]

    def emit(self, record):
        log_entry = {
            'level': record.levelname,
            'message': self.format(record),
            'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'logger_name': record.name,
        }

        self.collection.insert_one(log_entry)
