from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Result, GradingScale, Recommendation
from .serializers import ResultSerializer
from django.http import FileResponse
import io
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from my_profile.tasks import send_notification
from django.db.models import Avg

class FinalResultViewSet(viewsets.ModelViewSet):
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        queryset = Result.objects.filter(student=profile)
        semester = self.request.query_params.get('semester')
        year = self.request.query_params.get('year')
        if semester:
            queryset = queryset.filter(semester=semester)
        if year:
            queryset = queryset.filter(year=year)
        return queryset.order_by('-created_at')

    @action(detail=False, methods=['get'])
    def current(self, request):
        user = request.user
        profile = getattr(user, 'profile', None)
        current_semester = Result.objects.filter(student=profile).order_by('-created_at').first()
        if not current_semester:
            return Response({'detail': 'No results found.'}, status=status.HTTP_404_NOT_FOUND)
        semester = current_semester.semester
        year = current_semester.year
        results = Result.objects.filter(student=profile, semester=semester, year=year)
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def download_pdf(self, request):
        user = request.user
        profile = getattr(user, 'profile', None)
        semester = request.query_params.get('semester')
        year = request.query_params.get('year')
        results = Result.objects.filter(student=profile)
        if semester:
            results = results.filter(semester=semester)
        if year:
            results = results.filter(year=year)
        results = results.order_by('unit_code')
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 800, "Uzuri University Final Transcript")
        p.setFont("Helvetica", 12)
        p.drawString(100, 780, f"Student: {profile.user.get_full_name()} | Admission No: {profile.user.student_number}")
        p.drawString(100, 765, f"Programme: {getattr(profile, 'program', '')}")
        p.drawString(100, 750, f"Semester: {semester or '-'} | Year: {year or '-'}")
        y = 730
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y, "Unit Code")
        p.drawString(200, y, "Unit Name")
        p.drawString(400, y, "Hours")
        p.drawString(450, y, "Grade")
        y -= 20
        p.setFont("Helvetica", 12)
        for r in results:
            p.drawString(100, y, r.unit_code)
            p.drawString(200, y, r.unit_name)
            p.drawString(400, y, str(r.academic_hours))
            p.drawString(450, y, r.grade)
            y -= 18
            if y < 100:
                p.showPage()
                y = 800
        avg = results.aggregate(avg_marks=pd.models.Avg('marks'))['avg_marks'] or 0
        p.drawString(100, y-20, f"Current Average: {round(avg,2)}")
        all_results = Result.objects.filter(student=profile)
        cum_avg = all_results.aggregate(avg_marks=pd.models.Avg('marks'))['avg_marks'] or 0
        p.drawString(100, y-40, f"Cumulative Average: {round(cum_avg,2)}")
        rec = Recommendation.objects.filter(student=profile, semester=semester, year=year).first()
        rec_text = rec.text if rec else "No recommendation available."
        p.drawString(100, y-60, f"Recommendation: {rec_text}")
        if any(r.status == 'final' for r in results):
            p.setFont("Helvetica-Bold", 40)
            p.setFillGray(0.7, 0.5)
            p.drawString(200, 400, "FINAL")
        avg = results.aggregate(avg_marks=Avg('marks'))['avg_marks'] or 0
        p.setFillGray(0, 1)
        p.drawString(100, y-100, "Grading Scale:")
        cum_avg = all_results.aggregate(avg_marks=Avg('marks'))['avg_marks'] or 0
        for gs in GradingScale.objects.all():
            p.setFont("Helvetica", 10)
            p.drawString(100, y2, f"{gs.grade}: {gs.min_score}-{gs.max_score} ({gs.description})")
            y2 -= 14
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f"final_transcript_{profile.user.student_number}_{semester or 'all'}.pdf")

    @action(detail=False, methods=['get'])
    def download_excel(self, request):
        user = request.user
        profile = getattr(user, 'profile', None)
        semester = request.query_params.get('semester')
        year = request.query_params.get('year')
        results = Result.objects.filter(student=profile)
        if semester:
            results = results.filter(semester=semester)
        if year:
            results = results.filter(year=year)
        data = [
            {
                'Unit Code': r.unit_code,
                'Unit Name': r.unit_name,
                'Academic Hours': r.academic_hours,
                'Marks': r.marks,
                'Grade': r.grade,
                'Status': r.status,
                'Semester': r.semester,
                'Year': r.year,
            } for r in results
        ]
        df = pd.DataFrame(data)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Results')
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f"final_results_{profile.user.student_number}_{semester or 'all'}.xlsx")

    def perform_create(self, serializer):
        result = serializer.save()
        context = {
            'name': result.student.user.get_full_name(),
            'semester': result.semester,
            'unit_code': result.unit_code,
        }
        send_notification.delay(result.student.user.email, 'final_result_uploaded', context, ['email', 'in_app', 'sms'])

    def perform_update(self, serializer):
        result = serializer.save()
        context = {
            'name': result.student.user.get_full_name(),
            'semester': result.semester,
            'unit_code': result.unit_code,
        }
        send_notification.delay(result.student.user.email, 'final_result_updated', context, ['email', 'in_app', 'sms'])
