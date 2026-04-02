from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Sum, Q

from .models import *


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Login Successful ✅")
            return redirect("report")
        else:
            messages.error(request, "Invalid credentials ❌")
            return redirect("login")

    return render(request, "student_html/login.html")


def logout_page(request):
    logout(request)
    return redirect("login")


def register_page(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match ❌")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists ❌")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=firstname,
            last_name=lastname
        )

        messages.success(request, "Registered Successfully ✅")
        return redirect("login")

    return render(request, "student_html/register.html")


def report_card(request):
    students = Student.objects.all()

    if request.GET.get('search'):
        search = request.GET.get('search')
        students = students.filter(
            Q(student_name__icontains=search) |
            Q(student_email__icontains=search) |
            Q(student_id__student_id__icontains=search) |
            Q(department__department__icontains=search)
        )

    paginator = Paginator(students, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "student_html/report_table.html", {"page_obj": page_obj})


def see_marks(request, student_id):
    marks = SubjectMarks.objects.filter(student__student_id__student_id=student_id)
    total = marks.aggregate(total=Sum('marks'))

    ranks = Student.objects.annotate(
        total_marks=Sum('marks__marks')
    ).order_by('-total_marks')

    rank_position = next(
        (index + 1 for index, s in enumerate(ranks) if s.student_id.student_id == student_id),
        None
    )

    return render(
        request,
        "student_html/see_marks.html",
        {
            "marks_each": marks,
            "totals": total,
            "rank": rank_position
        }
    )
