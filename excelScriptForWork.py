import pandas as pd
import ipaddress

#Eventually need to add it so it takes file name as an argu
def httpScan():
    # Define the IP address ranges
    allowed_ranges = [
        '131.123.92.', '131.123.93.','131.123.94.','131.123.95.'
        '131.123.212.', '131.123.213.', '131.123.214.', '131.123.215.',
        '131.123.246.', '131.123.247.'
    ]

    # Read the Excel file

    df = pd.read_csv('2024-02-19-scan_http-kent_state_university-asn.csv')
    print(df)
    df.columns = df.columns.str.strip()
    colName = 'ip'
    print (df.iloc[0,2])
    print(colName)

    df.columns = df.columns.str.strip()
    print(df.columns.str.strip())
    # Function to check if an IP address is within allowed ranges
    def is_ip_allowed(ip):
        for ip_range in allowed_ranges:
            if ip.startswith(ip_range):
                return True
        return False

    # Filter rows based on IP address
    filtered_df = df[df[colName].apply(lambda x: not is_ip_allowed(x.strip()))]

    # Print the filtered rows
    print(filtered_df)

    filtered_df.to_csv('filteredOutput.csv', index=False)



###MAIN##############################################

httpScan()#Eventually need to add it so it takes file name as an argu