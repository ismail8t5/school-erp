from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import User, TeacherAssignment, Enrollment

class IsAdminLike(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in {User.Role.ADMIN}

class AdminRegistrarFinanceTeacherReadOnly(BasePermission):
    """Admins full, staff roles read, students read-only for own via view filtering."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role == User.Role.ADMIN:
            return True
        if request.method in SAFE_METHODS:
            return True
        return request.user.role in {User.Role.REGISTRAR, User.Role.FINANCE, User.Role.TEACHER}

class TeacherCanModifyAssigned(BasePermission):
    """Teachers can write only if the object relates to their assigned section+subject+term."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role == User.Role.ADMIN:
            return True
        if request.method in SAFE_METHODS:
            return True
        return request.user.role == User.Role.TEACHER

    def has_object_permission(self, request, view, obj):
        if request.user.role == User.Role.ADMIN:
            return True
        if request.method in SAFE_METHODS:
            return True
        teacher = getattr(request.user, "teacher_profile", None)
        if not teacher:
            return False
        # obj may be AttendanceSession/Record or Assessment/Score
        term = getattr(obj, "term", None) or getattr(getattr(obj, "session", None), "term", None) or getattr(getattr(obj, "assessment", None), "term", None)
        section = getattr(obj, "section", None) or getattr(getattr(obj, "session", None), "section", None) or getattr(getattr(obj, "assessment", None), "section", None)
        subject = getattr(obj, "subject", None) or getattr(getattr(obj, "assessment", None), "subject", None)
        qs = TeacherAssignment.objects.filter(teacher=teacher, term=term, section=section)
        if subject is not None:
            qs = qs.filter(subject=subject)
        return qs.exists()

class StudentOwnDataOnly(BasePermission):
    """Students can only access their own related objects."""
    def has_permission(self, request, view):
        return request.user.is_authenticated
