# IPeeps

A Python network tool that retrieves comprehensive IP address information using Abstract API.

**Project Activity 3 – Social Coding** | October 2025

---

## Quick Start

### Prerequisites
- Python 3.9+
- Abstract API key (free at [abstractapi.com](https://www.abstractapi.com/))

### Installation

```bash
# 1. Clone repository
git clone https://github.com/YOUR-USERNAME/ipv4-ipv6-address-app.git
cd ipv4-ipv6-address-app

# 2. Install dependencies
pip install requests python-dotenv colorama tabulate

# 3. Add your API key
# Create .env file and add:
ABSTRACT_API_KEY=your_api_key_here

# 4. Run
python src/main.py
```

---

## Features

- **IPv4/IPv6 Detection** - Automatically identifies your public IP address
- **Geolocation** - City, region, country, coordinates
- **ISP Information** - Provider name, ASN, organization
- **Security Analysis** - VPN, Proxy, Tor detection
- **Timezone & Currency** - Local time and currency info
- **Specific IP Lookup** - Search any IPv4/IPv6 address
- **Export Results** - Save to JSON or text files
- **Color-Coded Display** - Easy-to-read terminal output

---

## Usage

Run the application and choose from the menu:

1. **Get Current IP Information** - View your public IP details
2. **Lookup Specific IP Address** - Search any IP (e.g., `8.8.8.8`)
3. **Display in Table Format** - View results as a table
4. **Save Last Result to File** - Export to JSON/text
5. **Test API Connection** - Verify API setup
6. **Exit Application**

---

## Project Requirements

This project fulfills Project Activity 3 requirements:
- REST API integration (Abstract API)
- IPv4/IPv6 address retrieval
- Geolocation and ISP information
- Error handling
- User-friendly output formatting
- GitHub collaboration workflow
- Comprehensive documentation

---

## Future Enhancements

- Subnet calculator
- IP history tracking
- Batch IP lookup from CSV
- GUI interface
- Database integration
- Geolocation map visualization
