from openpyxl import load_workbook
workbook = load_workbook(filename="sample.xlsx")
workbook.sheetnames
['Sheet 1']

sheet = workbook.active
sheet 
sheet.title
'Sheet 1'