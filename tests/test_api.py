from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_reports_local_model():
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json()['local_first'] is True
    assert response.json()['provider'] == 'local Ollama / open-weight model'

def test_invalid_duration_is_rejected():
    response = client.post('/api/mission', json={'duration': 999})
    assert response.status_code == 422

def test_homepage_is_served():
    response = client.get('/')
    assert response.status_code == 200
    assert 'TouchGrass AI' in response.text
