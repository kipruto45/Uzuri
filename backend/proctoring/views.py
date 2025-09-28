from rest_framework import viewsets, permissions
from .models import ProctoringSession, PlagiarismReport
from .serializers import ProctoringSessionSerializer, PlagiarismReportSerializer

class ProctoringSessionViewSet(viewsets.ModelViewSet):
    queryset = ProctoringSession.objects.all()
    serializer_class = ProctoringSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

class PlagiarismReportViewSet(viewsets.ModelViewSet):
    queryset = PlagiarismReport.objects.all()
    serializer_class = PlagiarismReportSerializer
    permission_classes = [permissions.IsAuthenticated]
