import pytest
import flask
from flask import testing


@pytest.mark.parametrize('path', (
    '/account/settings',
    '/account/username',
    '/account/email',
    '/account/password',
    '/account/delete',
))
def test_login_required_get(client: testing.FlaskClient, path):
    response = client.get(path)
    assert response.headers["Location"] == "/auth/login"