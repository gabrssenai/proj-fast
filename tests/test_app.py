from http import HTTPStatus

from fastapi.testclient import TestClient

from proj_fast.app import app


def test_ok_ola():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá, Mundo!'}

def test_read_html(client):
    response = client.get('/html')

    assert response.status_code == HTTPStatus.OK
    assert response.text == '<h1> Olá Mundo!</h1>'

def test_create_user(client):
    response = client.post(
        '/user/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
            'id': 1,
            'username': 'alice',
            'email': 'alice@example.com',
    }