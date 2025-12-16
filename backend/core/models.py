from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class School(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        REGISTRAR = "REGISTRAR", "Registrar"
        FINANCE = "FINANCE", "Finance"
        TEACHER = "TEACHER", "Teacher"
        STUDENT = "STUDENT", "Student"

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="users", null=True, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

class Student(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="students")
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="student_profile")
    admission_no = models.CharField(max_length=50)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = [("school", "admission_no")]

    def __str__(self):
        return f"{self.admission_no} - {self.first_name} {self.last_name}"

class Teacher(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="teachers")
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="teacher_profile")
    staff_no = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class AcademicYear(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="academic_years")
    name = models.CharField(max_length=50)  # 2025/2026
    starts_on = models.DateField()
    ends_on = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = [("school", "name")]

    def __str__(self):
        return self.name

class Term(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name="terms")
    name = models.CharField(max_length=50)  # Term 1
    starts_on = models.DateField()
    ends_on = models.DateField()

    def __str__(self):
        return f"{self.academic_year.name} - {self.name}"

class Grade(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="grades")
    name = models.CharField(max_length=100)  # Grade 10
    sort_order = models.IntegerField(default=0)

    class Meta:
        unique_together = [("school", "name")]

    def __str__(self):
        return self.name

class Section(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="sections")
    name = models.CharField(max_length=50)  # A/B

    class Meta:
        unique_together = [("grade", "name")]

    def __str__(self):
        return f"{self.grade.name} {self.name}"

class Subject(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="subjects")
    code = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=120)

    class Meta:
        unique_together = [("school", "name")]

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        LEFT = "LEFT", "Left"
        SUSPENDED = "SUSPENDED", "Suspended"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name="enrollments")
    section = models.ForeignKey(Section, on_delete=models.RESTRICT, related_name="enrollments")
    enrolled_on = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    class Meta:
        unique_together = [("student", "academic_year")]

    def __str__(self):
        return f"{self.student} -> {self.section} ({self.academic_year})"

class TeacherAssignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="assignments")
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="teacher_assignments")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="teacher_assignments")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="teacher_assignments")

    class Meta:
        unique_together = [("teacher", "term", "section", "subject")]

    def __str__(self):
        return f"{self.teacher} {self.subject} {self.section} {self.term}"

class AttendanceSession(models.Model):
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="attendance_sessions")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="attendance_sessions")
    session_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_attendance_sessions")

    class Meta:
        unique_together = [("term", "section", "session_date")]

class AttendanceRecord(models.Model):
    class Status(models.TextChoices):
        PRESENT = "PRESENT", "Present"
        ABSENT = "ABSENT", "Absent"
        LATE = "LATE", "Late"

    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name="records")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance_records")
    status = models.CharField(max_length=20, choices=Status.choices)
    note = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = [("session", "student")]

class Assessment(models.Model):
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="assessments")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="assessments")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="assessments")
    name = models.CharField(max_length=120)
    max_score = models.DecimalField(max_digits=6, decimal_places=2)
    weight = models.DecimalField(max_digits=6, decimal_places=2, default=1.0)

class AssessmentScore(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name="scores")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="assessment_scores")
    score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="graded_scores")
    graded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = [("assessment", "student")]

class FeeHead(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="fee_heads")
    name = models.CharField(max_length=120)

    class Meta:
        unique_together = [("school", "name")]

class FeeStructure(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name="fee_structures")
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="fee_structures")
    name = models.CharField(max_length=120)

class FeeStructureItem(models.Model):
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE, related_name="items")
    fee_head = models.ForeignKey(FeeHead, on_delete=models.RESTRICT, related_name="structure_items")
    amount = models.DecimalField(max_digits=12, decimal_places=2)

class Invoice(models.Model):
    class Status(models.TextChoices):
        UNPAID = "UNPAID", "Unpaid"
        PARTIAL = "PARTIAL", "Partial"
        PAID = "PAID", "Paid"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="invoices")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name="invoices")
    issued_on = models.DateField(default=timezone.now)
    due_on = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UNPAID)

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    fee_head = models.ForeignKey(FeeHead, on_delete=models.RESTRICT, related_name="invoice_items")
    amount = models.DecimalField(max_digits=12, decimal_places=2)

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="payments")
    paid_on = models.DateField(default=timezone.now)
    method = models.CharField(max_length=30)  # CASH/BANK/MOBILE
    reference = models.CharField(max_length=120, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

class PaymentAllocation(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="allocations")
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="allocations")
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        unique_together = [("payment", "invoice")]
