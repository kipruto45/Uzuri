from rest_framework import viewsets, permissions
from .models import CollaborationSession, DocumentEdit, Whiteboard
from .serializers import CollaborationSessionSerializer, DocumentEditSerializer, WhiteboardSerializer

class CollaborationSessionViewSet(viewsets.ModelViewSet):
    queryset = CollaborationSession.objects.all()
    serializer_class = CollaborationSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

class DocumentEditViewSet(viewsets.ModelViewSet):
    queryset = DocumentEdit.objects.all()
    serializer_class = DocumentEditSerializer
    permission_classes = [permissions.IsAuthenticated]

class WhiteboardViewSet(viewsets.ModelViewSet):
    queryset = Whiteboard.objects.all()
    serializer_class = WhiteboardSerializer
    permission_classes = [permissions.IsAuthenticated]
