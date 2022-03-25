import math
import os
import time
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import json
from reportlab.pdfbase.ttfonts import TTFont, TTFError
from reportlab.pdfbase import pdfmetrics

# import details.json
with open('details.json') as json_file:
    data = json.load(json_file)
    # splitting the course name into two lines, also they are in two separate variables because the
    # pdf editor can't process a \n in a string
    course_raw = data["student_course"].split()
    student_course_2 = ' '.join(course_raw[:math.ceil(len(course_raw) / 2)])
    student_course_1 = ' '.join(course_raw[math.ceil(len(course_raw) / 2):])
    # same thing with the address
    address_raw = data["student_address"].split()
    address_2 = ' '.join(address_raw[:math.ceil(len(address_raw) / 2)])
    address_1 = ' '.join(address_raw[math.ceil(len(address_raw) / 2):])

    # check if the elements in the array of data["school_days"] are between 1 - 5
    # if they are not, then the program will exit
    for i in data["school_days"]:
        if i < 1 or i > 5:
            print("The school days must be between 1 and 5")
            exit("reterd")

FILE_NAME = 'Sheet.pdf'
FILE_NAME_NEW = 'SheetFilled.pdf'
# this is the font that will be used in the pdf
font_name = 'Helvetica'
try:
    pdfmetrics.registerFont(TTFont('Custom_Font', 'Custom_Font.ttf'))
    font_name = 'Custom_Font'
except TTFError:
    print("Font file could not be opened. Going back to default font")

packet = io.BytesIO()
# create a new PDF with Reportlab
can = canvas.Canvas(packet, pagesize=letter)
# change font to SF Pro cause we cool here
can.setFont(font_name, data["font_size"])

# region Employer Details
can.drawString(160, 665, data['company_name'])  # company name
can.drawString(160, 638, data['contact_person'])  # company name
can.drawString(160, 613, data['contact_email'])  # company name
can.drawString(160, 585, data['contact_telephone'])  # company name
# endregion

# region Apprentice Details
can.drawString(120, 550, data['student_name'])  # company name
can.drawString(120, 531, data['student_email'])  # company name
can.drawString(355, 531, data['student_mobile'])  # company name
can.drawString(355, 550, data['student_ID'])  # company name

# address and the course can be quite long as a name, so if they are over 70 characters, decrease font for them
if len(address_1) + len(address_2) >= 70:
    can.setFont(font_name, data["font_size"] - 1)
    can.drawString(135, 502, address_1)  # company name
    can.drawString(135, 514, address_2)  # company name
    can.setFont(font_name, data["font_size"])
else:
    can.drawString(135, 502, address_1)  # company name
    can.drawString(135, 514, address_2)  # company name

if len(student_course_1) + len(student_course_2) >= 70:
    can.setFont(font_name, data["font_size"] - 1)
    can.drawString(355, 502, student_course_1)  # company name
    can.drawString(355, 514, student_course_2)  # company name
    can.setFont(font_name, data["font_size"])
else:
    can.drawString(355, 502, student_course_1)  # company name
    can.drawString(355, 514, student_course_2)  # company name

# endregion

# region School Days
MONDAY_WK1_X, MONDAY_WK1_Y = 159, 427
INCREMENTAL_X = 54
INCREMENTAL_Y = -30

for week in range(0, 5):
    for day in range(0, 7):
        # this will ignore the days that are being ignored in the json file.
        for coordinate in data["coords_to_ignore"]:
            if coordinate[0] == week and coordinate[1] == day:
                day = 0  # stupid hack to ignore the if statement below
                break
        # if the day being looped over is in 'school_days' array, then draw mark "E"
        if day in data['school_days']:
            can.drawString(MONDAY_WK1_X + (INCREMENTAL_X * day), MONDAY_WK1_Y + (INCREMENTAL_Y * week - week), 'E')

# endregion


can.save()

# move to the beginning of the StringIO buffer
packet.seek(0)

# create a new PDF with Reportlab
new_pdf = PdfFileReader(packet)
# read your existing PDF
existing_pdf = PdfFileReader(open(FILE_NAME, "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
# close microsoft edge browser
# os.system("taskkill /f /im MicrosoftEdge.exe")
# time.sleep(2)
# finally, write "output" to a real file
outputStream = open(FILE_NAME_NEW, "wb")
# open microsoft edge browser with the new pdf
# os.startfile(FILE_NAME_NEW)
output.write(outputStream)
outputStream.close()
