Anything and Something fixtures for pytest
==========================================

If you ever had to ignore a certain part of an assertion, you would end up with
this.

.. code-block:: python

    import pytest


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
        assert None != Something


    def test_something_special(Something):
        assert object() == Something(lambda x: isinstance(x, object))
