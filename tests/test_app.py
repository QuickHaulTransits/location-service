import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Import the app from the location service
from app import app

client = TestClient(app)

def test_health_check_healthy():
    # Mock redis ping to succeed
    with patch('app.redis_client.ping', return_value=True):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy", "redis": "connected"}

def test_health_check_unhealthy():
    # Mock redis ping to raise an exception
    with patch('app.redis_client.ping', side_effect=Exception("Connection error")):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "unhealthy", "redis": "disconnected"}

@patch('app.redis_client.get')
@patch('app.get_all_states')
def test_get_states_no_cache(mock_get_all_states, mock_redis_get):
    # Setup mocks: cache miss
    mock_redis_get.return_value = None
    
    mock_states_data = [{"id": "S1", "name": "State 1"}, {"id": "S2", "name": "State 2"}]
    mock_get_all_states.return_value = mock_states_data
    
    with patch('app.redis_client.setex') as mock_redis_setex:
        response = client.get("/states")
        
        assert response.status_code == 200
        assert response.json() == mock_states_data
        mock_get_all_states.assert_called_once()
        mock_redis_setex.assert_called_once()

@patch('app.redis_client.get')
def test_get_states_with_cache(mock_redis_get):
    # Setup mocks: cache hit
    cached_data = '[{"id": "S1", "name": "State 1"}]'
    mock_redis_get.return_value = cached_data
    
    with patch('app.get_all_states') as mock_get_all_states:
        response = client.get("/states")
        
        assert response.status_code == 200
        assert response.json() == [{"id": "S1", "name": "State 1"}]
        mock_get_all_states.assert_not_called()

def test_get_districts_missing_param():
    response = client.get("/districts")
    assert response.status_code == 400
    assert "State parameter is required" in response.text

@patch('app.redis_client.get')
@patch('app.get_districts_by_state')
def test_get_districts_no_cache(mock_get_districts, mock_redis_get):
    mock_redis_get.return_value = None
    mock_get_districts.return_value = [{"id": "D1", "name": "District 1"}]
    
    with patch('app.redis_client.setex'):
        response = client.get("/districts?state=S1")
        assert response.status_code == 200
        assert response.json() == [{"id": "D1", "name": "District 1"}]

@patch('app.redis_client.get')
@patch('app.get_districts_by_state')
def test_get_districts_not_found(mock_get_districts, mock_redis_get):
    mock_redis_get.return_value = None
    mock_get_districts.return_value = None
    
    response = client.get("/districts?state=INVALID")
    assert response.status_code == 404
    assert "State not found" in response.text

def test_get_centers_missing_param():
    response = client.get("/centers")
    assert response.status_code == 400
    
    response = client.get("/centers?state=S1")
    assert response.status_code == 400

@patch('app.redis_client.get')
@patch('app.get_centers_by_district')
def test_get_centers_no_cache(mock_get_centers, mock_redis_get):
    mock_redis_get.return_value = None
    mock_get_centers.return_value = [{"id": "C1", "name": "Center 1"}]
    
    with patch('app.redis_client.setex'):
        response = client.get("/centers?state=S1&district=D1")
        assert response.status_code == 200
        assert response.json() == [{"id": "C1", "name": "Center 1"}]

@patch('app.redis_client.keys')
@patch('app.redis_client.delete')
def test_clear_cache(mock_delete, mock_keys):
    mock_keys.return_value = ["states", "districts:S1"]
    
    response = client.delete("/cache")
    assert response.status_code == 200
    assert "Cleared" in response.text
    mock_delete.assert_called_once()
