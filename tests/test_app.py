"""
Unit tests for Flask application
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


@pytest.fixture
def mock_env_api_key(monkeypatch):
    """Mock environment variable for API key"""
    monkeypatch.setenv('ABSTRACT_API_KEY', 'test_api_key_12345')


@pytest.fixture
def app(mock_env_api_key):
    """Create Flask app instance"""
    from app import app
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def mock_api_response():
    """Mock API response data"""
    return {
        'ip_address': '8.8.8.8',
        'city': 'Mountain View',
        'region': 'California',
        'country': 'United States',
        'country_code': 'US',
        'continent': 'North America',
        'postal_code': '94035',
        'latitude': 37.386,
        'longitude': -122.0838,
        'connection': {
            'isp_name': 'Google LLC',
            'organization_name': 'Google Public DNS',
            'autonomous_system_number': 15169,
            'autonomous_system_organization': 'GOOGLE',
            'connection_type': 'Corporate'
        },
        'timezone': {
            'name': 'America/Los_Angeles',
            'abbreviation': 'PST',
            'gmt_offset': -8,
            'current_time': '2025-11-24T10:30:00',
            'is_dst': False
        },
        'security': {
            'is_vpn': False,
            'is_proxy': False,
            'is_tor': False,
            'is_relay': False
        },
        'currency': {
            'currency_name': 'US Dollar',
            'currency_code': 'USD',
            'currency_symbol': '$'
        }
    }


class TestFlaskApp:
    """Test cases for Flask application"""
    
    def test_index_route(self, client):
        """Test index route renders template"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'IPeeps' in response.data
    
    @patch('app.api_client.get_current_ip_info')
    def test_get_current_ip_success(self, mock_get_info, client, mock_api_response):
        """Test successful current IP retrieval"""
        mock_get_info.return_value = mock_api_response
        
        response = client.get('/api/current-ip')
        json_data = response.get_json()
        
        assert response.status_code == 200
        assert json_data['success'] is True
        assert 'data' in json_data
        assert json_data['data']['basic']['IP Address'] == '8.8.8.8'
    
    @patch('app.api_client.get_current_ip_info')
    def test_get_current_ip_api_failure(self, mock_get_info, client):
        """Test current IP retrieval when API fails"""
        mock_get_info.return_value = None
        
        response = client.get('/api/current-ip')
        json_data = response.get_json()
        
        assert response.status_code == 500
        assert 'error' in json_data
    
    @patch('app.api_client.get_specific_ip_info')
    def test_lookup_ip_success(self, mock_get_info, client, mock_api_response):
        """Test successful specific IP lookup"""
        mock_get_info.return_value = mock_api_response
        
        response = client.post('/api/lookup-ip',
                              json={'ip_address': '8.8.8.8'},
                              content_type='application/json')
        json_data = response.get_json()
        
        assert response.status_code == 200
        assert json_data['success'] is True
        assert 'data' in json_data
    
    def test_lookup_ip_missing_address(self, client):
        """Test IP lookup with missing address"""
        response = client.post('/api/lookup-ip',
                              json={'ip_address': ''},
                              content_type='application/json')
        json_data = response.get_json()
        
        assert response.status_code == 400
        assert 'error' in json_data
    
    def test_lookup_ip_no_data(self, client):
        """Test IP lookup with no JSON data"""
        response = client.post('/api/lookup-ip',
                              json={},
                              content_type='application/json')
        json_data = response.get_json()
        
        assert response.status_code == 400
        assert 'error' in json_data
    
    @patch('app.api_client.get_specific_ip_info')
    def test_lookup_ip_api_failure(self, mock_get_info, client):
        """Test IP lookup when API fails"""
        mock_get_info.return_value = None
        
        response = client.post('/api/lookup-ip',
                              json={'ip_address': '1.1.1.1'},
                              content_type='application/json')
        json_data = response.get_json()
        
        assert response.status_code == 500
        assert 'error' in json_data
    
    @patch('app.api_client.test_connection')
    def test_test_connection_success(self, mock_test, client):
        """Test successful connection test"""
        mock_test.return_value = True
        
        response = client.get('/api/test-connection')
        json_data = response.get_json()
        
        assert response.status_code == 200
        assert json_data['success'] is True
        assert 'message' in json_data
    
    @patch('app.api_client.test_connection')
    def test_test_connection_failure(self, mock_test, client):
        """Test failed connection test"""
        mock_test.return_value = False
        
        response = client.get('/api/test-connection')
        json_data = response.get_json()
        
        assert response.status_code == 500
        assert json_data['success'] is False
