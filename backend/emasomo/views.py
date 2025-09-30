from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *
from .permissions import IsStudent, IsLecturer, IsOwnerOrReadOnly, IsEnrolledOrLecturer
from django.db.models import F, Avg, Count
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.throttling import ScopedRateThrottle
from django.utils import timezone
from rest_framework import exceptions
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter

class DepartmentViewSet(viewsets.ModelViewSet):
	queryset = Department.objects.all()
	serializer_class = DepartmentSerializer
	permission_classes = [permissions.IsAuthenticated]

class UnitViewSet(viewsets.ModelViewSet):
	queryset = Unit.objects.all()
	serializer_class = UnitSerializer
	permission_classes = [permissions.IsAuthenticated]

	@action(detail=True, methods=['get'], url_path='dashboard')
	def dashboard(self, request, pk=None):
		unit = self.get_object()
		progress = ProgressTracker.objects.filter(student=request.user, unit=unit).first()
		assignments = Assignment.objects.filter(unit=unit)
		quizzes = Quiz.objects.filter(unit=unit)
		materials = LearningMaterial.objects.filter(unit=unit)
		forum_threads = ForumThread.objects.filter(unit=unit)
		data = {
			'unit': UnitSerializer(unit).data,
			'progress': ProgressTrackerSerializer(progress).data if progress else {},
			'assignments': AssignmentSerializer(assignments, many=True).data,
			'quizzes': QuizSerializer(quizzes, many=True).data,
			'materials': LearningMaterialSerializer(materials, many=True).data,
			'forum_threads': ForumThreadSerializer(forum_threads, many=True).data,
		}
		return Response(data)

class EnrollmentViewSet(viewsets.ModelViewSet):
	queryset = Enrollment.objects.all()
	serializer_class = EnrollmentSerializer
	permission_classes = [permissions.IsAuthenticated, IsStudent]

	@action(detail=False, methods=['get'], url_path='available-units')
	def available_units(self, request):
		student = request.user
		# TODO: Add real eligibility logic
		units = Unit.objects.all()
		serializer = UnitSerializer(units, many=True)
		return Response(serializer.data)

	@action(detail=True, methods=['post'], url_path='enroll')
	def enroll(self, request, pk=None):
		student = request.user
		unit = self.get_object()
		# TODO: Add eligibility checks
		enrollment, created = Enrollment.objects.get_or_create(student=student, unit=unit)
		if created:
			ProgressTracker.objects.get_or_create(student=student, unit=unit)
		return Response({'status': 'enrolled', 'enrollment_id': enrollment.id})

	@action(detail=False, methods=['get'], url_path='my-courses')
	def my_courses(self, request):
		enrollments = Enrollment.objects.filter(student=request.user, status='active')
		serializer = EnrollmentSerializer(enrollments, many=True)
		return Response(serializer.data)

