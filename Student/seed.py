import os
import sys
import django
import random
from faker import Faker

# -----------------------
# Add project root to Python path
# -----------------------
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# -----------------------
# Django setup
# -----------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Student_Management.settings")
django.setup()

# -----------------------
# Imports after Django setup
# -----------------------
from Student.models import Department, StudentID, Student, Subject, SubjectMarks

fake = Faker()

# -----------------------
# Helper function: generate unique student ID
# -----------------------
def generate_unique_student_id():
    while True:
        student_id_val = f"STD-{random.randint(1000, 9999)}"
        if not StudentID.objects.filter(student_id=student_id_val).exists():
            return StudentID.objects.create(student_id=student_id_val)

# -----------------------
# Seed Departments
# -----------------------
def seed_departments():
    dept_names = ["Computer Science", "Physics", "Mathematics", "Chemistry", "Biology", "English"]
    for name in dept_names:
        dept, created = Department.objects.get_or_create(department=name)
        if created:
            print(f"Created department: {name}")

# -----------------------
# Seed Subjects
# -----------------------
def seed_subjects():
    subject_names = ["Mathematics", "Physics", "Chemistry", "Biology", "English", "Computer Programming"]
    for name in subject_names:
        subj, created = Subject.objects.get_or_create(subject=name)
        if created:
            print(f"Created subject: {name}")

# -----------------------
# Seed Students
# -----------------------
def seed_students(n=10):
    departments = list(Department.objects.all())
    if not departments:
        print("No departments found! Run seed_departments() first.")
        return

    for _ in range(n):
        # Pick a random department
        department = random.choice(departments)

        # Create a unique student ID
        student_id_obj = generate_unique_student_id()

        # Create fake student data
        student_obj = Student.objects.create(
            department=department,
            student_name=fake.name(),
            student_age=random.randint(18, 25),
            student_email=fake.unique.email(),
            student_address=fake.address(),
            student_id=student_id_obj
        )
        print(f"Created student: {student_obj.student_name} ({student_id_obj.student_id})")

# -----------------------
# Seed Subject Marks
# -----------------------
def seed_subject_marks():
    students = list(Student.objects.all())
    subjects = list(Subject.objects.all())

    if not students or not subjects:
        print("No students or subjects found! Add them first.")
        return

    marks_to_create = []

    for stu in students:
        for sub in subjects:
            # Skip if mark already exists for this student+subject
            if SubjectMarks.objects.filter(student=stu, subject=sub).exists():
                continue

            marks_to_create.append(
                SubjectMarks(
                    student=stu,
                    subject=sub,
                    marks=random.randint(0, 100)
                )
            )

    if marks_to_create:
        SubjectMarks.objects.bulk_create(marks_to_create)
        print(f"Created marks for {len(marks_to_create)} student-subject entries")
    else:
        print("All marks already exist. Nothing to create.")


# -----------------------
# Run the seed script
# -----------------------
if __name__ == "__main__":
    print("Starting database seeding...\n")

    # 1️⃣ Departments
    seed_departments()

    # 2️⃣ Subjects
    seed_subjects()

    # 3️⃣ Students
    seed_students(n=45)  # Adjust number of students here

    # 4️⃣ Marks
    seed_subject_marks()

    print("\nSeeding complete!")
