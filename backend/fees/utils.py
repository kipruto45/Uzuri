def generate_fees_pdf(invoices, payments):


import io
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
import qrcode
from .models import Invoice, Transaction

def generate_fees_pdf(invoices, transactions, student=None):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, "Fees Statement")
    y = 780
    c.setFont("Helvetica", 12)
    if student:
        c.drawString(100, y, f"Student: {student}")
        y -= 20
    for invoice in invoices:
        c.drawString(100, y, f"Invoice: {invoice.description} | Category: {invoice.category} | Amount: {invoice.amount} | Due: {invoice.due_date} | Status: {invoice.status}")
        y -= 20
    for tx in transactions:
        c.drawString(100, y, f"Payment: {tx.amount} | Date: {tx.created_at.date()} | Method: {tx.method} | Status: {tx.status}")
        y -= 20
    c.save()
    buffer.seek(0)
    return buffer


def generate_fees_excel(invoices, transactions):
    invoice_data = [{
        'Description': inv.description,
        'Category': inv.category,
        'Amount': inv.amount,
        'Due Date': inv.due_date,
        'Status': inv.status
    } for inv in invoices]
    tx_data = [{
        'Amount': tx.amount,
        'Date': tx.created_at.date(),
        'Method': tx.method,
        'Status': tx.status
    } for tx in transactions]
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        pd.DataFrame(invoice_data).to_excel(writer, sheet_name='Invoices', index=False)
        pd.DataFrame(tx_data).to_excel(writer, sheet_name='Transactions', index=False)
    output.seek(0)
    return output
