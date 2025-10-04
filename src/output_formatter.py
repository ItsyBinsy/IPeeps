"""
Output Formatter Module
Handles all display formatting, color coding, and data presentation.
"""

from colorama import Fore, Back, Style, init
from tabulate import tabulate
from typing import Dict, Any
import json
from datetime import datetime

# Initialize colorama for cross-platform color support
init(autoreset=True)

class OutputFormatter:
    """
    Handles formatting and display of IP information data.
    Provides colored output, tables, and file export capabilities.
    """
    
    @staticmethod
    def print_header(title: str):
        """
        Print a formatted header with decorative borders.
        
        Args:
            title (str): Header title text
        """
        width = 80
        print("\n" + Fore.CYAN + "=" * width)
        print(Fore.CYAN + Style.BRIGHT + title.center(width))
        print(Fore.CYAN + "=" * width + Style.RESET_ALL)
    
    @staticmethod
    def print_section_header(section_name: str):
        """
        Print a formatted section header.
        
        Args:
            section_name (str): Section name
        """
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}▶ {section_name}{Style.RESET_ALL}")
        print(Fore.YELLOW + "-" * 60 + Style.RESET_ALL)
    
    @staticmethod
    def print_key_value(key: str, value: Any, color: str = Fore.WHITE):
        """
        Print a key-value pair with formatting.
        
        Args:
            key (str): The key/label
            value: The value to display
            color (str): Colorama color code for the value
        """
        print(f"{Fore.LIGHTBLACK_EX}{key:.<25} {color}{value}{Style.RESET_ALL}")
    
    @staticmethod
    def print_basic_info(data: Dict[str, str]):
        """
        Display basic IP and location information.
        
        Args:
            data (dict): Basic information dictionary
        """
        OutputFormatter.print_section_header("BASIC INFORMATION")
        
        # Highlight IP address
        ip_color = Fore.GREEN if data.get('IP Version') == 'IPv4' else Fore.CYAN
        OutputFormatter.print_key_value("IP Address", data.get('IP Address', 'N/A'), ip_color + Style.BRIGHT)
        OutputFormatter.print_key_value("IP Version", data.get('IP Version', 'N/A'), Fore.LIGHTMAGENTA_EX)
        
        # Location information
        OutputFormatter.print_key_value("City", data.get('City', 'N/A'))
        OutputFormatter.print_key_value("Region", data.get('Region', 'N/A'))
        OutputFormatter.print_key_value("Country", data.get('Country', 'N/A'), Fore.LIGHTCYAN_EX)
        OutputFormatter.print_key_value("Country Code", data.get('Country Code', 'N/A'))
        OutputFormatter.print_key_value("Continent", data.get('Continent', 'N/A'))
        OutputFormatter.print_key_value("Postal Code", data.get('Postal Code', 'N/A'))
        OutputFormatter.print_key_value("Coordinates", f"{data.get('Latitude', 'N/A')}, {data.get('Longitude', 'N/A')}", Fore.LIGHTYELLOW_EX)
    
    @staticmethod
    def print_connection_info(data: Dict[str, str]):
        """
        Display ISP and connection information.
        
        Args:
            data (dict): Connection information dictionary
        """
        OutputFormatter.print_section_header("CONNECTION INFORMATION")
        
        OutputFormatter.print_key_value("ISP", data.get('ISP', 'N/A'), Fore.LIGHTGREEN_EX)
        OutputFormatter.print_key_value("Organization", data.get('Organization', 'N/A'))
        OutputFormatter.print_key_value("ASN", data.get('ASN', 'N/A'), Fore.LIGHTMAGENTA_EX)
        OutputFormatter.print_key_value("ASN Organization", data.get('ASN Organization', 'N/A'))
        OutputFormatter.print_key_value("Connection Type", data.get('Connection Type', 'N/A'), Fore.LIGHTYELLOW_EX)
    
    @staticmethod
    def print_timezone_info(data: Dict[str, str]):
        """
        Display timezone information.
        
        Args:
            data (dict): Timezone information dictionary
        """
        OutputFormatter.print_section_header("TIMEZONE INFORMATION")
        
        OutputFormatter.print_key_value("Timezone", data.get('Timezone Name', 'N/A'), Fore.LIGHTCYAN_EX)
        OutputFormatter.print_key_value("Abbreviation", data.get('Abbreviation', 'N/A'))
        OutputFormatter.print_key_value("GMT Offset", data.get('GMT Offset', 'N/A'), Fore.LIGHTYELLOW_EX)
        OutputFormatter.print_key_value("Current Time", data.get('Current Time', 'N/A'), Fore.LIGHTGREEN_EX)
        OutputFormatter.print_key_value("Daylight Saving", data.get('Is DST', 'N/A'))
    
    @staticmethod
    def print_security_info(data: Dict[str, Any]):
        """
        Display security and threat information with color-coded warnings.
        
        Args:
            data (dict): Security information dictionary
        """
        OutputFormatter.print_section_header("SECURITY ANALYSIS")
        
        # Color code based on threat detection
        vpn_color = Fore.RED if data.get('Is VPN') else Fore.GREEN
        proxy_color = Fore.RED if data.get('Is Proxy') else Fore.GREEN
        tor_color = Fore.RED if data.get('Is Tor') else Fore.GREEN
        relay_color = Fore.RED if data.get('Is Relay') else Fore.GREEN
        
        OutputFormatter.print_key_value("VPN Detected", "YES ⚠" if data.get('Is VPN') else "NO ✓", vpn_color + Style.BRIGHT)
        OutputFormatter.print_key_value("Proxy Detected", "YES ⚠" if data.get('Is Proxy') else "NO ✓", proxy_color + Style.BRIGHT)
        OutputFormatter.print_key_value("Tor Detected", "YES ⚠" if data.get('Is Tor') else "NO ✓", tor_color + Style.BRIGHT)
        OutputFormatter.print_key_value("Relay Detected", "YES ⚠" if data.get('Is Relay') else "NO ✓", relay_color + Style.BRIGHT)
        
        # Threat level summary
        threat_level = data.get('Threat Level', 'Unknown')
        if 'Clean' in threat_level:
            threat_color = Fore.GREEN
        elif 'Low' in threat_level:
            threat_color = Fore.YELLOW
        else:
            threat_color = Fore.RED
        
        OutputFormatter.print_key_value("Overall Threat Level", threat_level, threat_color + Style.BRIGHT)
    
    @staticmethod
    def print_currency_info(data: Dict[str, str]):
        """
        Display currency information.
        
        Args:
            data (dict): Currency information dictionary
        """
        OutputFormatter.print_section_header("CURRENCY INFORMATION")
        
        OutputFormatter.print_key_value("Currency", data.get('Currency Name', 'N/A'), Fore.LIGHTGREEN_EX)
        OutputFormatter.print_key_value("Currency Code", data.get('Currency Code', 'N/A'))
        OutputFormatter.print_key_value("Symbol", data.get('Currency Symbol', 'N/A'), Fore.LIGHTYELLOW_EX)
    
    @staticmethod
    def print_flag_info(data: Dict[str, str]):
        """
        Display country flag information.
        
        Args:
            data (dict): Flag information dictionary
        """
        OutputFormatter.print_section_header("FLAG INFORMATION")
        
        flag_emoji = data.get('Flag Emoji', 'N/A')
        print(f"{Fore.LIGHTBLACK_EX}Flag Emoji.............. {Fore.WHITE}{flag_emoji} {Style.RESET_ALL}")
        OutputFormatter.print_key_value("Unicode", data.get('Flag Unicode', 'N/A'))
    
    @staticmethod
    def display_all_info(processed_data: Dict[str, Dict]):
        """
        Display all processed information in organized sections.
        
        Args:
            processed_data (dict): Dictionary containing all categorized data
        """
        OutputFormatter.print_header("IP ADDRESS INFORMATION REPORT")
        
        # Display each section if data exists
        if 'basic' in processed_data:
            OutputFormatter.print_basic_info(processed_data['basic'])
        
        if 'connection' in processed_data:
            OutputFormatter.print_connection_info(processed_data['connection'])
        
        if 'timezone' in processed_data:
            OutputFormatter.print_timezone_info(processed_data['timezone'])
        
        if 'security' in processed_data:
            OutputFormatter.print_security_info(processed_data['security'])
        
        if 'currency' in processed_data:
            OutputFormatter.print_currency_info(processed_data['currency'])
        
        if 'flag' in processed_data:
            OutputFormatter.print_flag_info(processed_data['flag'])
        
        # Footer
        print("\n" + Fore.CYAN + "=" * 80 + Style.RESET_ALL)
        print(f"{Fore.LIGHTBLACK_EX}Report generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}\n")
    
    @staticmethod
    def display_table_format(processed_data: Dict[str, Dict]):
        """
        Display information in table format using tabulate.
        
        Args:
            processed_data (dict): Dictionary containing all categorized data
        """
        OutputFormatter.print_header("IP ADDRESS INFORMATION (TABLE VIEW)")
        
        # Combine all data into a single table
        table_data = []
        
        for category, data in processed_data.items():
            if isinstance(data, dict):
                table_data.append([f"{Fore.YELLOW}{category.upper()}{Style.RESET_ALL}", "", ""])
                for key, value in data.items():
                    table_data.append(["", key, str(value)])
        
        print(tabulate(table_data, headers=["Category", "Field", "Value"], tablefmt="grid"))
        print()
    
    @staticmethod
    def save_to_file(processed_data: Dict[str, Dict], filename: str = None):
        """
        Save processed data to a JSON file.
        
        Args:
            processed_data (dict): Dictionary containing all data
            filename (str): Output filename (optional)
        
        Returns:
            str: Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"ip_info_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, indent=4, ensure_ascii=False)
            
            print(f"{Fore.GREEN}✓ Data saved successfully to: {filename}{Style.RESET_ALL}")
            return filename
        
        except Exception as e:
            print(f"{Fore.RED}✗ Error saving file: {str(e)}{Style.RESET_ALL}")
            return None
    
    @staticmethod
    def save_to_text(processed_data: Dict[str, Dict], filename: str = None):
        """
        Save processed data to a formatted text file.
        
        Args:
            processed_data (dict): Dictionary containing all data
            filename (str): Output filename (optional)
        
        Returns:
            str: Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"ip_info_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("IP ADDRESS INFORMATION REPORT\n")
                f.write("=" * 80 + "\n\n")
                
                for category, data in processed_data.items():
                    if isinstance(data, dict):
                        f.write(f"\n▶ {category.upper()}\n")
                        f.write("-" * 60 + "\n")
                        for key, value in data.items():
                            f.write(f"{key:.<25} {value}\n")
                
                f.write("\n" + "=" * 80 + "\n")
                f.write(f"Report generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            print(f"{Fore.GREEN}✓ Data saved successfully to: {filename}{Style.RESET_ALL}")
            return filename
        
        except Exception as e:
            print(f"{Fore.RED}✗ Error saving file: {str(e)}{Style.RESET_ALL}")
            return None
    
    @staticmethod
    def print_error(message: str):
        """
        Print an error message with formatting.
        
        Args:
            message (str): Error message
        """
        print(f"\n{Fore.RED}{Style.BRIGHT}✗ ERROR: {message}{Style.RESET_ALL}\n")
    
    @staticmethod
    def print_success(message: str):
        """
        Print a success message with formatting.
        
        Args:
            message (str): Success message
        """
        print(f"\n{Fore.GREEN}{Style.BRIGHT}✓ {message}{Style.RESET_ALL}\n")
    
    @staticmethod
    def print_warning(message: str):
        """
        Print a warning message with formatting.
        
        Args:
            message (str): Warning message
        """
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}⚠ WARNING: {message}{Style.RESET_ALL}\n")