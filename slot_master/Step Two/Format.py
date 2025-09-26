import xlwings as xw
import win32com.client

# Load the workbook with the live SQL connection
wb = xw.Book('C:\\Users\\Paul Collins\\Dynamic Gaming Dropbox\\Dynamic Gaming Solutions (new)\\Paul Collins\\Slot Master.xlsm')

# Create a new workbook
new_wb = xw.Book()

# Copy each sheet from the old workbook to the new one in reverse order
for sheet in reversed(wb.sheets):
    sheet.api.Copy(After=new_wb.sheets[-1].api)
    new_wb.sheets[-1].name = sheet.name

# Delete the initial empty sheet in the new workbook
new_wb.sheets[0].api.Delete()

# Save the new workbook and close it
new_wb_path = 'C:\\Users\\Paul Collins\\Dynamic Gaming Dropbox\\Dynamic Gaming Solutions (new)\\Paul Collins\\Slot Master (Copy).xlsm'
new_wb.save(new_wb_path)
new_wb.close()

# Open the new workbook with win32com and remove connections
excel = win32com.client.Dispatch("Excel.Application")
wb_win32 = excel.Workbooks.Open(new_wb_path)

# Delete each connection individually
for i in range(wb_win32.Connections.Count, 0, -1):
    wb_win32.Connections.Item(i).Delete()

wb_win32.Save()
wb_win32.Close()

# Close the original workbook without saving
wb.close()