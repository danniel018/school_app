from openpyxl import Workbook, load_workbook
from openpyxl.styles import Border, Side, Alignment, Font, numbers
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl.utils import get_column_letter  
from io import BytesIO
import urllib.request
from datetime import datetime

from ..models.grades import Children,Grades

class ExcelReport:
    #wb = load_workbook(filename = BytesIO(file),data_only=True)
    wb = load_workbook('C:/Users/danie/PycharmProjects/school_app/report_format.xlsx')
    ws = wb.active
    #ws.merge_cells()
    student_name_box = ws['A3']
    student_lastname_box = ws['B3']
    teacher_box = ws['A4']
    date_of_report_box = ws['B4']
    first_grade_row = 8

    def __init__(self,student,subject):

        self.student_name = student.name
        self.student_lastname = student.lastname
        self.student_id = student.child_id
        self.teacher = subject.teacher.name
        self.subject = subject.grade_group.name + subject.subject.name
        self.subject_id = subject.grade_subject_id
        self.date = datetime.today()

    def average(self):

        grades = Grades.by_class_student(self.student_id,self.subject_id)
        
        current_grades = [grade for grade in grades if not grade.grade == None]

        for row in range(self.first_grade_row, self.first_grade_row + len(current_grades)):
            
            self.ws.merge_cells(start_row = row,end_row = row, start_column =  1, end_column = 2)
            self.ws.merge_cells(start_row = row,end_row = row, start_column =  3, end_column = 4)
            self.ws.merge_cells(start_row = row,end_row = row, start_column =  5, end_column = 6)
            
            self.ws[f'A{str(row)}'] = current_grades[row - self.first_grade_row].event.name
            self.ws[f'C{str(row)}'] = current_grades[row - self.first_grade_row].event.date
            self.ws[f'E{str(row)}'] = current_grades[row - self.first_grade_row].grade

        self.wb.save('fucking_report.xlsx')
            
    # notes = [88,85.3,75,77.6,79.34,81.43,88.5,92,92.6,96.24,83,85.6,80.04,
    #     74,81.4,83.56,90.04,86.87,79.8,88.56]
    # print(len(notes))

    # notes = sorted(notes)
    # print(notes)

    # percentile = ((notes.index(81.4) + 1)/len(notes)) * 100

    # print(percentile)