class LearningMaterialViewSet(viewsets.ModelViewSet):
    queryset = LearningMaterial.objects.all()
    serializer_class = LearningMaterialSerializer
    permission_classes = [permissions.IsAuthenticated, IsEnrolledOrLecturer]

    @action(detail=True, methods=['get'], url_path='download')
    def download(self, request, pk=None):
        material = self.get_object()
        if material.file.name.endswith('.pdf'):
            # Add watermark to PDF
            watermark_text = f"Uzuri University | {request.user.email} | {request.user.student_number}"
            # Create watermark PDF in memory
            watermark_io = io.BytesIO()
            c = canvas.Canvas(watermark_io)
            c.setFont('Helvetica', 24)
            c.setFillColorRGB(0.6, 0.6, 0.6, alpha=0.3)
            c.saveState()
            c.translate(300, 400)
            c.rotate(45)
            c.drawString(0, 0, watermark_text)
            c.restoreState()
            c.save()
            watermark_io.seek(0)
            # Merge watermark with original PDF
            original_pdf = PdfReader(material.file)
            watermark_pdf = PdfReader(watermark_io)
            writer = PdfWriter()
            watermark_page = watermark_pdf.pages[0]
            for page in original_pdf.pages:
                page.merge_page(watermark_page)
                writer.add_page(page)
            output_io = io.BytesIO()
            writer.write(output_io)
            output_io.seek(0)
            return FileResponse(output_io, as_attachment=True, filename=f"watermarked_{material.file.name}")
        # For non-PDF, just return the file
        return FileResponse(material.file, as_attachment=True)
        # Update progress
        ProgressTracker.objects.filter(student=request.user, unit=material.unit).update(percent_materials=F('percent_materials')+10)

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsEnrolledOrLecturer]

    @action(detail=True, methods=['get'], url_path='submissions')
    def submissions(self, request, pk=None):
        assignment = self.get_object()
        submissions = AssignmentSubmission.objects.filter(assignment=assignment, student=request.user)
        serializer = AssignmentSubmissionSerializer(submissions, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        assignment = self.get_object()
        eligible, reason = assignment.is_eligible(request.user)
        if not eligible:
            raise exceptions.PermissionDenied(detail=reason)
        return super().retrieve(request, *args, **kwargs)

class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    queryset = AssignmentSubmission.objects.all()
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Check deadline, allow drafts, check for late, plagiarism, etc.
        assignment = serializer.validated_data['assignment']
        is_late = timezone.now() > assignment.deadline
        attempt = AssignmentSubmission.objects.filter(student=self.request.user, assignment=assignment).count() + 1
        # TODO: Integrate with plagiarism checker
        serializer.save(student=self.request.user, is_late=is_late, attempt=attempt)
        # Update progress
        ProgressTracker.objects.filter(student=self.request.user, unit=assignment.unit).update(percent_assignments=F('percent_assignments')+20)

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated, IsEnrolledOrLecturer]

    @action(detail=True, methods=['get'], url_path='results')
    def results(self, request, pk=None):
        quiz = self.get_object()
        attempts = QuizAttempt.objects.filter(quiz=quiz, student=request.user)
        serializer = QuizAttemptSerializer(attempts, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        quiz = self.get_object()
        eligible, reason = quiz.is_eligible(request.user)
        if not eligible:
            raise exceptions.PermissionDenied(detail=reason)
        # Randomize/adapt questions
        if quiz.adaptive:
            questions = quiz.get_adaptive_questions(request.user)
        else:
            questions = quiz.get_randomized_questions(request.user)
        data = self.get_serializer(quiz).data
        data['questions'] = [q.id for q in questions]
        return Response(data)

    def create(self, request, *args, **kwargs):
        quiz = self.get_object()
        if quiz.time_limit > 0:
            start_time = timezone.now()
            end_time = start_time + timezone.timedelta(minutes=quiz.time_limit)
            request.data['start_time'] = start_time
            request.data['end_time'] = end_time
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class QuizAttemptViewSet(viewsets.ModelViewSet):
    queryset = QuizAttempt.objects.all()
    serializer_class = QuizAttemptSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        quiz = serializer.validated_data['quiz']
        # TODO: Enforce time limit, randomize questions, adaptive difficulty
        serializer.save(student=self.request.user)
        # Update progress
        ProgressTracker.objects.filter(student=self.request.user, unit=quiz.unit).update(percent_quizzes=F('percent_quizzes')+20)

class ForumThreadViewSet(viewsets.ModelViewSet):
    queryset = ForumThread.objects.all()
    serializer_class = ForumThreadSerializer
    permission_classes = [permissions.IsAuthenticated, IsEnrolledOrLecturer]

    @action(detail=True, methods=['post'], url_path='reply')
    def reply(self, request, pk=None):
        thread = self.get_object()
        reply = ForumReply.objects.create(thread=thread, student=request.user, body=request.data.get('body'))
        # Update engagement score
        ProgressTracker.objects.filter(student=request.user, unit=thread.unit).update(engagement_score=F('engagement_score')+5)
        return Response(ForumReplySerializer(reply).data)

class ForumReplyViewSet(viewsets.ModelViewSet):
	queryset = ForumReply.objects.all()
	serializer_class = ForumReplySerializer
	permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class ProgressTrackerViewSet(viewsets.ModelViewSet):
	queryset = ProgressTracker.objects.all()
	serializer_class = ProgressTrackerSerializer
	permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

	@action(detail=False, methods=['get'], url_path='overview')
	def overview(self, request):
		progress = ProgressTracker.objects.filter(student=request.user)
		serializer = ProgressTrackerSerializer(progress, many=True)
		return Response(serializer.data)

	@action(detail=False, methods=['get'], url_path='insights')
	def insights(self, request):
		progress = ProgressTracker.objects.filter(student=request.user)
		insights = []
		for p in progress:
			if p.percent_assignments < 80:
				insights.append(f"You’ve completed {p.percent_assignments}% of assignments in {p.unit.name}. Focus on assignments to reach 80%.")
		if not insights:
			insights.append("Great job! Keep up the good work.")
		return Response({'insights': insights})

class EmasomoNotificationViewSet(viewsets.ModelViewSet):
	queryset = EmasomoNotification.objects.all()
	serializer_class = EmasomoNotificationSerializer
	permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

	@action(detail=True, methods=['patch'], url_path='mark-read')
	def mark_read(self, request, pk=None):
		notification = self.get_object()
		notification.status = 'read'
		notification.save()
		return Response({'status': 'read'})

class AnalyticsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='student-dashboard')
    def student_dashboard(self, request):
        # Progress ring chart, heatmap, performance graphs
        progress = ProgressTracker.objects.filter(student=request.user)
        avg_assignment = progress.aggregate(avg=Avg('percent_assignments'))['avg'] or 0
        avg_quiz = progress.aggregate(avg=Avg('percent_quizzes'))['avg'] or 0
        avg_materials = progress.aggregate(avg=Avg('percent_materials'))['avg'] or 0
        engagement = progress.aggregate(avg=Avg('engagement_score'))['avg'] or 0
        # Heatmap: activity by week
        activity = ProgressTracker.objects.filter(student=request.user).annotate(week=F('last_updated__week')).values('week').annotate(count=Count('id')).order_by('week')
        return Response({
            'avg_assignment': avg_assignment,
            'avg_quiz': avg_quiz,
            'avg_materials': avg_materials,
            'engagement': engagement,
            'activity_heatmap': list(activity),
        })

    @action(detail=False, methods=['get'], url_path='lecturer-dashboard')
    def lecturer_dashboard(self, request):
        # Analytics for lecturer's units
        if not hasattr(request.user, 'is_lecturer') or not request.user.is_lecturer:
            return Response({'error': 'Not a lecturer'}, status=403)
        units = Unit.objects.filter(lecturer=request.user)
        data = []
        for unit in units:
            enrollments = Enrollment.objects.filter(unit=unit, status='active').count()
            avg_progress = ProgressTracker.objects.filter(unit=unit).aggregate(avg=Avg('percent_materials'))['avg'] or 0
            avg_assignment = ProgressTracker.objects.filter(unit=unit).aggregate(avg=Avg('percent_assignments'))['avg'] or 0
            avg_quiz = ProgressTracker.objects.filter(unit=unit).aggregate(avg=Avg('percent_quizzes'))['avg'] or 0
            data.append({
                'unit': unit.name,
                'enrollments': enrollments,
                'avg_progress': avg_progress,
                'avg_assignment': avg_assignment,
                'avg_quiz': avg_quiz,
            })
        return Response({'units': data})

    @action(detail=False, methods=['get'], url_path='engagement-stats')
    def engagement_stats(self, request):
        # Forum, assignment, quiz engagement
        progress = ProgressTracker.objects.filter(student=request.user)
        forum_count = ForumReply.objects.filter(student=request.user).count()
        assignment_count = AssignmentSubmission.objects.filter(student=request.user).count()
        quiz_count = QuizAttempt.objects.filter(student=request.user).count()
        return Response({
            'forum_replies': forum_count,
            'assignments_submitted': assignment_count,
            'quizzes_attempted': quiz_count,
        })

