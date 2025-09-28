from django.db import models
from django.conf import settings

class AlumniMentor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='alumni_mentors')
    bio = models.TextField()
    expertise = models.CharField(max_length=128)

class MentorshipMatch(models.Model):
    mentor = models.ForeignKey(AlumniMentor, on_delete=models.CASCADE, related_name='mentorship_matches')
    mentee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mentorships')
    matched_at = models.DateTimeField(auto_now_add=True)
