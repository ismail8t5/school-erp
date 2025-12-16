from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r"schools", views.SchoolViewSet)
router.register(r"users", views.UserViewSet)
router.register(r"students", views.StudentViewSet)
router.register(r"teachers", views.TeacherViewSet)

router.register(r"academic-years", views.AcademicYearViewSet)
router.register(r"terms", views.TermViewSet)
router.register(r"grades", views.GradeViewSet)
router.register(r"sections", views.SectionViewSet)
router.register(r"subjects", views.SubjectViewSet)
router.register(r"enrollments", views.EnrollmentViewSet)
router.register(r"teacher-assignments", views.TeacherAssignmentViewSet)

router.register(r"attendance-sessions", views.AttendanceSessionViewSet)
router.register(r"attendance-records", views.AttendanceRecordViewSet)

router.register(r"assessments", views.AssessmentViewSet)
router.register(r"assessment-scores", views.AssessmentScoreViewSet)

router.register(r"fee-heads", views.FeeHeadViewSet)
router.register(r"fee-structures", views.FeeStructureViewSet)
router.register(r"fee-structure-items", views.FeeStructureItemViewSet)
router.register(r"invoices", views.InvoiceViewSet)
router.register(r"invoice-items", views.InvoiceItemViewSet)
router.register(r"payments", views.PaymentViewSet)
router.register(r"payment-allocations", views.PaymentAllocationViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls)),
]
