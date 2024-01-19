




def test_core():

    url = 'http://localhost:18412'
    uuid = '760c6359-e28f-437c-aee4-409b83b604f8'

    from zww_test_package.core import sixvan

    all = sixvan.get_all(url, uuid)
    assert isinstance(all, dict)
    one = sixvan.get_one(url, uuid, '1')
    assert isinstance(one, dict)
    is_set = sixvan.set_one(url, uuid, id='1', payload={"function_code":16,"starting_address":40008,"value":"20,23"})
    assert is_set == 1
