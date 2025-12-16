from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from . import models, serializers
from .models import User
from .permissions import AdminRegistrarFinanceTeacherReadOnly, TeacherCanModifyAssigned

def filter_by_school(qs, user):
    if user.is_superuser or user.role == User.Role.ADMIN:
        return qs.filter(school=user.school) if hasattr(qs.model, "school_id") and user.school_id else qs
    if hasattr(qs.model, "school_id") and user.school_id:
        return qs.filter(school=user.school)
    return qs

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = models.School.objects.all()
    serializer_class = serializers.SchoolSerializer
    permission_classes = [IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated, AdminRegistrarFinanceTeacherReadOnly]

    def get_queryset(self):
        u=self.request.user
        if u.is_superuser:
            return models.User.objects.all()
        if u.school_id:
            return models.User.objects.filter(school=u.school)
        return models.User.objects.none()

class StudentViewSet(viewsets.ModelViewSet):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    permission_classes = [IsAuthenticated, AdminRegistrarFinanceTeacherReadOnly]

    def get_queryset(self):
        u=self.request.user
        if u.role == User.Role.STUDENT and hasattr(u, "student_profile") and u.student_profile:
            return models.Student.objects.filter(id=u.student_profile.id)
        qs = models.Student.objects.all()
        return filter_by_school(qs, u)

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = models.Teacher.objects.all()
    serializer_class = serializers.TeacherSerializer
    permission_classes = [IsAuthenticated, AdminRegistrarFinanceTeacherReadOnly]

    def get_queryset(self):
        u=self.request.user
        if u.role == User.Role.TEACHER and hasattr(u, "teacher_profile") and u.teacher_profile:
            return models.Teacher.objects.filter(id=u.teacher_profile.id)
        qs = models.Teacher.objects.all()
        return filter_by_school(qs, u)

class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = models.AcademicYear.objects.all()
    serializer_class = serializers.AcademicYearSerializer
    permission_classes = [IsAuthenticated, AdminRegistrarFinanceTeacherReadOnly]

    def get_queryset(self):
        return filter_by_school(models.AcademicYear.objects.all(), self.request.user)

class TermViewSet(viewsets.ModelViewSet):
    queryset = models.Term.objects.all()
    serializer_class = serializers.TermSerializer
    permission_classes = [IsAuthenticated, AdminRegistrarFinanceTeacherReadOnly]

class GradeViewSet(viewsets.ModelViewSet):
    queryset = models.Grade.objects.all()
    serializer_class = serializers.GradeSerializer
    permission_classes = [IsAuthenticated, AdminRegistrarFinanceTeacherReadOnly]
    def get_queryset(self):
        return filter_by_school(models.Grade.objects.all(), self.request.user)

class SectionViewSet(viewsets.ModelViewSet):
    queryset = models.Section.objects.all()
    serializer_class = serializers.SectionSerializer
    permission_classes = [IsAuthenticated, AdminRegistrarFinanceTeacherReadOnly]

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = models.Subject.objects.all()
    serializer_class = serializers.SubjectSerializer
    permission_classes = [IsAuthenticated, AdminRegistrarFinanceTeacherReadOnly]
    def get_queryset(self):
        return filter_by_school(models.Subject.objects.all(), self.request.user)

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = models.Enrollment.objects.all()
    serializer_class = serializers.EnrollmentSerializer
    permission_classes = [IsAuthenticated, AdminRegistrarFinanceTeacherReadOnly]

    def get_queryset(self):
        u=self.request.user
        if u.role == User.Role.STUDENT and hasattr(u, "student_profile") and u.student_profile:
            return models.Enrollment.objects.filter(student=u.student_profile)
        return models.Enrollment.objects.all()

class TeacherAssignmentViewSet(viewsets.ModelViewSet):
    queryset = models.TeacherAssignment.objects.all()
    serializer_class = serializers.TeacherAssignmentSerializer
    permission_classes = [IsAuthenticated, AdminRegistrarFinanceTeacherReadOnly]

