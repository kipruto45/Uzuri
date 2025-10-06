from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db import transaction

class EvaluationForm(models.Model):
    unit = models.ForeignKey('core.Unit', on_delete=models.CASCADE)
    lecturer = models.ForeignKey('core.CustomUser', on_delete=models.CASCADE, limit_choices_to={'role': 'lecturer'})
    semester = models.CharField(max_length=20)
    questions = models.JSONField(default=list)  # List of standard questions
    active = models.BooleanField(default=True)
    deadline = models.DateTimeField(null=True, blank=True)  # Deadline enforcement
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_open(self):
        return self.active and (not self.deadline or timezone.now() < self.deadline)

    def close_if_past_deadline(self):
        if self.deadline and timezone.now() > self.deadline:
            self.active = False
            self.save(update_fields=['active'])

    def __str__(self):
        return f"{self.unit} - {self.lecturer} ({self.semester})"

class EvaluationResponse(models.Model):
    form = models.ForeignKey(EvaluationForm, on_delete=models.CASCADE)
    answers = models.JSONField(default=dict)  # {question_id: score}
    comment = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    # student FK is not stored for anonymity, but can use a hash or session for restriction
    student_hash = models.CharField(max_length=64, db_index=True)  # anonymized identifier
    gamified = models.BooleanField(default=False)  # For badge/completion

    def __str__(self):
        return f"Response for {self.form} at {self.submitted_at}"

    @staticmethod
    def submit_evaluation(form, answers, comment, student_hash):
        if not form.is_open():
            raise Exception('Evaluation period closed.')
        if EvaluationResponse.objects.filter(form=form, student_hash=student_hash).exists():
            raise Exception('Already submitted.')
        with transaction.atomic():
            response = EvaluationResponse.objects.create(
                form=form, answers=answers, comment=comment, student_hash=student_hash
            )
            EvaluationSummary.update_summary(form)
            return response

class EvaluationSummary(models.Model):
    unit = models.ForeignKey('core.Unit', on_delete=models.CASCADE)
    lecturer = models.ForeignKey('core.CustomUser', on_delete=models.CASCADE, limit_choices_to={'role': 'lecturer'})
    semester = models.CharField(max_length=20)
    avg_scores = models.JSONField(default=dict)  # {question_id: avg_score}
    participation_rate = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True)
    # Analytics fields
    strong_areas = models.JSONField(default=list, blank=True)
    weak_areas = models.JSONField(default=list, blank=True)
    trend_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Summary: {self.unit} - {self.lecturer} ({self.semester})"

    @staticmethod
    def update_summary(form):
        responses = EvaluationResponse.objects.filter(form=form)
        if not responses.exists():
            return
        question_keys = form.questions
        avg_scores = {}
        for q in question_keys:
            scores = [r.answers.get(str(q), 0) for r in responses if str(q) in r.answers]
            avg_scores[q] = round(sum(scores)/len(scores), 2) if scores else 0
        participation = responses.count() / max(1, form.unit.unitregistrationitem_set.count())
        # Analytics: strong/weak areas
        sorted_scores = sorted(avg_scores.items(), key=lambda x: x[1], reverse=True)
        strong_areas = [k for k, v in sorted_scores[:2]]
        weak_areas = [k for k, v in sorted_scores[-2:]]
        # Trend data (could be extended)
        trend_data = {'count': responses.count()}
        summary, _ = EvaluationSummary.objects.get_or_create(
            unit=form.unit, lecturer=form.lecturer, semester=form.semester
        )
        summary.avg_scores = avg_scores
        summary.participation_rate = round(participation, 2)
        summary.strong_areas = strong_areas
        summary.weak_areas = weak_areas
        summary.trend_data = trend_data
        summary.save()

    @staticmethod
    def badge_earned(student_profile, semester):
        # Returns True if student has evaluated all registered units for the semester
        registered_units = student_profile.unit_registrations.filter(semester=semester, status='approved').values_list('items__unit', flat=True)
        forms = EvaluationForm.objects.filter(unit_id__in=registered_units, semester=semester, active=True)
        for form in forms:
            student_hash = hash(str(student_profile.user.id) + str(form.id) + str(timezone.now().date()))
            if not EvaluationResponse.objects.filter(form=form, student_hash=str(student_hash)).exists():
                return False
        return True
