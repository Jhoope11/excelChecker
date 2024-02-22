import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from datetime import datetime, timedelta
import os


allowedHttp = [
    '131.123.92.', '131.123.93.','131.123.94.','131.123.95.'
    '131.123.212.', '131.123.213.', '131.123.214.', '131.123.215.',
    '131.123.246.', '131.123.247.'
]
allowedDomains = [
    'cs.kent.edu', 'cs.math.kent.edu', 'mcs.kent.edu'
]
allowedSMTP = [
    'vs.cs.kent.edu', 'vs.cs.math.kent.edu', 'vs.mcs.kent.edu', 'vs.math.kent.edu'
]
allowedssl = [
    'TLSv1.2', 'TLSv1.3'
]
allowedDevices = [
    'BIG-IP', 'GlobalProtect'
]
allowedReasons = [
    'OK', 'Found'
]


def sshScan(csvFile):
    sshdf = pd.read_csv(csvFile)
    colName = 'hostname'
    #print(sshdf)
    sshdf.columns = sshdf.columns.str.strip()
    sshReport = sshdf[sshdf[colName].apply(lambda x: not is_ssh_allowed(str(x).strip()))]
    return sshReport

def smtpScan(csvFile):
    smtpdf = pd.read_csv(csvFile)
    colName = 'hostname'
    #print(smtpdf)
    smtpdf.columns = smtpdf.columns.str.strip()
    smtpReport = smtpdf[smtpdf[colName].apply(lambda x: not is_smtp_allowed(str(x).strip()))]
    return smtpReport

def sslScan(csvFile):
    #print(csvFile)
    ssldf = pd.read_csv(csvFile)
    colName = 'handshake'
    #print(ssldf)
    ssldf.columns = ssldf.columns.str.strip()
    sslReport = ssldf[ssldf[colName].apply(lambda x: not is_ssl_allowed(str(x).strip()))]
    return sslReport

def httpScan(csvFile):
    httpdf = pd.read_csv(csvFile)
    colName = 'ip'
    colSecName = 'http_reason'
    #print(httpdf)
    httpdf.columns = httpdf.columns.str.strip()
    httpReport = httpdf[httpdf[colName].apply(lambda x: not is_http_allowed(x.strip()))]
    httpReport = httpReport[httpReport[colSecName].apply(lambda x: not is_reason_allowed(x.strip()))]
    print(httpReport)
    return httpReport

def dIDScan(csvFile):
    dIDdf = pd.read_csv(csvFile)
    colName = 'device_model'
    #print(dIDdf)
    dIDdf.columns = dIDdf.columns.str.strip()
    dIDReport = dIDdf[dIDdf[colName].apply(lambda x: not is_dID_allowed(str(x).strip()))]
    return dIDReport
    

def is_http_allowed(ip):
        for ip_range in allowedHttp:
            if ip.startswith(ip_range):
                return True
        return False

def is_reason_allowed(reason):
        for reasons in allowedReasons:
            if reason.startswith(reasons):
                return False
        return True

def is_ssh_allowed(domain):
    domain = str(domain)
    for allowed_domain in allowedDomains:
        if domain.endswith(allowed_domain):
            return True
    return False

def is_smtp_allowed(smtpName):
    smtpName = str(smtpName)
    for allowed_smtpName in allowedSMTP:
        if smtpName.endswith(allowed_smtpName):
            return True
    return False

def is_ssl_allowed(ssl):
    ssl = str(ssl)
    for allowed_ssl in allowedssl:
        if ssl.endswith(allowed_ssl):
            return True
    return False

def is_dID_allowed(dID):
    dID = str(dID)
    for allowed_dID in allowedDevices:
        if dID.endswith(allowed_dID):
            return True
    return False

def saveToExcel(df, sheetName, workbook):
    sheet = workbook.create_sheet(title=sheetName)
    for r in dataframe_to_rows(df, index=False, header=True):
        sheet.append(r)


#call time date library
def genReports(csvFiles,outputFile):
    workbook = Workbook()
    x = 0
    for csvFile in csvFiles:
        print("current file is: %s" %csvFile)
        print("x is: %s" %x)
        if x == 0 and os.path.exists(csvFile):
            print("entering sshScan")
            sshFiltered = sshScan(csvFile)
            saveToExcel(sshFiltered, 'sshReport', workbook)
            workbook.save(outputFile)
            print("leaving sshScan")
        if x == 1 and os.path.exists(csvFile):
            print("entering smtpScan")
            smtpFiltered = smtpScan(csvFile)
            saveToExcel(smtpFiltered, 'smtpReport', workbook)
            workbook.save(outputFile)
            print("entering smtpScan")
        if x == 2 and os.path.exists(csvFile):
            print("entering sslScan")
            sslFiltered = sslScan(csvFile)
            saveToExcel(sslFiltered, 'sslReport', workbook)
            workbook.save(outputFile)
            print("leaving sslScan")
        if x == 3 and os.path.exists(csvFile):
            print("entering httpScan")
            httpFiltered = httpScan(csvFile)
            saveToExcel(httpFiltered, 'httpReport', workbook)
            workbook.save(outputFile)
            print("leaving httpScan")
        if x == 4 and os.path.exists(csvFile):
            print("entering dIDScan")
            dIDFiltered = dIDScan(csvFile)
            saveToExcel(dIDFiltered, 'dIDReport', workbook)
            workbook.save(outputFile)
            print("leaving dIDScan")
        x += 1
    workbook.save(outputFile) 
        
        

###MAIN##############################################

#currentDate = datetime.now().strftime("%Y-%m-%d")
yesterdayDate = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
csvFiles = [f"{yesterdayDate}-scan_ssh-kent_state_university-asn.csv",    #0    #ssh report -   done
            f"{yesterdayDate}-scan_smtp-kent_state_university-asn.csv",   #1    #smtp report-   done
            f"{yesterdayDate}-scan_ssl-kent_state_university-asn.csv",    #2    #ssl report -   done
            f"{yesterdayDate}-scan_http-kent_state_university-asn.csv",   #3    #http report-   done
            f"{yesterdayDate}-device_id-kent_state_university-asn.csv"]   #4    #devID report-  done
outputFile = f"{yesterdayDate}-output.xlsx"
genReports(csvFiles, outputFile)

