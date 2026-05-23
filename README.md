# 🎓 EduTrack — School Management System

![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.16-red?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)

A full-featured, role-based School Management System built with **Django**, **Django REST Framework**, **HTML/CSS**, and **Python**. Supports Admin, Teacher, and Student roles with QR-based attendance, marks management, fee tracking, and REST APIs.

---

## 📸 Screenshots

### 🔐 Login Page
<img width="1918" height="1074" alt="admin_page" src="https://github.com/user-attachments/assets/df566841-912a-4873-bdd5-19a8d1db2a62" />


### 👑 Admin Dashboard
![Admin Dashboard](https://via.placeholder.com/900x450?text=Admin+Dashboard)

### 👨‍🏫 Teacher Dashboard
![Teacher Dashboard](https://via.placeholder.com/900x450?text=Teacher+Dashboard)

### 👨‍🎓 Student Dashboard
![Student Dashboard](https://via.placeholder.com/900x450?text=Student+Dashboard)

### 📝 Marks Management
![Marks](https://via.placeholder.com/900x450?text=Marks+Management)

### 📅 Attendance with QR Code
![Attendance](https://via.placeholder.com/900x450?text=Attendance+QR+Code)

### 💳 Fees Management
![Fees](https://via.placeholder.com/900x450?text=Fees+Management)

> 💡 Replace placeholder images with real screenshots by adding images to a `/screenshots` folder and updating the paths above.

---

## ✨ Features

### 👑 Admin
- Full control over the entire system
- Add and manage teachers with subject assignments
- View all students, marks, fees, and attendance
- Live dashboard stats (students, teachers, fees, attendance)

### 👨‍🏫 Teacher
- Subject-specific access (only sees their assigned subjects)
- Assign and update student marks
- Create attendance sessions with auto-generated QR codes
- View fee status of all students

### 👨‍🎓 Student
- View personal profile
- View marks with grades and percentage
- View fee payment status
- Mark attendance by scanning QR code

---

## 🏗️ Project Structure

```
EduTrack/
│
├── EduTrack/                   # Project settings & root URLs
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── users/                      # Authentication & role management
│   ├── models.py               # CustomUser (admin/teacher/student)
│   ├── views.py                # Login, logout, dashboard routing
│   ├── serializers.py          # JWT token serializer
│   └── permissions.py          # IsAdmin, IsTeacher, IsStudent
│
├── students/                   # Student & Teacher profiles
│   ├── models.py               # Student, TeacherProfile, Department, Subject
│   ├── views.py                # Student list, teacher management
│   └── serializers.py
│
├── marks/                      # Marks management
│   ├── models.py               # Marks with grade/percentage
│   ├── views.py                # Teacher filtered by subject
│   └── serializers.py
│
├── fees/                       # Fee tracking
│   ├── models.py               # Fee with paid/unpaid/partial status
│   ├── views.py                # Stats, search, filter
│   └── serializers.py
│
├── attendance/                 # Attendance system
│   ├── models.py               # Session, Attendance
│   ├── views.py                # QR generation, manual marking
│   └── serializers.py
│
├── templates/                  # HTML templates
│   ├── base.html
│   ├── auth/
│   ├── admin/
│   ├── teacher/
│   └── student/
│
├── static/css/                 # Stylesheets
├── seed_students.py            # Sample data seeder
├── requirements.txt
└── .env.example
```

---

## 🔐 User Roles & Credentials

| Role    | Username   | Password     | Access Level              |
|---------|------------|--------------|---------------------------|
| Admin   | `teacher`  | `teacher123` | Full system access        |
| Teacher | `mr_math`  | `teacher123` | Mathematics & Algorithms  |
| Teacher | `ms_sci`   | `teacher123` | Physics & Chemistry       |
| Teacher | `mr_eng`   | `teacher123` | English & Data Structures |
| Student | `alice_j`  | `student123` | Own data only             |
| Student | `bob_s`    | `student123` | Own data only             |
| Student | `carol_w`  | `student123` | Own data only             |

> ⚠️ Change all passwords before deploying to production.

---

## 🗄️ Database Models

```
CustomUser          → role: admin / teacher / student
    │
    ├── TeacherProfile  → subjects (M2M), department, phone
    └── Student         → student_id, department, age, phone, address
            │
            ├── Marks       → subject, score, max_score, grade, percentage
            ├── Fee         → amount, paid_amount, status, due_date
            └── Attendance  → session, status (present/absent/late), method (manual/QR)
                    │
                    └── Session → subject, date, qr_token, qr_valid_until
```

---

## 🌐 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/api/token/` | Get JWT access & refresh token |
| POST | `/auth/api/token/refresh/` | Refresh access token |
| POST | `/auth/api/register/` | Register new user |
| GET  | `/auth/api/me/` | Get current user info |

### Students
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/students/api/students/` | List / create students |
| GET/PUT/DELETE | `/students/api/students/{id}/` | Retrieve / update / delete |
| GET/POST | `/students/api/departments/` | Departments |
| GET/POST | `/students/api/subjects/` | Subjects |

### Marks
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/marks/api/` | List / assign marks |
| GET/PUT/DELETE | `/marks/api/{id}/` | Update marks |

### Fees
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/fees/api/` | List / create fee records |
| GET/PUT/DELETE | `/fees/api/{id}/` | Update fee record |

### Attendance
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/attendance/api/sessions/` | List / create sessions |
| GET | `/attendance/api/sessions/{id}/qr_image/` | Get QR code image |
| GET/POST | `/attendance/api/records/` | Attendance records |
| POST | `/attendance/api/qr-scan/` | Student scans QR to mark attendance |

> All endpoints require `Authorization: Bearer <token>` header except login/register.

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/monikanimmana/EduTrack.git
cd EduTrack
```

### 2. Create and activate virtual environment
```bash
python -m venv env

# Windows
env\Scripts\activate

# Mac/Linux
source env/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file
```bash
cp .env.example .env
```
Edit `.env` and set your secret key:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Seed sample data
```bash
python seed_students.py
```

### 7. Run the server
```bash
python manage.py runserver
```

### 8. Open in browser
```
http://127.0.0.1:8000/
```

---

## 📦 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 6.0, Python 3.12 |
| REST API | Django REST Framework 3.16 |
| Authentication | JWT (djangorestframework-simplejwt) |
| Database | SQLite (dev), PostgreSQL ready |
| Frontend | HTML5, CSS3, Vanilla JS |
| QR Code | qrcode + Pillow |
| Filtering | django-filter |
| Reports | ReportLab (PDF ready) |

---

## 🔒 Security

- JWT token-based authentication
- Role-based access control (Admin / Teacher / Student)
- Teachers can only access their assigned subjects
- Students can only view their own data
- `.env` file excluded from version control
- CSRF protection on all forms

---

## 🚀 Scalability

- Modular app structure (easy to add new features)
- DRF ViewSets with pagination, filtering, search, ordering
- Ready to switch from SQLite to PostgreSQL (change `DATABASES` in settings)
- Environment variables via `.env` for easy deployment

---

## 📄 License

This project is for educational purposes.

---

## 👩‍💻 Author

**Monika Nimmana**  
GitHub: [@monikanimmana](https://github.com/monikanimmana)
