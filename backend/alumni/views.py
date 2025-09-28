from rest_framework import viewsets, permissions
from .models import AlumniProfile, JobPosting
from .serializers import AlumniProfileSerializer, JobPostingSerializer

class AlumniProfileViewSet(viewsets.ModelViewSet):
    queryset = AlumniProfile.objects.all()
    serializer_class = AlumniProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    permission_classes = [permissions.IsAuthenticated]
