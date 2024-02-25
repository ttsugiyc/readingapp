import pytest
import flask
from flask import testing


@pytest.mark.parametrize('path', (
    '/admin',
    '/admin/1/update',
    '/admin/1/username',
    '/admin/1/email',
    '/admin/1/password',
    '/admin/settings',
))
def test_login_required_get(client: testing.FlaskClient, path):
    response = client.get(path)
    print(response.headers)
    assert response.headers['Location'] == '/admin/login'


@pytest.mark.parametrize('path', (
    '/admin',
    '/admin/1/username',
    '/admin/1/email',
    '/admin/1/password',
    '/admin/1/delete',
    '/admin/settings',
))
def test_login_required_post(client: testing.FlaskClient, path):
    response = client.post(path)
    assert response.headers['Location'] == '/admin/login'