# URL Shortener Project   https://url-shortner-i5rk.onrender.com


## Project Overview
The **URL Shortener** is a web application built using **Django** that allows users to easily shorten long URLs, track usage statistics, and manage their links. It provides a modern dashboard with analytics and supports QR code generation for quick access.

---

## Core Features

### User Management
- Secure user registration and login system.
- Password validation and confirmation.
- Only authenticated users can create, edit, or delete URLs.

### URL Shortening
- Generate unique short URLs automatically or manually.
- Set optional expiration dates for short URLs.
- Track total clicks for each URL.
- Identify active and expired URLs.

### Dashboard & Analytics
- View all URLs in a personalized dashboard.
- Get quick statistics:
  - Total URLs created
  - Total clicks across all URLs
  - Number of active URLs
  - Number of expired URLs
- QR code generation for short URLs.

### Services Layer
- **UserWriteService** → Handles creating and updating user accounts.
- **UrlService** → Handles read-only operations on URLs (e.g., fetching original URLs, checking expiration).
- **UrlWriteService** → Handles creating, updating, deleting, and click tracking of URLs.
- **AnalyticsService** → Provides aggregated statistics for dashboards.

### Validation & Security
- Form-level validation for URLs, short codes, and expiration dates.
- Only the owner of a URL can edit or delete it.
- Passwords are securely hashed using Django’s built-in authentication system.

### Testing
- Comprehensive **Pytest** coverage for forms, services, and views.
- Includes tests for creating, editing, deleting URLs, and analytics calculations.

---

## Technology Stack
- **Backend:** Django, Python 3.13  
- **Database:** SQLite (easy to set up, no external server required)  
- **Frontend:** Django templates with Bootstrap for responsive design  
- **Testing:** Pytest  

---

## Goals
- Build a functional, secure URL shortener within a short timeframe.
- Provide meaningful analytics and easy management for users.
- Ensure clean, modular code using services for business logic.
- Make the project easy for recruiters to run locally without extra setup.

```
url_shortener_project/
│
├── accounts/
│ ├── forms.py
│ ├── views.py
│ ├── Services/
│ │ └── user_services.py
│ └── templates/accounts/
│
├── shortner/
│ ├── forms.py
│ ├── models.py
│ ├── views.py
| |--- context_processors.py 
│ ├── Services/
│ │ ├── url_shortner.py
│ │ └── analytics_service.py
│ ├── templates/shortner/
│ └── tests/
│ ├── test_forms.py
│ ├── test_services.py
│ └── test_views.py
│
├── myapp/
│ └── templates/myapp/
│
├── static/
├── templates/
├── manage.py
├── requirements.txt
├── db.sqlite3
└── README.md
  ```
## Installation (Windows)

```powershell
# Clone the repository
git clone https://github.com/Mahasethmanish987/url_shortner.git
cd url_shortner

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Create a superuser (optional)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run the development server
python manage.py runserver




