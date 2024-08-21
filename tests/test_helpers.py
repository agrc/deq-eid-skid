from deq_eid.helpers import convert_to_int


def test_convert_to_int_with_valid_string():
    assert convert_to_int("123") == 123


def test_convert_to_int_with_invalid_string():
    assert convert_to_int("abc") == -1


def test_convert_to_int_with_none():
    assert convert_to_int(None) is None


def test_convert_to_int_with_empty_string():
    assert convert_to_int("") == -1
