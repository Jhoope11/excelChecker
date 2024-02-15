from openpyxl import Workbook

filename = "hello_world.xlsx"

workbook = Workbook()
sheet = workbook.active

sheet["A1"] = "hello"
sheet["B1"] = "world!"



sheet["A1"] = "value"
def print_rows():
    for row in sheet.iter_rows(values_only=True):
        print(row)
        
        
workbook.save(filename=filename)