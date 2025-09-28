from django.contrib import admin
from .models import CollaborationSession, DocumentEdit, Whiteboard

admin.site.register(CollaborationSession)
admin.site.register(DocumentEdit)
admin.site.register(Whiteboard)
