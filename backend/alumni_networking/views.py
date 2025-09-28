from rest_framework import viewsets, permissions
from .models import AlumniMentor, MentorshipMatch
from .serializers import AlumniMentorSerializer, MentorshipMatchSerializer

class AlumniMentorViewSet(viewsets.ModelViewSet):
    queryset = AlumniMentor.objects.all()
    serializer_class = AlumniMentorSerializer
    permission_classes = [permissions.IsAuthenticated]

class MentorshipMatchViewSet(viewsets.ModelViewSet):
    queryset = MentorshipMatch.objects.all()
    serializer_class = MentorshipMatchSerializer
    permission_classes = [permissions.IsAuthenticated]
