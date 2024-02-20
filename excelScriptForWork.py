import pandas as pd
import ipaddress

# Define the IP address ranges
allowed_ranges = [
    ipaddress.ip_network('192.168.0.0/24'),
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12')
]

# Read the Excel file
df = pd.read_excel('your_file.xlsx')

# Function to check if an IP address is within allowed ranges
def is_ip_allowed(ip):
    for ip_range in allowed_ranges:
        if ipaddress.ip_address(ip) in ip_range:
            return True
    return False

# Filter rows based on IP address
filtered_df = df[df['IP Address'].apply(lambda x: not is_ip_allowed(x))]

# Print the filtered rows
print(filtered_df)