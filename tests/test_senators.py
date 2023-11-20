from modules.apis.senators import *


def test_list_senators():
    senators = Senators()
    result = senators.list_senators()
    assert isinstance(result, list)


def test_by_state():
    senators = Senators()
    result = senators.by_state("SP")
    assert isinstance(result, list)
