from modules.apis.deputies import *


def test_list_deputies():
    deputies = Deputies()
    result = deputies.list_deputies()
    assert isinstance(result, list)


def test_by_state():
    deputies = Deputies()
    result = deputies.by_state("SP")
    assert isinstance(result, list)
