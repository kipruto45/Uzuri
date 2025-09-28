from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import EvaluationForm, EvaluationResponse, EvaluationSummary
from .serializers import EvaluationFormSerializer, EvaluationResponseSerializer, EvaluationSummarySerializer
from django.utils import timezone
from django.db.models import Avg, Count

# Create your views here.

class StudentEvaluationViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def available(self, request):
        student = request.user.profile
        semester = request.query_params.get('semester')
        registered_units = student.unit_registrations.filter(semester=semester, status='approved').values_list('items__unit', flat=True)
        forms = EvaluationForm.objects.filter(unit_id__in=registered_units, semester=semester, active=True)
        serializer = EvaluationFormSerializer(forms, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def submit(self, request):
        form_id = request.data.get('form')
        answers = request.data.get('answers')
        comment = request.data.get('comment', '')
        student_hash = hash(str(request.user.id) + str(form_id) + str(timezone.now().date()))
        form = EvaluationForm.objects.get(id=form_id)
        semester = form.semester
        unit = form.unit
        lecturer = form.lecturer
        exists = EvaluationResponse.objects.filter(form=form, student_hash=str(student_hash)).exists()
        if exists:
            return Response({'detail': 'Already submitted.'}, status=status.HTTP_400_BAD_REQUEST)
        EvaluationResponse.objects.create(form=form, answers=answers, comment=comment, student_hash=str(student_hash))
        return Response({'detail': f'Your evaluation for {unit} has been received.'})

    @action(detail=False, methods=['get'])
    def status(self, request):
        student = request.user.profile
        semester = request.query_params.get('semester')
        registered_units = student.unit_registrations.filter(semester=semester, status='approved').values_list('items__unit', flat=True)
        forms = EvaluationForm.objects.filter(unit_id__in=registered_units, semester=semester, active=True)
        status_list = []
        for form in forms:
            submitted = EvaluationResponse.objects.filter(form=form, student_hash=hash(str(request.user.id) + str(form.id) + str(timezone.now().date()))).exists()
            status_list.append({
                'unit': form.unit.id,
                'lecturer': form.lecturer.id,
                'evaluated': submitted
            })
        return Response(status_list)

    @action(detail=False, methods=['get'])
    def history(self, request):
        student_hashes = [hash(str(request.user.id) + str(form.id) + str(timezone.now().date())) for form in EvaluationForm.objects.all()]
        responses = EvaluationResponse.objects.filter(student_hash__in=[str(h) for h in student_hashes])
        serializer = EvaluationResponseSerializer(responses, many=True)
        return Response(serializer.data)

class EvaluationSummaryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EvaluationSummary.objects.all()
    serializer_class = EvaluationSummarySerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        semester = request.query_params.get('semester')
        summaries = EvaluationSummary.objects.filter(semester=semester)
        serializer = EvaluationSummarySerializer(summaries, many=True)
        return Response(serializer.data)
