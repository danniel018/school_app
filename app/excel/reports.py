from openpyxl import Workbook, load_workbook
from openpyxl.styles import Border, Side, Alignment, Font, numbers
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl.utils import get_column_letter  
from io import BytesIO
import urllib.request


class ExcelReports:
    #wb = load_workbook(filename = BytesIO(file),data_only=True)
    wb = load_workbook('directory')

    notes = [88,85.3,75,77.6,79.34,81.43,88.5,92,92.6,96.24,83,85.6,80.04,
        74,81.4,83.56,90.04,86.87,79.8,88.56]
    print(len(notes))

    notes = sorted(notes)
    print(notes)

    percentile = ((notes.index(81.4) + 1)/len(notes)) * 100

    print(percentile)