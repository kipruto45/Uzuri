from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from calendar_app.models import CalendarEvent
from notifications.models import Notification
from django.db.models import Avg

class Department(models.Model):
	name = models.CharField(max_length=128)
	faculty = models.CharField(max_length=128)
	description = models.TextField(blank=True)
	def __str__(self):
		return self.name

class Unit(models.Model):
	code = models.CharField(max_length=16, unique=True)
	name = models.CharField(max_length=128)
	department = models.ForeignKey(Department, on_delete=models.CASCADE)
	lecturer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='lecturer_units')
	year = models.PositiveIntegerField()
	semester = models.PositiveIntegerField()
	prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
	def __str__(self):
		return f"{self.code} - {self.name}"

class Enrollment(models.Model):
	STATUS_CHOICES = [
		('active', 'Active'),
		('completed', 'Completed'),
		('dropped', 'Dropped'),
	]
	student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
	status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='active')
	enrolled_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"{self.student} - {self.unit} ({self.status})"

class LearningMaterial(models.Model):
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
	topic = models.CharField(max_length=128)
	file = models.FileField(upload_to='materials/')
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"{self.unit}: {self.topic}"

class Assignment(models.Model):
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
	title = models.CharField(max_length=128)
	description = models.TextField()
	deadline = models.DateTimeField()
	lecturer_notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	due_date = models.DateTimeField(null=True, blank=True)
	prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)
	min_score_required = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	def __str__(self):
		return f"{self.unit}: {self.title}"
	def is_eligible(self, user):
		# Check enrollment
		if not Enrollment.objects.filter(student=user, unit=self.unit).exists():
			return False, 'Not enrolled in this unit.'
		# Check prerequisites
		for prereq in self.prerequisites.all():
			sub = AssignmentSubmission.objects.filter(assignment=prereq, student=user, grade__gte=prereq.min_score_required).exists()
			if not sub:
				return False, f'Missing prerequisite: {prereq}'
		# Check deadline
		from django.utils import timezone
		if timezone.now() > self.due_date:
			return False, 'Assignment deadline has passed.'
		return True, ''

class AssignmentSubmission(models.Model):
	student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
	file = models.FileField(upload_to='submissions/')
	grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	feedback = models.TextField(blank=True)
	submitted_at = models.DateTimeField(auto_now_add=True)
	is_late = models.BooleanField(default=False)
	is_draft = models.BooleanField(default=False)
	attempt = models.PositiveIntegerField(default=1)
	plagiarism_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	def __str__(self):
		return f"{self.student} - {self.assignment} (Attempt {self.attempt})"

class Quiz(models.Model):
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
	title = models.CharField(max_length=128)
	questions = models.JSONField()
	time_limit = models.PositiveIntegerField(default=0, help_text='Time limit in minutes (0 = no limit)')
	adaptive = models.BooleanField(default=False)
	prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)
	min_score_required = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"{self.unit}: {self.title}"
	def is_eligible(self, user):
		# Check enrollment
		if not Enrollment.objects.filter(student=user, unit=self.unit).exists():
			return False, 'Not enrolled in this unit.'
		# Check prerequisites
		for prereq in self.prerequisites.all():
			attempt = QuizAttempt.objects.filter(quiz=prereq, student=user, score__gte=prereq.min_score_required).exists()
			if not attempt:
				return False, f'Missing prerequisite: {prereq}'
		return True, ''
	def get_randomized_questions(self, user=None):
		qs = list(self.questions.all())
		import random
		random.shuffle(qs)
		return qs
	def get_adaptive_questions(self, user):
		# Placeholder: select easier/harder questions based on user performance
		if not self.adaptive:
			return self.get_randomized_questions(user)
		# Example: if user struggled, pick easier questions
		last_attempt = QuizAttempt.objects.filter(quiz=self, student=user).order_by('-created_at').first()
		if last_attempt and last_attempt.score < 50:
			return list(self.questions.filter(difficulty='easy'))
		elif last_attempt and last_attempt.score > 80:
			return list(self.questions.filter(difficulty='hard'))
		else:
			return self.get_randomized_questions(user)

class QuizAttempt(models.Model):
	student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	answers = models.JSONField()
	score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	attempted_at = models.DateTimeField(auto_now_add=True)
	duration = models.PositiveIntegerField(help_text='Duration in seconds', null=True, blank=True)
	def __str__(self):
		return f"{self.student} - {self.quiz}"

class ForumThread(models.Model):
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
	student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.CharField(max_length=128)
	body = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	is_pinned = models.BooleanField(default=False)
	def __str__(self):
		return f"{self.unit}: {self.title}"

class ForumReply(models.Model):
	thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE, related_name='replies')
	student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	body = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	is_answer = models.BooleanField(default=False)
	def __str__(self):
		return f"Reply by {self.student} on {self.thread}"

class ProgressTracker(models.Model):
	student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
	percent_materials = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	percent_assignments = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	percent_quizzes = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	engagement_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	last_updated = models.DateTimeField(auto_now=True)
	def __str__(self):
		return f"{self.student} - {self.unit} Progress"

