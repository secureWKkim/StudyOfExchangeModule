# -*- coding: utf-8 -*-
from pymongo import MongoClient
from pymongo.cursor import CursorType
import configparser
from trading1.db.base_handler import DBHandler


class MongoDBHandler(DBHandler):
    """
    pymongo 를 래핑해서 사용하는 클래스입니다. DBHandler 추상 클래스를 상속합니다.
    리모트 DB 와 로컬 DB 에서 모두 사용할 수 있도록 __init__에서 mode 로 구분합니다.
    """
    def __init__(self, mode="local", db_name=None, collection_name=None):
        if db_name is None or collection_name is None:
            raise Exception("Need to db name and collection name")
        config = configparser.ConfigParser()
        config.read('conf/config.ini')
        self.db_config = {}
        self.db_config["local_ip"] = config['MONGODB']['local_ip']
        self.db_config["port"] = config['MONGODB']['port']
        self.db_config["remote_host"] = config['MONGODB']['remote_host']
        # self.db_config["remote_port"] = config['MONGODB']['remote_port']
        self.db_config["user"] = config['MONGODB']['user']
        self.db_config["password"] = config['MONGODB']['password']

        if mode == "remote":
            self._client = MongoClient("mongodb://{user}:{password}@{remote_host}:{port}".format(**self.db_config))
        elif mode == "local":
            self._client = MongoClient("mongodb://{user}:{password}@{local_ip}:{port}".format(**self.db_config))

        self._db = self._client[db_name]
        self._collection = self._db[collection_name]

    def set_db_collection(self, db_name=None, collection_name=None):
        """mongodb 에서 작업하려는 데베와 컬렉션을 변경할 때 사용합니다."""
        if db_name is None:
            raise Exception("Need to dbname name")

        self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]

    def get_current_db_name(self):
        return self._db.name

    def get_current_collection_name(self):
        return self._collection.name

    def insert_item(self, data, db_name=None, collection_name=None):
        if db_name is None:
            self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]
        return self._collection.insert_one(data).inserted_id

    def insert_items(self, datas, db_name=None, collection_name=None):
        if db_name is not None:
            self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]
        return self._collection.insert_many(datas).inserted_ids

    def find_items(self, condition=None, db_name=None, collection_name=None):
        """condition 은 검색 조건을 일컬? 컫? 음"""
        if condition is None:
            condition = {}
        if db_name is not None:
            self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]
        return self._collection.find(condition, no_cursor_timeout=True, cursor_type=CursorType.EXHAUST)

    def find_item(self, condition=None, db_name=None, collection_name=None):
        if condition is None:
            condition = {}
        if db_name is not None:
            self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]
        return self._collection.find_one(condition)

    def delete_items(self, condition=None, db_name=None, collection_name=None):
        """
        MongoDB 에 다수의 document 를 삭제하기 위한 몌소드입니다.

        Args:
            condition (dict): 삭제 조건을 dictionary 형태로 받습니다.
            db_name (str): MongoDB 에서 database 에 해당하는 이름을 받습니다.
            collection_name (str): database 에 속하는 collection 이름을 받습니다.

        Returns:
            DeleteResult : PyMongo 의 문서의 삭제 결과 객체 DeleteResult 가 반환됩니다.
        """
        if condition is None:
            raise Exception("Need to condition")
        if db_name is not None:
            self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]
        return self._collection.delete_many(condition)

    def update_items(self, condition=None, update_value=None, db_name=None, collection_name=None):
        """
        MongoDB에 다수의 document 를 갱신하기 위한 메소드입니다.

        Args:
            condition (dict): 갱신 조건을 dictionary 형태로 받습니다.
            update_value (dict) : 깽신하고자 하는 값을 dictionary 형태로 받습니다.
            db_name (str): MongoDB 에서 database 에 해당하는 이름을 받습니다.
            collection_name (str): database 에 속하는 collection 이름을 받습니다.

        Returns:
            UpdateResult : PyMongo 의 문서의 갱신 결과 객체 UpdateResult 가 반환됩니다.
        """
        if condition is None:
            raise Exception("Need to condition")
        if update_value is None:
            raise Exception("Need to update value")
        if db_name is not None:
            self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]
        return self._collection.update_many(filter=condition, update=update_value)

    def aggregate(self, pipeline=None, db_name=None, collection_name=None):
        """
        MongoDB의 aggregate 작업을 위한 메소드 입니다.

        Args:
            pipeline (dict): 갱신 조건을 dictionary 형태로 받습니다.
            db_name (str): MongoDB 에서 database 에 해당하는 이름을 받습니다.
            collection_name (str): database 에 속하는 collection 이름을 받습니다.

        Returns:
            CommandCursor : PyMongo 의 CommandCursor 가 반환됩니다.
        """
        if pipeline is None:
            raise Exception("Need to pipeline")
        if db_name is not None:
            self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]
        return self._collection.aggregate(pipeline)
