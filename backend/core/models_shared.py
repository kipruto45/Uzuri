from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # Role field: keeps track of user role (student, admin, registrar, etc.)
    role = models.CharField(max_length=32, default='student')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    def __str__(self):
        return self.email

class Disability(models.Model):
    CATEGORY_CHOICES = [
        ('physical', 'Physical'),
        ('visual', 'Visual'),
        ('hearing', 'Hearing'),
        ('cognitive', 'Cognitive'),
        ('other', 'Other'),
    ]
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name='disabilities', null=True, blank=True)
    category = models.CharField(max_length=16, choices=CATEGORY_CHOICES, default='other')
    name = models.CharField(max_length=32, default="General")
    support_needs = models.TextField(blank=True)
    tagged_for_reporting = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.student} - {self.get_category_display()}"

class StudyMode(models.Model):
    MODE_CHOICES = [
        ('full_time', 'Full-Time'),
        ('part_time', 'Part-Time'),
        ('distance', 'Distance/Online'),
    ]
    name = models.CharField(max_length=32, choices=MODE_CHOICES, unique=True)
    def __str__(self):
        return self.get_name_display()

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    program = models.CharField(max_length=100)
    year = models.IntegerField()
    contact_info = models.CharField(max_length=255)
    emergency_contact = models.CharField(max_length=255)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    digital_id_qr = models.ImageField(upload_to='student_qr/', blank=True, null=True)
    study_mode = models.ForeignKey(StudyMode, on_delete=models.SET_NULL, null=True, blank=True)
    disability = models.ForeignKey(Disability, on_delete=models.SET_NULL, null=True, blank=True, related_name='student_disability')
    student_id = models.CharField(max_length=32, unique=True, blank=True, editable=False, null=True)
    def save(self, *args, **kwargs):
        if not self.student_id:
            # Dynamic codes (replace with actual lookups if you have related models)
            self.student_id = f"UZ-{self.year}-{self.program[:2].upper()}-{self.user.id}"
        super().save(*args, **kwargs)
    def __str__(self):
        email = self.user.email if self.user else "No Email"
        return f"Profile: {email}"
