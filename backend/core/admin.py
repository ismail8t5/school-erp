from django.contrib import admin
from . import models

for m in [
    models.School, models.User, models.Student, models.Teacher,
    models.AcademicYear, models.Term, models.Grade, models.Section, models.Subject,
    models.Enrollment, models.TeacherAssignment,
    models.AttendanceSession, models.AttendanceRecord,
    models.Assessment, models.AssessmentScore,
    models.FeeHead, models.FeeStructure, models.FeeStructureItem,
    models.Invoice, models.InvoiceItem, models.Payment, models.PaymentAllocation
]:
    admin.site.register(m)
