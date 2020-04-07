'''
Tests for jwt flask app.
'''
import os
import json
import pytest

import main

SECRET = '123abc123abc1234'
TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODc0NzI5NjMsIm5iZiI6MTU4NjI2MzM2MywiZW1haWwiOiJ3b2xmQHRoZWRvb3IuY29tIn0.ACeK8_zJwzSsKNlyZjCYn4cfkXmVmSn8NfLXVQTd5lI'
EMAIL = 'wolf@thedoor.com'
PASSWORD = 'huff-puff'

@pytest.fixture
def client():
    os.environ['JWT_SECRET'] = SECRET
    main.APP.config['TESTING'] = True
    client = main.APP.test_client()

    yield client



def test_health(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == 'Healthy'

def test_404_health(client):
    response = client.get('/healthy')
    assert response.status_code == 404

def test_auth(client):
    body = {'email': EMAIL,
            'password': PASSWORD}
    response = client.post('/auth', 
                           data=json.dumps(body),
                           content_type='application/json')

    assert response.status_code == 200
    token = response.json['token']
    assert token is not None

def test_auth_error(client):
    body = {'email': EMAIL}
    response = client.post('/auth', 
                           data=json.dumps(body),
                           content_type='application/json')

    assert response.status_code == 400
    assert response.message=="Missing parameter:password"

    def test_auth_error(client):
    body = {'password': PASSWORD}
    response = client.post('/auth', 
                           data=json.dumps(body),
                           content_type='application/json')

    assert response.status_code == 400
    assert response.message=="Missing parameter:email"