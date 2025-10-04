"""
Main Application Module
IPv4/IPv6 Address Information Application

This application retrieves comprehensive IP address information including
geolocation, ISP details, security analysis, and more using Abstract API.
"""

import sys
import os
from colorama import Fore, Style, init

# Import custom modules
from api_client import AbstractAPIClient
from data_processor import DataProcessor
from output_formatter import OutputFormatter

# Initialize colorama
init(autoreset=True)

class IPInfoApp:
    """
    Main application class for IP Information lookup tool.
    Handles user interaction and coordinates between modules.
    """
    
    def __init__(self):
        """Initialize the application with API client."""
        try:
            self.api_client = AbstractAPIClient()
            self.data_processor = DataProcessor()
            self.output_formatter = OutputFormatter()
            self.running = True
        except ValueError as e:
            print(f"{Fore.RED}Initialization Error: {e}{Style.RESET_ALL}")
            sys.exit(1)
    
    def display_welcome(self):
        """Display welcome message and application information."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 80}")
        print(f"{'IPv4/IPv6 ADDRESS INFORMATION APPLICATION'.center(80)}")
        print(f"{'Network Technician Tool'.center(80)}")
        print(f"{'=' * 80}{Style.RESET_ALL}\n")
        print(f"{Fore.LIGHTBLACK_EX}Powered by Abstract API | Team Project 2025{Style.RESET_ALL}\n")
    
    def display_menu(self):
        """Display the main menu options."""
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}MAIN MENU{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 60}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. {Fore.LIGHTGREEN_EX}Get Current IP Information")
        print(f"{Fore.WHITE}2. {Fore.LIGHTCYAN_EX}Lookup Specific IP Address")
        print(f"{Fore.WHITE}3. {Fore.LIGHTMAGENTA_EX}Display in Table Format")
        print(f"{Fore.WHITE}4. {Fore.LIGHTYELLOW_EX}Save Last Result to File")
        print(f"{Fore.WHITE}5. {Fore.LIGHTBLUE_EX}Test API Connection")
        print(f"{Fore.WHITE}6. {Fore.LIGHTRED_EX}Exit Application")
        print(f"{Fore.CYAN}{'─' * 60}{Style.RESET_ALL}")
    
    def get_user_choice(self) -> str:
        """
        Get and validate user menu choice.
        
        Returns:
            str: User's menu choice
        """
        while True:
            choice = input(f"\n{Fore.WHITE}Enter your choice (1-6): {Style.RESET_ALL}").strip()
            if choice in ['1', '2', '3', '4', '5', '6']:
                return choice
            else:
                print(f"{Fore.RED}Invalid choice. Please enter a number between 1 and 6.{Style.RESET_ALL}")
    
    def get_current_ip_info(self):
        """Retrieve and display current public IP information."""
        print(f"\n{Fore.CYAN}Fetching your current IP information...{Style.RESET_ALL}")
        
        # Fetch data from API
        raw_data = self.api_client.get_current_ip_info()
        
        if raw_data:
            # Process the data
            self.last_processed_data = self.data_processor.process_all_data(raw_data)
            
            if self.last_processed_data:
                # Display formatted output
                self.output_formatter.display_all_info(self.last_processed_data)
                self.output_formatter.print_success("Information retrieved successfully!")
            else:
                self.output_formatter.print_error("Failed to process API response.")
        else:
            self.output_formatter.print_error("Failed to retrieve IP information.")
    
    def lookup_specific_ip(self):
        """Lookup information for a specific IP address."""
        print(f"\n{Fore.CYAN}IP Address Lookup{Style.RESET_ALL}")
        print(f"{Fore.LIGHTBLACK_EX}Enter an IPv4 or IPv6 address to lookup{Style.RESET_ALL}")
        print(f"{Fore.LIGHTBLACK_EX}Examples: 8.8.8.8 or 2001:4860:4860::8888{Style.RESET_ALL}\n")
        
        ip_address = input(f"{Fore.WHITE}Enter IP address: {Style.RESET_ALL}").strip()
        
        if not ip_address:
            self.output_formatter.print_error("No IP address provided.")
            return
        
        print(f"\n{Fore.CYAN}Fetching information for {ip_address}...{Style.RESET_ALL}")
        
        # Fetch data from API
        raw_data = self.api_client.get_specific_ip_info(ip_address)
        
        if raw_data:
            # Process the data
            self.last_processed_data = self.data_processor.process_all_data(raw_data)
            
            if self.last_processed_data:
                # Display formatted output
                self.output_formatter.display_all_info(self.last_processed_data)
                self.output_formatter.print_success("Information retrieved successfully!")
            else:
                self.output_formatter.print_error("Failed to process API response.")
        else:
            self.output_formatter.print_error(f"Failed to retrieve information for {ip_address}.")
    
    def display_table_format(self):
        """Display the last result in table format."""
        if not hasattr(self, 'last_processed_data') or not self.last_processed_data:
            self.output_formatter.print_warning("No data available. Please fetch IP information first (Option 1 or 2).")
            return
        
        self.output_formatter.display_table_format(self.last_processed_data)
    
    def save_last_result(self):
        """Save the last result to a file."""
        if not hasattr(self, 'last_processed_data') or not self.last_processed_data:
            self.output_formatter.print_warning("No data available. Please fetch IP information first (Option 1 or 2).")
            return
        
        print(f"\n{Fore.CYAN}Save Options{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Save as JSON")
        print(f"{Fore.WHITE}2. Save as Text")
        print(f"{Fore.WHITE}3. Save as Both")
        
        save_choice = input(f"\n{Fore.WHITE}Enter choice (1-3): {Style.RESET_ALL}").strip()
        
        filename_base = input(f"{Fore.WHITE}Enter filename (press Enter for auto-generated): {Style.RESET_ALL}").strip()
        
        if save_choice == '1':
            json_file = filename_base + '.json' if filename_base else None
            self.output_formatter.save_to_file(self.last_processed_data, json_file)
        
        elif save_choice == '2':
            text_file = filename_base + '.txt' if filename_base else None
            self.output_formatter.save_to_text(self.last_processed_data, text_file)
        
        elif save_choice == '3':
            json_file = filename_base + '.json' if filename_base else None
            text_file = filename_base + '.txt' if filename_base else None
            self.output_formatter.save_to_file(self.last_processed_data, json_file)
            self.output_formatter.save_to_text(self.last_processed_data, text_file)
        
        else:
            self.output_formatter.print_error("Invalid choice.")
    
    def test_api_connection(self):
        """Test the API connection."""
        print(f"\n{Fore.CYAN}Testing API connection...{Style.RESET_ALL}\n")
        
        if self.api_client.test_connection():
            self.output_formatter.print_success("API connection is working properly!")
        else:
            self.output_formatter.print_error("API connection failed. Please check your API key and internet connection.")
    
    def run(self):
        """Main application loop."""
        self.display_welcome()
        
        # Initialize last_processed_data
        self.last_processed_data = None
        
        while self.running:
            self.display_menu()
            choice = self.get_user_choice()
            
            if choice == '1':
                self.get_current_ip_info()
            
            elif choice == '2':
                self.lookup_specific_ip()
            
            elif choice == '3':
                self.display_table_format()
            
            elif choice == '4':
                self.save_last_result()
            
            elif choice == '5':
                self.test_api_connection()
            
            elif choice == '6':
                self.exit_application()
            
            # Pause before showing menu again
            if self.running:
                input(f"\n{Fore.LIGHTBLACK_EX}Press Enter to continue...{Style.RESET_ALL}")
    
    def exit_application(self):
        """Exit the application gracefully."""
        print(f"\n{Fore.CYAN}{'=' * 80}")
        print(f"{Fore.CYAN}Thank you for using IP Address Information Application!")
        print(f"{Fore.LIGHTBLACK_EX}Developed by [Your Team Name] | DEVASC Project 2025")
        print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}\n")
        self.running = False


def main():
    """
    Entry point for the application.
    Handles initialization and error catching.
    """
    try:
        app = IPInfoApp()
        app.run()
    
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Application interrupted by user.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Goodbye!{Style.RESET_ALL}\n")
        sys.exit(0)
    
    except Exception as e:
        print(f"\n{Fore.RED}An unexpected error occurred: {str(e)}{Style.RESET_ALL}")
        print(f"{Fore.LIGHTBLACK_EX}Please contact support or check the logs.{Style.RESET_ALL}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()