import json
import requests
import time

import pytest

BASE_URL = "http://127.0.0.1:5000/"


def add_product(stamp, price):
    """
    Add product via API
    :param stamp: str, unique string added to name for better indentification
    :param price: str, price of a product
    """
    product_name = "Bread_" + str(stamp)
    payload = {"name":product_name,"price":str(price),"id":""}
    headers = {'content-type': 'application/json'}

    response = requests.post(
        BASE_URL + "products", data=json.dumps(payload), headers=headers
    )

    return response

def get_product(product_id):
    """
    Get product via API
    :param product_id: str
    """
    headers = {'accept': 'application/json'}

    response = requests.get(
        BASE_URL + "products/{}".format(product_id), headers=headers
    )

    if not 200 <= response.status_code <= 209:
        raise AssertionError(
            "Cannot get product from this id. Error: {}".format(response.status_code)
        )

    return response


def get_fresh_product():
    """
    Get the newest product via API
    Returns product id in response
    """
    headers = {'accept': 'application/json'}

    response = requests.get(
        BASE_URL + "products/newest_id", headers=headers
    )

    if not 200 <= response.status_code <= 209:
        raise AssertionError(
            "Cannot get the fresh product. Error: {}".format(response.status_code)
        )

    return response


class TestProductFeature(object):

    def test_adding_product(self):
        stamp = str(time.time())
        price = str(3)
        assert add_product(stamp, price).status_code == 200

    def test_product_name(self):
        stamp = str(time.time())
        price = str(3)
        product_id = add_product(stamp, price).json()["id"]
        assert get_product(product_id).json()["name"] == 'Bread_' + stamp

    def test_product_price(self):
        stamp = str(time.time())
        price = str(2.5)
        product_id = add_product(stamp, price).json()["id"]
        assert get_product(product_id).json()["price"] == price

    def test_check_fresh_product(self):
        stamp = str(time.time())
        price = str(8)
        assert add_product(stamp, price).json()["id"] == get_fresh_product().json()["id"]
