"""
Unit tests for AbstractAPIClient module
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from api_client import AbstractAPIClient


class TestAbstractAPIClient:
    """Test cases for AbstractAPIClient class"""
    
    @pytest.fixture
    def mock_env_api_key(self, monkeypatch):
        """Mock environment variable for API key"""
        monkeypatch.setenv('ABSTRACT_API_KEY', 'test_api_key_12345')
    
    @pytest.fixture
    def client(self, mock_env_api_key):
        """Create API client instance"""
        return AbstractAPIClient()
    
    @pytest.fixture
    def mock_response_success(self):
        """Mock successful API response"""
        return {
            'ip_address': '8.8.8.8',
            'city': 'Mountain View',
            'country': 'United States'
        }
    
    def test_init_with_api_key(self, mock_env_api_key):
        """Test initialization with valid API key"""
        client = AbstractAPIClient()
        assert client.api_key == 'test_api_key_12345'
        assert client.base_url == 'https://ipgeolocation.abstractapi.com/v1/'
        assert client.timeout == 10
    
    def test_init_without_api_key(self, monkeypatch):
        """Test initialization without API key raises error"""
        monkeypatch.delenv('ABSTRACT_API_KEY', raising=False)
        
        with pytest.raises(ValueError, match="ABSTRACT_API_KEY not found"):
            AbstractAPIClient()
    
    @patch('api_client.requests.get')
    def test_get_current_ip_info_success(self, mock_get, client, mock_response_success):
        """Test successful current IP info retrieval"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response_success
        
        result = client.get_current_ip_info()
        
        assert result == mock_response_success
        assert mock_get.called
        assert 'api_key=test_api_key_12345' in mock_get.call_args[0][0]
    
    @patch('api_client.requests.get')
    def test_get_current_ip_info_401_error(self, mock_get, client, capsys):
        """Test 401 unauthorized error"""
        mock_get.return_value.status_code = 401
        
        result = client.get_current_ip_info()
        
        assert result is None
        captured = capsys.readouterr()
        assert 'Invalid API key' in captured.out
    
    @patch('api_client.requests.get')
    def test_get_current_ip_info_429_error(self, mock_get, client, capsys):
        """Test 429 rate limit error"""
        mock_get.return_value.status_code = 429
        
        result = client.get_current_ip_info()
        
        assert result is None
        captured = capsys.readouterr()
        assert 'rate limit exceeded' in captured.out
    
    @patch('api_client.requests.get')
    def test_get_current_ip_info_other_error(self, mock_get, client, capsys):
        """Test other HTTP errors"""
        mock_get.return_value.status_code = 500
        
        result = client.get_current_ip_info()
        
        assert result is None
        captured = capsys.readouterr()
        assert 'status code 500' in captured.out
    
    @patch('api_client.requests.get')
    def test_get_current_ip_info_timeout(self, mock_get, client, capsys):
        """Test timeout error"""
        mock_get.side_effect = __import__('requests').exceptions.Timeout()
        
        result = client.get_current_ip_info()
        
        assert result is None
        captured = capsys.readouterr()
        assert 'timed out' in captured.out
    
    @patch('api_client.requests.get')
    def test_get_current_ip_info_connection_error(self, mock_get, client, capsys):
        """Test connection error"""
        mock_get.side_effect = __import__('requests').exceptions.ConnectionError()
        
        result = client.get_current_ip_info()
        
        assert result is None
        captured = capsys.readouterr()
        assert 'Could not connect' in captured.out
    
    @patch('api_client.requests.get')
    def test_get_specific_ip_info_success(self, mock_get, client, mock_response_success):
        """Test successful specific IP lookup"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response_success
        
        result = client.get_specific_ip_info('8.8.8.8')
        
        assert result == mock_response_success
        assert 'ip_address=8.8.8.8' in mock_get.call_args[0][0]
    
    def test_get_specific_ip_info_invalid_format(self, client, capsys):
        """Test invalid IP address format"""
        result = client.get_specific_ip_info('')
        
        assert result is None
        captured = capsys.readouterr()
        assert 'Invalid IP address format' in captured.out
    
    def test_get_specific_ip_info_not_string(self, client, capsys):
        """Test non-string IP address"""
        result = client.get_specific_ip_info(None)
        
        assert result is None
        captured = capsys.readouterr()
        assert 'Invalid IP address format' in captured.out
    
    @patch('api_client.requests.get')
    def test_get_specific_ip_info_422_error(self, mock_get, client, capsys):
        """Test 422 invalid IP error"""
        mock_get.return_value.status_code = 422
        
        result = client.get_specific_ip_info('invalid.ip')
        
        assert result is None
        captured = capsys.readouterr()
        assert 'Invalid IP address format' in captured.out
    
    @patch('api_client.requests.get')
    def test_test_connection_success(self, mock_get, client, capsys):
        """Test successful connection test"""
        mock_get.return_value.status_code = 200
        
        result = client.test_connection()
        
        assert result is True
        captured = capsys.readouterr()
        assert 'connection successful' in captured.out
    
    @patch('api_client.requests.get')
    def test_test_connection_failure(self, mock_get, client, capsys):
        """Test failed connection test"""
        mock_get.return_value.status_code = 401
        
        result = client.test_connection()
        
        assert result is False
        captured = capsys.readouterr()
        assert 'connection failed' in captured.out
    
    @patch('api_client.requests.get')
    def test_test_connection_exception(self, mock_get, client, capsys):
        """Test connection test with exception"""
        mock_get.side_effect = Exception('Network error')
        
        result = client.test_connection()
        
        assert result is False
        captured = capsys.readouterr()
        assert 'Connection test failed' in captured.out
