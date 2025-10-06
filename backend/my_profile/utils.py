import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
import qrcode

def generate_id_card_pdf(profile):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    # Draw student info
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30 * mm, height - 40 * mm, f"Student ID Card")
    c.setFont("Helvetica", 12)
    c.drawString(30 * mm, height - 55 * mm, f"Name: {profile.user.first_name} {profile.user.last_name}")
    c.drawString(30 * mm, height - 65 * mm, f"Program: {profile.program}")
    c.drawString(30 * mm, height - 75 * mm, f"Year: {profile.year_of_study}")
    c.drawString(30 * mm, height - 85 * mm, f"Student Number: {profile.user.student_number}")
    # Profile photo
    if profile.profile_photo:
        try:
            c.drawImage(ImageReader(profile.profile_photo.path), 150 * mm, height - 90 * mm, 30 * mm, 30 * mm)
        except Exception:
            pass
    # QR code
    qr_data = f"Name: {profile.user.first_name} {profile.user.last_name}\nProgram: {profile.program}\nYear: {profile.year_of_study}\nStudent Number: {profile.user.student_number}"
    qr_img = qrcode.make(qr_data)
    qr_buffer = io.BytesIO()
    qr_img.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)
    c.drawImage(ImageReader(qr_buffer), 30 * mm, height - 120 * mm, 30 * mm, 30 * mm)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
