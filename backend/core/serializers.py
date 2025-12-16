from rest_framework import serializers
from . import models

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.School
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["id","email","role","school","is_active","is_staff","date_joined"]
        read_only_fields = ["date_joined"]

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = "__all__"

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = "__all__"

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AcademicYear
        fields = "__all__"

class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Term
        fields = "__all__"

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Grade
        fields = "__all__"

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Section
        fields = "__all__"

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subject
        fields = "__all__"

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Enrollment
        fields = "__all__"

class TeacherAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TeacherAssignment
        fields = "__all__"

class AttendanceSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttendanceSession
        fields = "__all__"

class AttendanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttendanceRecord
        fields = "__all__"

class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Assessment
        fields = "__all__"

class AssessmentScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AssessmentScore
        fields = "__all__"

class FeeHeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FeeHead
        fields = "__all__"

class FeeStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FeeStructure
        fields = "__all__"

class FeeStructureItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FeeStructureItem
        fields = "__all__"

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Invoice
        fields = "__all__"

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InvoiceItem
        fields = "__all__"

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = "__all__"

class PaymentAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentAllocation
        fields = "__all__"