class AttendanceSessionViewSet(viewsets.ModelViewSet):
    queryset = models.AttendanceSession.objects.all()
    serializer_class = serializers.AttendanceSessionSerializer
    permission_classes = [IsAuthenticated, TeacherCanModifyAssigned]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = models.AttendanceRecord.objects.all()
    serializer_class = serializers.AttendanceRecordSerializer
    permission_classes = [IsAuthenticated, TeacherCanModifyAssigned]

    def get_queryset(self):
        u=self.request.user
        if u.role == User.Role.STUDENT and hasattr(u, "student_profile") and u.student_profile:
            return models.AttendanceRecord.objects.filter(student=u.student_profile)
        return models.AttendanceRecord.objects.all()

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = models.Assessment.objects.all()
    serializer_class = serializers.AssessmentSerializer
    permission_classes = [IsAuthenticated, TeacherCanModifyAssigned]

class AssessmentScoreViewSet(viewsets.ModelViewSet):
    queryset = models.AssessmentScore.objects.all()
    serializer_class = serializers.AssessmentScoreSerializer
    permission_classes = [IsAuthenticated, TeacherCanModifyAssigned]

    def perform_create(self, serializer):
        serializer.save(graded_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(graded_by=self.request.user)

    def get_queryset(self):
        u=self.request.user
        if u.role == User.Role.STUDENT and hasattr(u, "student_profile") and u.student_profile:
            return models.AssessmentScore.objects.filter(student=u.student_profile)
        return models.AssessmentScore.objects.all()

class FeeHeadViewSet(viewsets.ModelViewSet):
    queryset = models.FeeHead.objects.all()
    serializer_class = serializers.FeeHeadSerializer
    permission_classes = [IsAuthenticated, AdminRegistrarFinanceTeacherReadOnly]
    def get_queryset(self):
        return filter_by_school(models.FeeHead.objects.all(), self.request.user)

class FeeStructureViewSet(viewsets.ModelViewSet):
    queryset = models.FeeStructure.objects.all()
    serializer_class = serializers.FeeStructureSerializer
    permission_classes = [IsAuthenticated, AdminRegistrarFinanceTeacherReadOnly]

class FeeStructureItemViewSet(viewsets.ModelViewSet):
    queryset = models.FeeStructureItem.objects.all()
    serializer_class = serializers.FeeStructureItemSerializer
    permission_classes = [IsAuthenticated, AdminRegistrarFinanceTeacherReadOnly]

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = models.Invoice.objects.all()
    serializer_class = serializers.InvoiceSerializer
    permission_classes = [IsAuthenticated, AdminRegistrarFinanceTeacherReadOnly]

    def get_queryset(self):
        u=self.request.user
        if u.role == User.Role.STUDENT and hasattr(u, "student_profile") and u.student_profile:
            return models.Invoice.objects.filter(student=u.student_profile)
        return models.Invoice.objects.all()

class InvoiceItemViewSet(viewsets.ModelViewSet):
    queryset = models.InvoiceItem.objects.all()
    serializer_class = serializers.InvoiceItemSerializer
    permission_classes = [IsAuthenticated, AdminRegistrarFinanceTeacherReadOnly]

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = models.Payment.objects.all()
    serializer_class = serializers.PaymentSerializer
    permission_classes = [IsAuthenticated, AdminRegistrarFinanceTeacherReadOnly]

    def get_queryset(self):
        u=self.request.user
        if u.role == User.Role.STUDENT and hasattr(u, "student_profile") and u.student_profile:
            return models.Payment.objects.filter(student=u.student_profile)
        return models.Payment.objects.all()

class PaymentAllocationViewSet(viewsets.ModelViewSet):
    queryset = models.PaymentAllocation.objects.all()
    serializer_class = serializers.PaymentAllocationSerializer
    permission_classes = [IsAuthenticated, AdminRegistrarFinanceTeacherReadOnly]
