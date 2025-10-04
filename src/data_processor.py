"""
Data Processor Module
Handles parsing, validation, and structuring of IP information data.
"""

from typing import Dict, Optional, Any

class DataProcessor:
    """
    Processes and structures IP geolocation data from Abstract API.
    Validates data and extracts relevant information for display.
    """
    
    @staticmethod
    def validate_response(data: Optional[Dict]) -> bool:
        """
        Validate that the API response contains required fields.
        
        Args:
            data (dict): Response data from API
        
        Returns:
            bool: True if data is valid, False otherwise
        """
        if not data:
            return False
        
        # Check for essential fields
        required_fields = ['ip_address']
        for field in required_fields:
            if field not in data:
                return False
        
        return True
    
    @staticmethod
    def extract_basic_info(data: Dict) -> Dict[str, str]:
        """
        Extract basic IP and location information.
        
        Args:
            data (dict): Raw API response data
        
        Returns:
            dict: Structured basic information
        """
        return {
            'IP Address': data.get('ip_address', 'N/A'),
            'IP Version': DataProcessor._determine_ip_version(data.get('ip_address', '')),
            'City': data.get('city', 'N/A'),
            'Region': data.get('region', 'N/A'),
            'Country': data.get('country', 'N/A'),
            'Country Code': data.get('country_code', 'N/A'),
            'Continent': data.get('continent', 'N/A'),
            'Postal Code': data.get('postal_code', 'N/A'),
            'Latitude': str(data.get('latitude', 'N/A')),
            'Longitude': str(data.get('longitude', 'N/A'))
        }
    
    @staticmethod
    def extract_connection_info(data: Dict) -> Dict[str, str]:
        """
        Extract ISP and connection information.
        
        Args:
            data (dict): Raw API response data
        
        Returns:
            dict: Structured connection information
        """
        connection = data.get('connection', {})
        
        return {
            'ISP': connection.get('isp_name', 'N/A'),
            'Organization': connection.get('organization_name', 'N/A'),
            'ASN': str(connection.get('autonomous_system_number', 'N/A')),
            'ASN Organization': connection.get('autonomous_system_organization', 'N/A'),
            'Connection Type': connection.get('connection_type', 'N/A')
        }
    
    @staticmethod
    def extract_timezone_info(data: Dict) -> Dict[str, str]:
        """
        Extract timezone information.
        
        Args:
            data (dict): Raw API response data
        
        Returns:
            dict: Structured timezone information
        """
        timezone = data.get('timezone', {})
        
        return {
            'Timezone Name': timezone.get('name', 'N/A'),
            'Abbreviation': timezone.get('abbreviation', 'N/A'),
            'GMT Offset': str(timezone.get('gmt_offset', 'N/A')),
            'Current Time': timezone.get('current_time', 'N/A'),
            'Is DST': str(timezone.get('is_dst', 'N/A'))
        }
    
    @staticmethod
    def extract_security_info(data: Dict) -> Dict[str, Any]:
        """
        Extract security and threat information.
        This is a key feature of Abstract API - VPN/Proxy detection.
        
        Args:
            data (dict): Raw API response data
        
        Returns:
            dict: Structured security information
        """
        security = data.get('security', {})
        
        return {
            'Is VPN': security.get('is_vpn', False),
            'Is Proxy': DataProcessor._check_proxy(security),
            'Is Tor': DataProcessor._check_tor(security),
            'Is Relay': DataProcessor._check_relay(security),
            'Threat Level': DataProcessor._assess_threat_level(security)
        }
    
    @staticmethod
    def extract_currency_info(data: Dict) -> Dict[str, str]:
        """
        Extract currency information for the location.
        
        Args:
            data (dict): Raw API response data
        
        Returns:
            dict: Structured currency information
        """
        currency = data.get('currency', {})
        
        return {
            'Currency Name': currency.get('currency_name', 'N/A'),
            'Currency Code': currency.get('currency_code', 'N/A'),
            'Currency Symbol': currency.get('currency_symbol', 'N/A')
        }
    
    @staticmethod
    def extract_flag_info(data: Dict) -> Dict[str, str]:
        """
        Extract country flag information.
        
        Args:
            data (dict): Raw API response data
        
        Returns:
            dict: Structured flag information
        """
        flag = data.get('flag', {})
        
        return {
            'Flag Emoji': flag.get('emoji', 'N/A'),
            'Flag Unicode': flag.get('unicode', 'N/A'),
            'Flag PNG': flag.get('png', 'N/A'),
            'Flag SVG': flag.get('svg', 'N/A')
        }
    
    @staticmethod
    def process_all_data(data: Dict) -> Dict[str, Dict]:
        """
        Process all available data from API response.
        Organizes data into categorized sections.
        
        Args:
            data (dict): Raw API response data
        
        Returns:
            dict: Dictionary with categorized information sections
        """
        if not DataProcessor.validate_response(data):
            return {}
        
        return {
            'basic': DataProcessor.extract_basic_info(data),
            'connection': DataProcessor.extract_connection_info(data),
            'timezone': DataProcessor.extract_timezone_info(data),
            'security': DataProcessor.extract_security_info(data),
            'currency': DataProcessor.extract_currency_info(data),
            'flag': DataProcessor.extract_flag_info(data)
        }
    
    @staticmethod
    def _determine_ip_version(ip_address: str) -> str:
        """
        Determine if IP address is IPv4 or IPv6.
        
        Args:
            ip_address (str): IP address string
        
        Returns:
            str: 'IPv4', 'IPv6', or 'Unknown'
        """
        if ':' in ip_address:
            return 'IPv6'
        elif '.' in ip_address:
            return 'IPv4'
        else:
            return 'Unknown'
    
    @staticmethod
    def _check_proxy(security: Dict) -> bool:
        """Check if IP is identified as proxy."""
        return security.get('is_proxy', False)
    
    @staticmethod
    def _check_tor(security: Dict) -> bool:
        """Check if IP is identified as Tor exit node."""
        return security.get('is_tor', False)
    
    @staticmethod
    def _check_relay(security: Dict) -> bool:
        """Check if IP is identified as relay."""
        return security.get('is_relay', False)
    
    @staticmethod
    def _assess_threat_level(security: Dict) -> str:
        """
        Assess overall threat level based on security indicators.
        
        Args:
            security (dict): Security information
        
        Returns:
            str: Threat level description
        """
        threats = []
        
        if security.get('is_vpn', False):
            threats.append('VPN')
        if security.get('is_proxy', False):
            threats.append('Proxy')
        if security.get('is_tor', False):
            threats.append('Tor')
        if security.get('is_relay', False):
            threats.append('Relay')
        
        if len(threats) == 0:
            return 'Clean'
        elif len(threats) == 1:
            return f'Low ({threats[0]} detected)'
        else:
            return f'Medium (Multiple: {", ".join(threats)})'