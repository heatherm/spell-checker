"""
You can auto-discover and run all tests with this command:

    $ pytest

Documentation:

* https://docs.pytest.org/en/latest/
* https://docs.pytest.org/en/latest/fixture.html
* http://flask.pocoo.org/docs/latest/testing/
"""

import pytest
from flask import Flask

import app


@pytest.fixture
def app():
    app = Flask(__name__)
    app = app.create_app()
    app.debug = True
    return app.test_client()


def test_register(app):
    res = app.get("/register")
    assert res.status_code == 200
    assert b"Register" in res.data


def test_login(app):
    res = app.get("/login")
    assert res.status_code == 200
    assert b"Login" in res.data
