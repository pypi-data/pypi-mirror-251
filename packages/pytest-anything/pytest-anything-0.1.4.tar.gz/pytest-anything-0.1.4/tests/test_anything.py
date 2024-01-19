import pytest


def test_import():
    # this is just to satisfy coverage
    import sys

    del sys.modules["pytest_anything"]
    import pytest_anything


@pytest.mark.parametrize(
    "obj",
    [
        "string",
        123,
        123.1,
        True,
        False,
        [],
        {},
        (),
        object,
        object(),
        type,
        type(None),
        None,
    ],
)
def test_anything(obj, Anything):
    assert obj == Anything


@pytest.mark.parametrize(
    "obj",
    [
        "string",
        123,
        123.1,
        True,
        False,
        [],
        {},
        (),
        object,
        object(),
        type,
        type(None),
    ],
)
def test_something(obj, Something):
    assert obj == Something


def test_nothing(Something):
    assert Something != None and None != Something


def test_anything_repr(Anything):
    assert repr(Anything) == "Anything"


def test_something_repr(Something):
    assert repr(Something) == "Something"


def test_something_special(Something, mocker):
    special = mocker.Mock(return_value=True)
    obj = object()
    assert obj == Something(special)
    special.mock_assert_call_once_with(obj)


def test_something_special_false(Something):
    assert object() != Something(lambda x: False)


def test_something_special_repr(Something):
    r = repr(Something(lambda _: True))
    assert r.startswith("Something(") and r.endswith(")")


def test_something_special_fails(Something):
    # this fails if we get e.g. unhashable error
    with pytest.raises(AssertionError):
        assert {"a": 1, "b": 2} == {
            "a": 1,
            "b": Something(lambda x: isinstance(x, str)),
        }


def test_pprint_special(Something):
    import pprint

    foo = Something(lambda x: x is True)
    pprint.pformat(foo)