class EmasomoNotification(models.Model):
	student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	type = models.CharField(max_length=32)
	message = models.TextField()
	status = models.CharField(max_length=16, choices=[('read','Read'),('unread','Unread')], default='unread')
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"{self.student} - {self.type}"

class Badge(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    icon = models.CharField(max_length=128, blank=True)  # URL or icon name
    criteria = models.CharField(max_length=256)  # e.g. 'complete_100_percent', 'top_forum_contributor'
    def __str__(self):
        return self.name

class AwardedBadge(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.student} - {self.badge}"

class AIInsightLog(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    insight = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=64, blank=True)  # e.g. 'progress', 'forum', 'quiz'
    def __str__(self):
        return f"{self.student} - {self.insight[:30]}..."

class Group(models.Model):
	name = models.CharField(max_length=128)
	members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='emasomo_groups')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class GroupAssignment(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    file = models.FileField(upload_to='group_submissions/')
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.group} - {self.assignment}"

class PeerReview(models.Model):
    submission = models.ForeignKey(AssignmentSubmission, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Review by {self.reviewer}"

class LiveSession(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    link = models.URLField()
    platform = models.CharField(max_length=32, choices=[('zoom','Zoom'),('meet','Google Meet'),('jitsi','Jitsi')])
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.unit} - {self.title}"

class Guardian(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guardian_profile')
    phone = models.CharField(max_length=32)
    email = models.EmailField()
    def __str__(self):
        return f"Guardian: {self.user}"

class StudentGuardianLink(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guardian_links')
    guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.student} - {self.guardian}"

class AuditLog(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='emasomo_audit_logs')
	action = models.CharField(max_length=128)
	details = models.JSONField(default=dict, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"{self.user} - {self.action}"

class MarketplaceItem(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    file = models.FileField(upload_to='marketplace/')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Purchase(models.Model):
    item = models.ForeignKey(MarketplaceItem, on_delete=models.CASCADE)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.buyer} - {self.item}"

class DashboardWidget(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    widget_type = models.CharField(max_length=64)
    config = models.JSONField(default=dict, blank=True)
    position = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.student} - {self.widget_type}"

@receiver(post_save, sender=ProgressTracker)
def award_badges_on_progress(sender, instance, **kwargs):
    # 100% Completion
    if instance.percent_materials == 100 and not AwardedBadge.objects.filter(student=instance.student, badge__criteria='complete_100_percent').exists():
        badge = Badge.objects.filter(criteria='complete_100_percent').first()
        if badge:
            AwardedBadge.objects.create(student=instance.student, badge=badge)
    # Assignment Master
    if instance.percent_assignments == 100 and not AwardedBadge.objects.filter(student=instance.student, badge__criteria='all_assignments_completed').exists():
        badge = Badge.objects.filter(criteria='all_assignments_completed').first()
        if badge:
            AwardedBadge.objects.create(student=instance.student, badge=badge)
    # Quiz Whiz
    if instance.percent_quizzes >= 90 and not AwardedBadge.objects.filter(student=instance.student, badge__criteria='quiz_high_score').exists():
        badge = Badge.objects.filter(criteria='quiz_high_score').first()
        if badge:
            AwardedBadge.objects.create(student=instance.student, badge=badge)
    # Engagement Pro
    if instance.engagement_score >= 80 and not AwardedBadge.objects.filter(student=instance.student, badge__criteria='high_engagement').exists():
        badge = Badge.objects.filter(criteria='high_engagement').first()
        if badge:
            AwardedBadge.objects.create(student=instance.student, badge=badge)

@receiver(post_save, sender=ForumReply)
def award_forum_star_badge(sender, instance, **kwargs):
    # Top forum contributor (e.g., 50+ replies)
    reply_count = ForumReply.objects.filter(student=instance.student).count()
    if reply_count >= 50 and not AwardedBadge.objects.filter(student=instance.student, badge__criteria='top_forum_contributor').exists():
        badge = Badge.objects.filter(criteria='top_forum_contributor').first()
        if badge:
            AwardedBadge.objects.create(student=instance.student, badge=badge)

@receiver(post_save, sender=AIInsightLog)
def notify_ai_insight(sender, instance, **kwargs):
    Notification.objects.create(
        user=instance.student,
        category='academic',
        type='ai-insight',
        title='AI Insight',
        message=instance.insight,
        urgency='info',
        channels=["in_app"],
    )

# Deeper AI analytics and recommendations
@receiver(post_save, sender=ProgressTracker)
def deeper_ai_recommendations(sender, instance, **kwargs):
    # Example: Recommend focus area based on lowest progress
    areas = {
        'Materials': instance.percent_materials,
        'Assignments': instance.percent_assignments,
        'Quizzes': instance.percent_quizzes,
        'Engagement': instance.engagement_score,
    }
    min_area = min(areas, key=areas.get)
    if areas[min_area] < 60:
        AIInsightLog.objects.create(
            student=instance.student,
            insight=f"AI: Focus on {min_area} to improve your overall performance in {instance.unit.name}.",
            source='ai-recommendation')
