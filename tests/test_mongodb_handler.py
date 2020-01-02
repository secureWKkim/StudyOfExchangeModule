import unittest, inspect
from trading1.db.mongodb.mongodb_handler import MongoDBHandler


class MongoDBHandlerTestCase(unittest.TestCase):
    """아래 테스트는 로컬 디비에 대해 테스트 케이스를 작성한 것이므로 실행할 경우 로컬 디비의 모든 내용이 삭제된다."""

    def setUp(self):
        self.mongodb = MongoDBHandler("local", "coiner", "price_info")
        self.mongodb.delete_items({})
        docs = [
            {"currency": "btc", "price": 10000},
            {"currency": "eth", "price": 1000},
            {"currency": "xrp", "price": 100},
            {"currency": "btc", "price": 20000},
            {"currency": "eth", "price": 2000},
            {"currency": "xrp", "price": 200}
        ]
        self.mongodb.insert_items(docs)

    def tearDown(self):
        pass

    def test_set_db_collection(self):
        print(inspect.stack([0][3]))
        self.mongodb.set_db_collection("trader","trade_status")
        self.assertEqual(self.mongodb.get_current_db_name(), "trader")
        self.assertEqual(self.mongodb.get_current_collection_name(), "trade_status")

    def test_get_db_name(self):
        print(inspect.stack([0][3]))
        dbname = self.mongodb.get_current_db_name()
        self.assertEqual(dbname, "coiner")

    def test_get_collection_name(self):
        print(inspect.stack([0][3]))
        collection_name = self.mongodb.get_current_collection_name()
        self.assertEqual(collection_name, "price_info")

    def test_insert_item(self):
        print(inspect.stack([0][3]))
        doc = {"item":"item0", "name":"test_insert_item"}
        id = self.mongodb.insert_item(doc)
        assert id
        print(id)

    def test_insert_items(self):
        print(inspect.stack([0][3]))
        doc = [
            {"item": "item1", "name": "test_insert_items"},
            {"item": "item2", "name": "test_insert_items"},
        ]
        id = self.mongodb.insert_items(doc)
        assert ids
        print(ids)

if __name__ == "__main__":
    unittest.main()
