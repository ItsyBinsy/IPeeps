let currentData = null;

function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';
    hideAlerts();
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

function showError(message) {
    const alert = document.getElementById('errorAlert');
    alert.textContent = '> ERROR: ' + message;
    alert.style.display = 'block';
    setTimeout(() => alert.style.display = 'none', 5000);
}

function showSuccess(message) {
    const alert = document.getElementById('successAlert');
    alert.textContent = '> SUCCESS: ' + message;
    alert.style.display = 'block';
    setTimeout(() => alert.style.display = 'none', 3000);
}

function hideAlerts() {
    document.getElementById('errorAlert').style.display = 'none';
    document.getElementById('successAlert').style.display = 'none';
}

function createInfoItem(label, value, highlight = false) {
    return `
        <div class="info-item">
            <span class="info-label">${label}:</span>
            <span class="info-value" style="${highlight ? 'color: #00ff41; font-weight: 700; text-shadow: 0 0 8px rgba(0, 255, 65, 0.6);' : ''}">${value}</span>
        </div>
    `;
}

function displayResults(data) {
    currentData = data;

    // Basic
    if (data.basic) {
        const b = data.basic;
        document.getElementById('basicInfo').innerHTML = `
            ${createInfoItem('IP Address', b['IP Address'], true)}
            ${createInfoItem('IP Version', b['IP Version'])}
            ${createInfoItem('City', b['City'])}
            ${createInfoItem('Region', b['Region'])}
            ${createInfoItem('Country', b['Country'], true)}
            ${createInfoItem('Country Code', b['Country Code'])}
            ${createInfoItem('Continent', b['Continent'])}
            ${createInfoItem('Postal Code', b['Postal Code'])}
            ${createInfoItem('Latitude', b['Latitude'])}
            ${createInfoItem('Longitude', b['Longitude'])}
        `;
    }

    // Connection
    if (data.connection) {
        const c = data.connection;
        document.getElementById('connectionInfo').innerHTML = `
            ${createInfoItem('ISP', c['ISP'], true)}
            ${createInfoItem('Organization', c['Organization'])}
            ${createInfoItem('ASN', c['ASN'])}
            ${createInfoItem('ASN Organization', c['ASN Organization'])}
            ${createInfoItem('Connection Type', c['Connection Type'])}
        `;
    }

    // Timezone
    if (data.timezone) {
        const tz = data.timezone;
        document.getElementById('timezoneInfo').innerHTML = `
            ${createInfoItem('Timezone', tz['Timezone Name'], true)}
            ${createInfoItem('Abbreviation', tz['Abbreviation'])}
            ${createInfoItem('GMT Offset', tz['GMT Offset'])}
            ${createInfoItem('Current Time', tz['Current Time'], true)}
            ${createInfoItem('Daylight Saving', tz['Is DST'])}
        `;
    }

    // Security
    if (data.security) {
        const s = data.security;
        const threatClass = s['Threat Level'].includes('Clean') ? 'badge-clean'
            : s['Threat Level'].includes('Low') ? 'badge-warning'
            : 'badge-danger';

        document.getElementById('securityInfo').innerHTML = `
            ${createInfoItem('VPN Detected', s['Is VPN'] ? '[!] YES' : '[✓] NO')}
            ${createInfoItem('Proxy Detected', s['Is Proxy'] ? '[!] YES' : '[✓] NO')}
            ${createInfoItem('Tor Detected', s['Is Tor'] ? '[!] YES' : '[✓] NO')}
            ${createInfoItem('Relay Detected', s['Is Relay'] ? '[!] YES' : '[✓] NO')}
            <div class="info-item" style="grid-column: 1/-1;">
                <span class="info-label">Threat Level:</span>
                <span class="security-badge ${threatClass}">${s['Threat Level']}</span>
            </div>
        `;
    }

    // Currency
    if (data.currency) {
        const cur = data.currency;
        document.getElementById('currencyInfo').innerHTML = `
            ${createInfoItem('Currency', cur['Currency Name'], true)}
            ${createInfoItem('Code', cur['Currency Code'])}
            ${createInfoItem('Symbol', cur['Currency Symbol'])}
        `;
    }

    // Flag
    if (data.flag) {
        const f = data.flag;
        document.getElementById('flagInfo').innerHTML = `
            <div style="text-align: center; padding: 20px;">
                <div class="flag-emoji">${f['Flag Emoji']}</div>
                <p style="margin-top: 10px; color: #00cc00;">Unicode: ${f['Flag Unicode']}</p>
            </div>
        `;
    }

    document.getElementById('results').style.display = 'block';
    showSuccess('Information retrieved successfully!');
}

async function getCurrentIP() {
    showLoading();
    try {
        const res = await fetch('/api/current-ip');
        const result = await res.json();
        hideLoading();
        if (result.success) {
            displayResults(result.data);
        } else {
            showError(result.error || 'Failed to retrieve IP information');
        }
    } catch (e) {
        hideLoading();
        showError('Network error: ' + e.message);
    }
}

function validateIPAddress(ip) {
    // IPv4 only (pattern: 0-255.0-255.0-255.0-255)
    const ipv4Pattern = /^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$/;
    if (ipv4Pattern.test(ip)) return { valid: true, type: 'IPv4' };
    return { valid: false, type: null };
}

async function lookupIP() {
    const ip = document.getElementById('ipInput').value.trim();
    if (!ip) return showError('Please enter an IP address');

    const validation = validateIPAddress(ip);
    if (!validation.valid) {
        return showError('Invalid IPv4 format. Try e.g., 8.8.8.8 or 192.168.1.1');
    }

    showLoading();
    try {
        const res = await fetch('/api/lookup-ip', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ip_address: ip })
        });
        const result = await res.json();
        hideLoading();
        if (result.success) {
            displayResults(result.data);
        } else {
            showError(result.error || 'Failed to lookup IP address');
        }
    } catch (e) {
        hideLoading();
        showError('Network error: ' + e.message);
    }
}

function exportJSON() {
    if (!currentData) return showError('No data available to export');
    const dataStr = JSON.stringify(currentData, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = `ip_info_${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
    showSuccess('JSON file downloaded!');
}

function exportText() {
    if (!currentData) return showError('No data available to export');

    let text = '='.repeat(80) + '\n';
    text += 'IP ADDRESS INFORMATION REPORT\n';
    text += '='.repeat(80) + '\n\n';

    for (const [category, data] of Object.entries(currentData)) {
        text += `\n> ${category.toUpperCase()}\n`;
        text += '-'.repeat(60) + '\n';
        for (const [key, value] of Object.entries(data)) {
            text += `${key.padEnd(25, '.')} ${value}\n`;
        }
    }
    text += '\n' + '='.repeat(80) + '\n';
    text += `Report generated at: ${new Date().toLocaleString()}\n`;

    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = `ip_info_${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
    showSuccess('Text file downloaded!');
}

// Enter key in the IP input triggers lookup
document.addEventListener('DOMContentLoaded', () => {
    const ipInput = document.getElementById('ipInput');
    ipInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') lookupIP();
    });
});

async function testConnection() {
    showLoading();
    try {
        const res = await fetch('/api/test-connection');
        const result = await res.json();
        hideLoading();
        if (result.success) {
            showSuccess(result.message || 'API connection successful!');
        } else {
            showError(result.message || 'API connection failed');
        }
    } catch (e) {
        hideLoading();
        showError('Network error: ' + e.message);
    }
}
