from openpyxl import load_workbook
workbook = load_workbook(filename="sample.xlsx")
workbook.sheetnames


sheet = workbook.active
sheet


sheet.title


sheet["A1"]


sheet["A1"].value


sheet["F10"].value