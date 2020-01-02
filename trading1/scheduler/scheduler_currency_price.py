from trading1.db.mongodb import mongodb_handler
from datetime import datetime
from trading1.machine.bithumb_machine import BithumbMachine
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))


if __name__ == "__main__":
    bithumb = BithumbMachine()
    result_etc = bithumb.get_filled_orders(currency_type="ETC")
    result_eth = bithumb.get_filled_orders(currency_type="ETH")
    result_btc = bithumb.get_filled_orders(currency_type="BTC")
    result_xrp = bithumb.get_filled_orders(currency_type="XRP")
    result_bch = bithumb.get_filled_orders(currency_type="BCH")
    result_btg = bithumb.get_filled_orders(currency_type="BTG")
    mongodb = mongodb_handler.MongoDBHandler("local", "coiner", "price_info")
    result_list = result_bch + result_btc + result_btg + result_etc + result_eth + result_xrp
    if len(result_list) != 0:
        for item in result_list:
            d = datetime.fromtimestamp(item["timestamp"]/1000)
            """TypeError: string indices must be integers
            21줄에서 이 에러가 생기는데 도저히 이유를 몰겠음... result는 분명 res.json()인데...
            https://twpower.github.io/124-python-requests-usage
            를 참고해도 마찬가지임..."""
            item["year"] = d.year
            item["month"] = d.month
            item["day"] = d.day
            item["hour"] = d.hour
            item["minute"] = d.minute
            item["second"] = d.second
            item["amount"] = float(item["amount"])
            item["timestamp"] /= 1000
            item.pop("tid")
        ids = mongodb.insert_items(result_list)
