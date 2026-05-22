import os
import sys
import django
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EduTrack.settings")
django.setup()

from django.utils import timezone
from datetime import date, timedelta
from users.models import CustomUser
from students.models import Department, Student, Subject
from marks.models import Marks
from fees.models import Fee
from attendance.models import Session, Attendance

STUDENTS = [
    ("alice_j",    "Alice",    "Johnson",   "alice@sms.com",    "STD-1001"),
    ("bob_s",      "Bob",      "Smith",     "bob@sms.com",      "STD-1002"),
    ("carol_w",    "Carol",    "Williams",  "carol@sms.com",    "STD-1003"),
    ("david_b",    "David",    "Brown",     "david@sms.com",    "STD-1004"),
    ("emma_d",     "Emma",     "Davis",     "emma@sms.com",     "STD-1005"),
    ("frank_m",    "Frank",    "Miller",    "frank@sms.com",    "STD-1006"),
    ("grace_w",    "Grace",    "Wilson",    "grace@sms.com",    "STD-1007"),
    ("henry_m",    "Henry",    "Moore",     "henry@sms.com",    "STD-1008"),
    ("iris_t",     "Iris",     "Taylor",    "iris@sms.com",     "STD-1009"),
    ("jack_a",     "Jack",     "Anderson",  "jack@sms.com",     "STD-1010"),
]

ADDRESSES = [
    "12 Oak Street, Springfield",
    "45 Maple Ave, Shelbyville",
    "78 Pine Road, Capital City",
    "23 Elm Blvd, Ogdenville",
    "99 Cedar Lane, North Haverbrook",
]

PHONES = ["9876543210", "9123456780", "8765432109", "9988776655", "7654321098",
          "8899001122", "9001122334", "7788990011", "8877665544", "9900112233"]

depts = list(Department.objects.all())
subjects = list(Subject.objects.all())

created_students = []

for i, (username, first, last, email, sid) in enumerate(STUDENTS):
    # Create user
    user, _ = CustomUser.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'first_name': first,
            'last_name': last,
            'role': CustomUser.ROLE_STUDENT,
        }
    )
    if _:
        user.set_password('student123')
        user.save()

    # Create student profile
    student, created = Student.objects.get_or_create(
        student_id=sid,
        defaults={
            'user': user,
            'department': depts[i % len(depts)],
            'age': random.randint(18, 24),
            'address': ADDRESSES[i % len(ADDRESSES)],
            'phone': PHONES[i],
        }
    )
    created_students.append(student)
    print(f"{'Created' if created else 'Exists'}: {sid} - {first} {last}")

# Assign marks
for student in created_students:
    for subject in subjects:
        score = random.randint(45, 98)
        Marks.objects.get_or_create(
            student=student,
            subject=subject,
            defaults={'score': score, 'max_score': 100, 'exam_date': date(2026, 3, 15)}
        )

print(f"\nMarks assigned: {Marks.objects.count()}")

# Assign fees
fee_types = [
    ("Tuition Fee", 15000),
    ("Library Fee", 500),
    ("Lab Fee", 2000),
]
for student in created_students:
    for desc, amount in fee_types:
        paid = random.choice([0, amount // 2, amount])
        Fee.objects.get_or_create(
            student=student,
            description=desc,
            defaults={
                'amount': amount,
                'paid_amount': paid,
                'due_date': date(2026, 6, 30),
            }
        )

print(f"Fees assigned: {Fee.objects.count()}")

# Create attendance sessions and records
teacher = CustomUser.objects.filter(role='teacher').first()
today = date.today()

for subject in subjects[:3]:
    session, _ = Session.objects.get_or_create(
        subject=subject,
        date=today,
        defaults={
            'start_time': '09:00',
            'is_active': True,
            'qr_valid_until': timezone.now() + timedelta(hours=2),
            'created_by': teacher,
        }
    )
    for student in created_students:
        status = random.choice([
            Attendance.STATUS_PRESENT,
            Attendance.STATUS_PRESENT,
            Attendance.STATUS_PRESENT,
            Attendance.STATUS_ABSENT,
            Attendance.STATUS_LATE,
        ])
        Attendance.objects.get_or_create(
            session=session,
            student=student,
            defaults={'status': status, 'method': Attendance.METHOD_MANUAL}
        )

print(f"Attendance records: {Attendance.objects.count()}")
print("\nAll done! Login with any student: username / student123")
print("Teacher login: teacher / teacher123")
