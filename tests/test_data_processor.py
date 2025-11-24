"""
Unit tests for DataProcessor module
"""

import pytest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_processor import DataProcessor


class TestDataProcessor:
    """Test cases for DataProcessor class"""
    
    @pytest.fixture
    def sample_api_response(self):
        """Sample API response for testing"""
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
    
    def test_validate_response_valid(self, sample_api_response):
        """Test validation with valid response"""
        assert DataProcessor.validate_response(sample_api_response) is True
    
    def test_validate_response_none(self):
        """Test validation with None"""
        assert DataProcessor.validate_response(None) is False
    
    def test_validate_response_empty(self):
        """Test validation with empty dict"""
        assert DataProcessor.validate_response({}) is False
    
    def test_validate_response_missing_required_field(self):
        """Test validation with missing required field"""
        assert DataProcessor.validate_response({'city': 'Test'}) is False
    
    def test_extract_basic_info(self, sample_api_response):
        """Test basic info extraction"""
        result = DataProcessor.extract_basic_info(sample_api_response)
        
        assert result['IP Address'] == '8.8.8.8'
        assert result['IP Version'] == 'IPv4'
        assert result['City'] == 'Mountain View'
        assert result['Region'] == 'California'
        assert result['Country'] == 'United States'
        assert result['Country Code'] == 'US'
        assert result['Continent'] == 'North America'
        assert result['Postal Code'] == '94035'
        assert result['Latitude'] == '37.386'
        assert result['Longitude'] == '-122.0838'
    
    def test_extract_basic_info_missing_fields(self):
        """Test basic info extraction with missing fields"""
        result = DataProcessor.extract_basic_info({'ip_address': '1.1.1.1'})
        
        assert result['IP Address'] == '1.1.1.1'
        assert result['City'] == 'N/A'
        assert result['Region'] == 'N/A'
    
    def test_extract_connection_info(self, sample_api_response):
        """Test connection info extraction"""
        result = DataProcessor.extract_connection_info(sample_api_response)
        
        assert result['ISP'] == 'Google LLC'
        assert result['Organization'] == 'Google Public DNS'
        assert result['ASN'] == '15169'
        assert result['ASN Organization'] == 'GOOGLE'
        assert result['Connection Type'] == 'Corporate'
    
    def test_extract_connection_info_missing_connection(self):
        """Test connection info extraction with missing connection data"""
        result = DataProcessor.extract_connection_info({'ip_address': '1.1.1.1'})
        
        assert result['ISP'] == 'N/A'
        assert result['Organization'] == 'N/A'
    
    def test_extract_timezone_info(self, sample_api_response):
        """Test timezone info extraction"""
        result = DataProcessor.extract_timezone_info(sample_api_response)
        
        assert result['Timezone Name'] == 'America/Los_Angeles'
        assert result['Abbreviation'] == 'PST'
        assert result['GMT Offset'] == '-8'
        assert result['Current Time'] == '2025-11-24T10:30:00'
        assert result['Is DST'] == 'False'
    
    def test_extract_security_info_clean(self, sample_api_response):
        """Test security info extraction for clean IP"""
        result = DataProcessor.extract_security_info(sample_api_response)
        
        assert result['Is VPN'] is False
        assert result['Is Proxy'] is False
        assert result['Is Tor'] is False
        assert result['Is Relay'] is False
        assert result['Threat Level'] == 'Clean'
    
    def test_extract_security_info_vpn_detected(self, sample_api_response):
        """Test security info extraction with VPN detected"""
        sample_api_response['security']['is_vpn'] = True
        result = DataProcessor.extract_security_info(sample_api_response)
        
        assert result['Is VPN'] is True
        assert 'VPN' in result['Threat Level']
        assert 'Low' in result['Threat Level']
    
    def test_extract_security_info_multiple_threats(self, sample_api_response):
        """Test security info extraction with multiple threats"""
        sample_api_response['security']['is_vpn'] = True
        sample_api_response['security']['is_proxy'] = True
        result = DataProcessor.extract_security_info(sample_api_response)
        
        assert 'Medium' in result['Threat Level']
    
    def test_extract_currency_info(self, sample_api_response):
        """Test currency info extraction"""
        result = DataProcessor.extract_currency_info(sample_api_response)
        
        assert result['Currency Name'] == 'US Dollar'
        assert result['Currency Code'] == 'USD'
        assert result['Currency Symbol'] == '$'
    
    def test_process_all_data(self, sample_api_response):
        """Test processing all data"""
        result = DataProcessor.process_all_data(sample_api_response)
        
        assert 'basic' in result
        assert 'connection' in result
        assert 'timezone' in result
        assert 'security' in result
        assert 'currency' in result
        
        assert result['basic']['IP Address'] == '8.8.8.8'
        assert result['connection']['ISP'] == 'Google LLC'
        assert result['timezone']['Timezone Name'] == 'America/Los_Angeles'
        assert result['security']['Threat Level'] == 'Clean'
        assert result['currency']['Currency Code'] == 'USD'
    
    def test_process_all_data_invalid(self):
        """Test processing invalid data"""
        result = DataProcessor.process_all_data({})
        assert result == {}
    
    def test_determine_ip_version_ipv4(self):
        """Test IPv4 detection"""
        assert DataProcessor._determine_ip_version('8.8.8.8') == 'IPv4'
        assert DataProcessor._determine_ip_version('192.168.1.1') == 'IPv4'
    
    def test_determine_ip_version_ipv6(self):
        """Test IPv6 detection"""
        assert DataProcessor._determine_ip_version('2001:4860:4860::8888') == 'IPv6'
        assert DataProcessor._determine_ip_version('::1') == 'IPv6'
    
    def test_determine_ip_version_unknown(self):
        """Test unknown IP format"""
        assert DataProcessor._determine_ip_version('invalid') == 'Unknown'
        assert DataProcessor._determine_ip_version('') == 'Unknown'
    
    def test_assess_threat_level_clean(self):
        """Test threat assessment for clean IP"""
        security = {'is_vpn': False, 'is_proxy': False, 'is_tor': False, 'is_relay': False}
        assert DataProcessor._assess_threat_level(security) == 'Clean'
    
    def test_assess_threat_level_single_threat(self):
        """Test threat assessment for single threat"""
        security = {'is_vpn': True, 'is_proxy': False, 'is_tor': False, 'is_relay': False}
        result = DataProcessor._assess_threat_level(security)
        assert 'Low' in result
        assert 'VPN' in result
    
    def test_assess_threat_level_multiple_threats(self):
        """Test threat assessment for multiple threats"""
        security = {'is_vpn': True, 'is_proxy': True, 'is_tor': False, 'is_relay': False}
        result = DataProcessor._assess_threat_level(security)
        assert 'Medium' in result
