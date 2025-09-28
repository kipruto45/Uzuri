import io
import openpyxl
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .models import CalendarEvent

def export_events_excel(events):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Title", "Category", "Start", "End", "Location", "Status"])
    for e in events:
        ws.append([e.title, e.category, e.start_time, e.end_time, e.location, e.status])
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output

def export_events_pdf(events):
    output = io.BytesIO()
    p = canvas.Canvas(output)
    y = 800
    for e in events:
        p.drawString(50, y, f"{e.title} | {e.category} | {e.start_time} - {e.end_time} | {e.location} | {e.status}")
        y -= 20
    p.save()
    output.seek(0)
    return output
