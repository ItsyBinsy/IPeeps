"""
API Client Module for Abstract API IP Geolocation
This module handles all interactions with the Abstract API service.
"""

import requests
import os
from dotenv import load_dotenv
from typing import Dict, Optional

# Load environment variables from .env file
load_dotenv()

class AbstractAPIClient:
    """
    Client class for interacting with Abstract API IP Geolocation service.
    Handles API requests, response processing, and error management.
    """
    
    def __init__(self):
        """
        Initialize the API client with API key and base URL.
        Raises ValueError if API key is not found in environment variables.
        """
        self.api_key = os.getenv('ABSTRACT_API_KEY')
        if not self.api_key:
            raise ValueError("ABSTRACT_API_KEY not found in environment variables. Please check your .env file.")
        
        self.base_url = 'https://ipgeolocation.abstractapi.com/v1/'
        self.timeout = 10  # Request timeout in seconds
    
    def get_current_ip_info(self) -> Optional[Dict]:
        """
        Retrieve IP information for the current public IP address.
        
        Returns:
            dict: Dictionary containing IP information if successful
            None: If request fails
        
        Example return structure:
        {
            'ip_address': '8.8.8.8',
            'city': 'Mountain View',
            'country': 'United States',
            'timezone': {...},
            'security': {...}
        }
        """
        try:
            url = f"{self.base_url}?api_key={self.api_key}"
            response = requests.get(url, timeout=self.timeout)
            
            # Check if request was successful
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                print("Error: Invalid API key. Please check your credentials.")
                return None
            elif response.status_code == 429:
                print("Error: API rate limit exceeded. Please try again later.")
                return None
            else:
                print(f"Error: API returned status code {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            print("Error: Request timed out. Please check your internet connection.")
            return None
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to API. Please check your internet connection.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error: An unexpected error occurred: {str(e)}")
            return None
    
    def get_specific_ip_info(self, ip_address: str) -> Optional[Dict]:
        """
        Retrieve IP information for a specific IP address.
        
        Args:
            ip_address (str): The IP address to lookup (IPv4 or IPv6)
        
        Returns:
            dict: Dictionary containing IP information if successful
            None: If request fails
        """
        try:
            # Validate IP address format (basic validation)
            if not ip_address or not isinstance(ip_address, str):
                print("Error: Invalid IP address format.")
                return None
            
            url = f"{self.base_url}?api_key={self.api_key}&ip_address={ip_address}"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 422:
                print(f"Error: Invalid IP address format: {ip_address}")
                return None
            elif response.status_code == 401:
                print("Error: Invalid API key. Please check your credentials.")
                return None
            elif response.status_code == 429:
                print("Error: API rate limit exceeded. Please try again later.")
                return None
            else:
                print(f"Error: API returned status code {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            print("Error: Request timed out. Please check your internet connection.")
            return None
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to API. Please check your internet connection.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error: An unexpected error occurred: {str(e)}")
            return None
    
    def test_connection(self) -> bool:
        """
        Test the API connection and verify API key validity.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            url = f"{self.base_url}?api_key={self.api_key}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                print("✓ API connection successful!")
                return True
            else:
                print(f"✗ API connection failed with status code: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"✗ Connection test failed: {str(e)}")
            return False