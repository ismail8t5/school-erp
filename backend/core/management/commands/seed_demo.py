from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import School, User, Student, Teacher, AcademicYear, Term, Grade, Section, Subject, Enrollment, TeacherAssignment, FeeHead, FeeStructure, FeeStructureItem, Invoice, InvoiceItem

class Command(BaseCommand):
    help = "Seed demo data (school, users, grade/section, subject, enrollment, fee structure)."

    def handle(self, *args, **options):
        school, _ = School.objects.get_or_create(code="DEMO", defaults={"name":"Demo School"})
        password = "Passw0rd!"

        def mkuser(email, role, is_staff=True):
            u, created = User.objects.get_or_create(email=email, defaults={
                "school": school,
                "role": role,
                "is_staff": is_staff,
                "is_active": True,
            })
            if created:
                u.set_password(password)
                u.save()
            return u

        admin = mkuser("admin@example.com", User.Role.ADMIN, is_staff=True)
        admin.is_superuser = True
        admin.is_staff = True
        admin.save()

        registrar = mkuser("registrar@example.com", User.Role.REGISTRAR, is_staff=True)
        finance = mkuser("finance@example.com", User.Role.FINANCE, is_staff=True)
        teacher_u = mkuser("teacher@example.com", User.Role.TEACHER, is_staff=True)
        student_u = mkuser("student@example.com", User.Role.STUDENT, is_staff=False)

        teacher, _ = Teacher.objects.get_or_create(school=school, user=teacher_u, defaults={"first_name":"Terry","last_name":"Teacher","staff_no":"T001"})
        student, _ = Student.objects.get_or_create(school=school, user=student_u, defaults={"first_name":"Sam","last_name":"Student","admission_no":"A0001"})

        ay, _ = AcademicYear.objects.get_or_create(school=school, name="2025/2026", defaults={"starts_on":"2025-09-01","ends_on":"2026-07-15","is_active":True})
        term1, _ = Term.objects.get_or_create(academic_year=ay, name="Term 1", defaults={"starts_on":"2025-09-01","ends_on":"2025-12-20"})

        g10, _ = Grade.objects.get_or_create(school=school, name="Grade 10", defaults={"sort_order":10})
        secA, _ = Section.objects.get_or_create(grade=g10, name="A")
        math, _ = Subject.objects.get_or_create(school=school, name="Mathematics", defaults={"code":"MATH"})

        Enrollment.objects.get_or_create(student=student, academic_year=ay, defaults={"section":secA, "enrolled_on":timezone.now().date()})
        TeacherAssignment.objects.get_or_create(teacher=teacher, term=term1, section=secA, subject=math)

        tuition, _ = FeeHead.objects.get_or_create(school=school, name="Tuition")
        exam, _ = FeeHead.objects.get_or_create(school=school, name="Exam Fee")
        fs, _ = FeeStructure.objects.get_or_create(academic_year=ay, grade=g10, name="Standard G10 Fees")
        FeeStructureItem.objects.get_or_create(fee_structure=fs, fee_head=tuition, defaults={"amount":"1200.00"})
        FeeStructureItem.objects.get_or_create(fee_structure=fs, fee_head=exam, defaults={"amount":"150.00"})

        inv, _ = Invoice.objects.get_or_create(student=student, academic_year=ay, defaults={"issued_on":timezone.now().date(), "status":"UNPAID"})
        InvoiceItem.objects.get_or_create(invoice=inv, fee_head=tuition, defaults={"amount":"1200.00"})
        InvoiceItem.objects.get_or_create(invoice=inv, fee_head=exam, defaults={"amount":"150.00"})

        self.stdout.write(self.style.SUCCESS("Seed complete. Password for demo users: Passw0rd!"))
