from openpyxl import load_workbook
workbook = load_workbook(filename="sample.xlsx")
workbook.sheetnames


sheet = workbook.active
sheet


sheet.title