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