class BadgeViewSet(viewsets.ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [permissions.IsAuthenticated]

class AwardedBadgeViewSet(viewsets.ModelViewSet):
    queryset = AwardedBadge.objects.all()
    serializer_class = AwardedBadgeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class AIInsightLogViewSet(viewsets.ModelViewSet):
    queryset = AIInsightLog.objects.all()
    serializer_class = AIInsightLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class InsightsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='ai-suggestions')
    def ai_suggestions(self, request):
        # Example: AI-powered suggestions based on progress, forum, quiz, etc.
        progress = ProgressTracker.objects.filter(student=request.user)
        suggestions = []
        for p in progress:
            if p.percent_assignments < 80:
                suggestions.append(f"AI: Complete more assignments in {p.unit.name} to boost your grade.")
            if p.engagement_score < 30:
                suggestions.append(f"AI: Participate in forums for {p.unit.name} to increase your engagement.")
        if not suggestions:
            suggestions.append("AI: You're on track! Keep it up.")
        # Log insights
        for s in suggestions:
            AIInsightLog.objects.create(student=request.user, insight=s, source='progress')
        return Response({'ai_suggestions': suggestions})

from .models import Group, GroupAssignment, PeerReview, LiveSession, Guardian, StudentGuardianLink, AuditLog, MarketplaceItem, Purchase, DashboardWidget
from .serializers import (
    GroupSerializer, GroupAssignmentSerializer, PeerReviewSerializer, LiveSessionSerializer,
    GuardianSerializer, StudentGuardianLinkSerializer, AuditLogSerializer,
    MarketplaceItemSerializer, PurchaseSerializer, DashboardWidgetSerializer
)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsStudent]

class GroupAssignmentViewSet(viewsets.ModelViewSet):
    queryset = GroupAssignment.objects.all()
    serializer_class = GroupAssignmentSerializer
    permission_classes = [IsAuthenticated, IsStudent]

class PeerReviewViewSet(viewsets.ModelViewSet):
    queryset = PeerReview.objects.all()
    serializer_class = PeerReviewSerializer
    permission_classes = [IsAuthenticated, IsStudent]

class LiveSessionViewSet(viewsets.ModelViewSet):
    queryset = LiveSession.objects.all()
    serializer_class = LiveSessionSerializer
    permission_classes = [IsAuthenticated, IsStudent]

class GuardianViewSet(viewsets.ModelViewSet):
    queryset = Guardian.objects.all()
    serializer_class = GuardianSerializer
    permission_classes = [IsAuthenticated]

class StudentGuardianLinkViewSet(viewsets.ModelViewSet):
    queryset = StudentGuardianLink.objects.all()
    serializer_class = StudentGuardianLinkSerializer
    permission_classes = [IsAuthenticated, IsStudent]

class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]

class MarketplaceItemViewSet(viewsets.ModelViewSet):
    queryset = MarketplaceItem.objects.all()
    serializer_class = MarketplaceItemSerializer
    permission_classes = [IsAuthenticated]

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated, IsStudent]

class DashboardWidgetViewSet(viewsets.ModelViewSet):
    queryset = DashboardWidget.objects.all()
    serializer_class = DashboardWidgetSerializer
    permission_classes = [IsAuthenticated, IsStudent]

class LoginWithEmailView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'login'
    # Login must be publicly accessible so tests can POST credentials
    permission_classes = []
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
