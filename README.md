# Saeed English Language and Computer Academy
### Complete Professional Website & Online Admission Management System

> **Tagline:** Learn. Improve. Succeed.  
> **Campus Address:** Habib Rahman Market, Basement Floor, Mandi Bakakhel, Wazir, Pakistan  
> **Official WhatsApp:** 0331-9898199  
> **WhatsApp Direct:** [https://wa.me/923319898199](https://wa.me/923319898199)  
> **Founder & CEO:** Saeed Wazir  

---

## 1. Project Overview

This is a production-ready, full-stack educational web application and student management system built for **Saeed English Language and Computer Academy** (also known as Ahmad Saeed English Language and Computer Academy).

It combines:
1. **Public Institution Website:** 6 beautifully designed, mobile-responsive pages matching the academy's dark red (`#8B0000`) and gold (`#C9A84C`) identity with Google Fonts (`Playfair Display` and `DM Sans`).
2. **Authentic Photography:** Real institutional pictures featuring the official academy emblem, founder Saeed Wazir addressing the World Peace Summit, graduation ceremonies, Skill Development Council certification distributions, and classroom learning sessions.
3. **Interactive Online Admission System:** 6-section registration form with photograph upload, client/server validation, unique sequential application number generator (`SELCA-2026-XXXX`), dynamic course syllabus/fee preview, and an **Official Printable Student Admission Receipt**.
4. **Secure Admin Dashboard:** Protected portal with password hashing, overview statistics, student management (search, filter, status approval/rejection, record editing, and receipt printing), course management, and contact message management.
5. **Python Flask & SQL Backend:** Robust REST API, SQLAlchemy ORM database architecture, and cross-platform compatibility (SQLite for local development, PostgreSQL ready for production).

---

## 2. Technology Stack

- **Frontend:**
  - HTML5 & Responsive Semantic Markup
  - Modern CSS3 with CSS Variables, Flexbox, CSS Grid & `@media print`
  - JavaScript (ES6+ Fetch API, real-time validation, dynamic DOM rendering)
  - Google Fonts (`DM Sans` + `Playfair Display`)
  - Font Awesome 6.5.0 icons
- **Backend:**
  - Python 3.10+ / 3.14
  - Flask (REST API, Jinja2 Template Engine, Blueprints)
  - SQLAlchemy ORM & Flask-SQLAlchemy
  - Werkzeug (Secure Password Hashing & filename sanitization)
  - Pillow (Image handling & optimization)
- **Database:**
  - SQLite (`instance/academy.db`) for zero-configuration local development
  - PostgreSQL compatible via standard `DATABASE_URL` environment variable

---

## 3. Real Photos Integration

All institutional photographs provided by the academy are integrated into the application:

| Filename | Role in Application |
|---|---|
| `static/images/logo.png` | Official Academy Crest / Logo with graduation cap, globe, British flag, and laptop |
| `static/images/academy/ceo.jpg` | Official portrait of Saeed Wazir addressing the World Peace Summit |
| `static/images/academy/ceo_speech.jpg` | Saeed Wazir at World Peace Summit podium |
| `static/images/academy/poster_english.jpg` | Official Academy Flyer: *English with Saeed Wazir* |
| `static/images/academy/ceremony_group.jpg` | Annual Certificate Distribution Ceremony group photograph |
| `static/images/academy/ceremony_award1.jpg` | Skill Development Council (SDC) Certificate Awarding |
| `static/images/academy/ceremony_award2.jpg` | Faculty presenting student certificates |
| `static/images/academy/classroom_sitting.jpg` | Interactive classroom learning session |
| `static/images/academy/classroom_tutoring.jpg` | Sir Saeed Wazir conducting personalized student instruction |
| `static/images/academy/faculty1.jpg` | Faculty Member & IT Instructor (Ghufran Ullah) |

---

## 4. Project Directory Structure

```
Academy/
├── app.py                      # Flask Application factory & routing setup
├── config.py                   # Development & Production configuration
├── requirements.txt            # Python dependencies
├── .env.example                # Example environment variables
├── verify_system.py            # Comprehensive automated test suite
├── README.md                   # Complete documentation
│
├── models/                     # SQLAlchemy Database Models
│   ├── __init__.py             # Database extension initialization
│   ├── admin.py                # AdminUser model with password hashing
│   ├── student.py              # Admission model (24 schema columns)
│   ├── course.py               # Course model with fees, syllabus, images
│   └── contact.py              # ContactMessage model
│
├── routes/                     # Flask Blueprints & REST API endpoints
│   ├── __init__.py
│   ├── auth_helper.py          # Session authentication decorator (@admin_required)
│   ├── admissions.py           # Public submission & protected student management
│   ├── courses.py              # Public catalog & protected course CRUD
│   ├── contacts.py             # Public contact inquiry & protected message review
│   └── admin.py                # Admin dashboard, statistics, login/logout
│
├── templates/                  # Jinja2 HTML Templates
│   ├── index.html              # Home Page (Hero, Courses, Gallery, CEO spotlight)
│   ├── about.html              # About Page (History, Mission, Vision, Faculty)
│   ├── courses.html            # Courses Page (Dynamic cards, fees, full syllabi)
│   ├── ceo.html                # CEO Page (World Peace Summit portrait, vision)
│   ├── contact.html            # Contact Page (Address, Map, Working Form)
│   ├── admission.html          # Online Admission Registration & Printable Receipt
│   ├── 404.html                # Custom Not Found Error Page
│   ├── 500.html                # Custom Server Error Page
│   └── admin/
│       ├── login.html          # Secure Administrator Login
│       └── dashboard.html      # Full Administration Management Dashboard
│
├── static/                     # Static Assets
│   ├── css/
│   │   ├── style.css           # Institutional design, typography, print styles
│   │   └── admin.css           # Admin dashboard styling
│   ├── js/
│   │   ├── main.js             # Navigation, smooth scroll, loaders
│   │   ├── api.js              # Admission form, photo preview, receipt generator
│   │   └── admin.js            # Dashboard operations, search, modals, print actions
│   ├── images/
│   │   ├── logo.png            # Official institutional crest
│   │   ├── favicon.ico         # Academy browser tab icon
│   │   └── academy/            # 10 real institutional photographs
│   └── uploads/                # Directory for uploaded student photographs
│
└── instance/
    └── academy.db              # SQLite Database file (auto-generated)
```

---

## 5. Quick Installation & Running Locally

### Step 1: Open Terminal in Project Directory
```powershell
cd c:\Users\khan\Desktop\Academy
```

### Step 2: Create and Activate Virtual Environment (Recommended)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Run the Application
```powershell
python app.py
```

### Step 5: Open in Your Browser
- **Public Website:** [http://127.0.0.1:5000](http://127.0.0.1:5000)
- **Online Admission Page:** [http://127.0.0.1:5000/admission](http://127.0.0.1:5000/admission)
- **Admin Dashboard:** [http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin)

---

## 6. Default Admin Credentials

Upon initial launch, the system automatically initializes the database and seeds the default administrator account:

- **Login URL:** `/admin/login`
- **Username:** `admin`
- **Password:** `admin123`

*(You can securely update this password at any time directly from the **Academy Settings** tab inside the Admin Dashboard).*

---

## 7. Online Admission & Printable Receipt Workflow

1. **Step-by-Step Registration:**
   - **Section 1 (Student Info):** Full Name, Father's Name, DOB, Gender, CNIC/B-Form, and Student Photograph upload with live preview.
   - **Section 2 (Contact Info):** Phone Number, WhatsApp Number (with 1-click "Same as Mobile" checkbox), Email, Home Address, City, District.
   - **Section 3 (Educational Info):** Highest Qualification, College/School, Passing Year, and Computer Experience.
   - **Section 4 (Course Selection):** Dropdown linked dynamically to the database. Selecting a course displays its duration, fee, and syllabus highlights.
   - **Section 5 (Preferences):** Shift timing (Morning, Mid-day, Afternoon, Evening), admission date, special requirements, and required declaration checkbox.
2. **Receipt Generation:**
   - Submitting the form validates all fields and sends a `multipart/form-data` request to `POST /api/admissions`.
   - Generates a guaranteed-unique application number (e.g. `SELCA-2026-0001`).
   - Immediately renders the **Official Admission Registration Receipt** complete with the academy crest, applicant photo, fee details, security watermark, verification stamp, and signature lines.
   - Clicking **"Print Official Receipt"** triggers clean `@media print` formatting designed specifically for standard A4 paper or PDF export.
3. **Application Tracking:**
   - Any applicant can enter their Application Number on `/admission` to retrieve and re-print their receipt anytime.

---

## 8. REST API Reference

### Admissions
- `POST /api/admissions` — Submit new admission with optional photo upload.
- `GET /api/admissions` — Retrieve all admissions (*Admin session required*).
- `GET /api/admissions/<id>` — View single admission (*Admin session required*).
- `PUT /api/admissions/<id>` — Update status or student data (*Admin session required*).
- `DELETE /api/admissions/<id>` — Permanently delete record (*Admin session required*).
- `GET /api/admissions/receipt/<app_number>` — Public safe receipt lookup.

### Courses
- `GET /api/courses` — Public list of all available academy courses.
- `GET /api/courses/<id>` — Public course details by ID.
- `POST /api/courses` — Add new course (*Admin session required*).
- `PUT /api/courses/<id>` — Update course details & fees (*Admin session required*).
- `DELETE /api/courses/<id>` — Remove course (*Admin session required*).

### Contact Inquiries
- `POST /api/contact` — Public submission of visitor message.
- `GET /api/contacts` — Retrieve contact messages (*Admin session required*).
- `DELETE /api/contacts/<id>` — Delete message (*Admin session required*).

### Authentication & Dashboard
- `POST /api/admin/login` — Sign in and create secure session.
- `POST /api/admin/logout` — Destroy session.
- `GET /api/admin/check` — Check current authentication state.
- `GET /api/admin/dashboard` — Overview statistics (*Admin session required*).
- `POST /api/admin/change-password` — Update administrator password (*Admin session required*).

---

## 9. Automated Testing

Run the automated test suite to verify all endpoints, database models, and security checks:

```powershell
python verify_system.py
```

All 6 integration tests will execute and confirm:
1. All 7 page routes return HTTP 200.
2. The authentic CEO photograph is in place.
3. Seeded courses are loaded and accessible.
4. Admission submission, application number generator, and receipt rendering work.
5. Contact message saving works.
6. Admin authentication, authorization barriers (HTTP 401 on unauthorized calls), status updating, course CRUD, and logout work.

---

## 10. Production Deployment & GitHub Upload

### Push to GitHub
```bash
git init
git add .
git commit -m "Complete Saeed English Language and Computer Academy full-stack website"
git branch -M main
git remote add origin https://github.com/<your-username>/saeed-academy.git
git push -u origin main
```

### Production Environment Variables
On your production server (Linux VPS, Ubuntu, or cloud platforms like Render / Railway / PythonAnywhere):
```bash
export FLASK_ENV=production
export SECRET_KEY=your_very_long_secure_random_key_here
export DATABASE_URL=postgresql://user:password@host:5432/saeed_academy
```

### Running with Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app('production')"
```

---

## 11. Academy Contact & Campus Details

- **Campus Address:** Habib Rahman Market, Basement Floor, Mandi Bakakhel, Wazir, Pakistan
- **Phone / WhatsApp:** 0331-9898199
- **WhatsApp Web Link:** [https://wa.me/923319898199](https://wa.me/923319898199)
- **Class Shifts:** Morning (8am–10am), Mid-day (11am–1pm), Afternoon (2pm–4pm), Evening (4:30pm–6:30pm)
- **Certifications:** Recognized by Skill Development Council (SDC) Peshawar
