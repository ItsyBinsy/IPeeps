# IPeeps

A Python web application that retrieves comprehensive IPv4 and IPv6 information using the Abstract API.

**Project Activity 3 – Social Coding | October 2025**
**Developed by Group 3 – 4ITH**

## Overview

**IPeeps** is a Python web tool that simplifies network intelligence. It retrieves comprehensive information about any IPv4 or IPv6 address, including geolocation, ISP, security, timezone, and currency details.
Built with Flask and the Abstract API, the system demonstrates REST API integration, data parsing, error handling, and clean UI presentation.

## Quick Start

**Prerequisites**

* Python 3.9 or higher
* Abstract API key (obtainable for free at [abstractapi.com](https://www.abstractapi.com))

**Setup Steps**

1. Clone the repository from GitHub.
2. Install the required dependencies listed in `requirements.txt`.
3. Create a `.env` file and add the line:
   `ABSTRACT_API_KEY=your_api_key_here`
4. Run the Flask application:
   `python app.py`
5. Open your web browser and navigate to `http://127.0.0.1:5000`

## Features

* **IPv4 & IPv6 Lookup** – Retrieve data for any valid IP address.
* **Geolocation Data** – Displays country, region, city, latitude, and longitude.
* **ISP & ASN Information** – Shows provider, organization, and connection details.
* **Security Insights** – Detects VPN, proxy, Tor, or relay usage.
* **Timezone & Currency Data** – Includes GMT offset, local time, and national currency.
* **Export Options** – Save lookup results as JSON or text files.
* **Error Handling** – Displays “N/A” instead of null for missing values.
* **Clean, Responsive UI** – Web interface with a terminal-inspired design.

## API Reference

**Provider:** [Abstract API - IP Geolocation & Threat Intelligence](https://www.abstractapi.com/ip-geolocation-api)

**Data Retrieved:**
* IP version, address, continent, country, region, city
* ISP, ASN, organization, connection type
* VPN, proxy, relay, and Tor detection
* Timezone name, abbreviation, and offset
* Currency name, code, and symbol

## Error Handling

* Invalid IP formats trigger on-screen alerts.
* Null or missing data is displayed as “N/A”.
* Network and API errors are caught gracefully with user feedback.

## Future Enhancements

* **Mini Weather Widget** – Display real-time weather for the IP’s detected city using a free weather API.
* **Country Mood Background** – Dynamically adapt the background color or gradient based on country code.
* **Human-Readable Summary** – Generate a concise, natural-language description of lookup results.
* **Custom Result Themes by Country** – Apply distinct accent colors or highlight schemes per country.
* **Embed Google Maps** – Integrate a visual map pinpointing the geolocation of the IP.
* **Dark/Light Theme Toggle** – Allow users to switch between light and dark interface modes.
* **Auto-Detect Current IP** – Automatically retrieve and display the user’s public IP information on load.
* **Free Trivia API Integration** – Show short trivia facts about countries or IPs for engagement.
* **Privacy Checker** – Indicate if an IP shows signs of VPN, proxy, or possible tracking exposure.
* **Network Speed Simulator** – Simulate connection speeds to demonstrate network conditions.