# 🌟 SocialApp - Django Social Media & Feed Application

A complete, modern, and production-ready **Django monolithic web application** for a social media feed where users can share moments, upload photos, manage personalized profiles, and interact in a responsive community feed.

Built using **Django**, **MySQL**, **Pillow**, **Bootstrap 5**, and custom modern CSS design with smooth micro-interactions.

---

## 📸 Key Features

* 🔐 **Full Authentication**: User registration with instant sign-in, login, secure session management, and logout.
* 🖼️ **Image & Media Handling**: Upload, validate (formats & size up to 10MB), and serve post images and profile avatars using Django's media storage and Pillow.
* 📝 **Full Post CRUD**:
  * **Create**: Post text-only updates, image-only posts, or rich text + photo posts with live client-side preview.
  * **Read**: Chronological community feed (`created_at DESC`), individual post view, and user timeline.
  * **Update**: Edit post text or replace/remove images (restricted strictly to the post owner).
  * **Delete**: Delete posts with safety confirmation modals (restricted strictly to the post owner).
* 👤 **User Profiles**:
  * Customizable biography, member since date, post counts, and avatar upload.
  * Public profile browsing for any creator.
  * Secure profile editing (first name, last name, email, bio, profile photo).
* 🛡️ **Security & Authorization**:
  * CSRF protection across all forms.
  * Password hashing via Django Auth framework.
  * Strict permission enforcement (403 Forbidden on unauthorized edit/delete attempts).
* 🎨 **UI/UX Design**:
  * Responsive layout (Mobile, Tablet, Desktop).
  * Toast alerts for real-time user feedback.
  * Polished card styling with Plus Jakarta Sans typography and subtle shadows.
  * Custom 404, 403, and 500 error pages.

---

## 🛠️ Technology Stack

* **Backend**: Python 3.12, Django 5.1 (LTS)
* **Database**: MySQL (via `mysqlclient` & `pymysql` fallback)
* **Image Processing**: Pillow
* **Configuration**: `python-dotenv`
* **Frontend**: HTML5, CSS3, JavaScript (Vanilla ES6), Bootstrap 5.3, Bootstrap Icons, Google Fonts

---

## 🚀 Getting Started

Follow these step-by-step instructions to run the application locally on Windows.

### 1. Prerequisites

Make sure the following are installed:
* [Python 3.10+](https://www.python.org/downloads/)
* [MySQL Server 8.0+](https://dev.mysql.com/downloads/mysql/)

---

### 2. Clone or Navigate to Project Directory

```powershell
cd c:\Users\gutti\Desktop\Django-feed
```

---

### 3. Create & Activate Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Or in Windows Command Prompt (cmd.exe)
venv\Scripts\activate.bat
```

---

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

### 5. Setup MySQL Database

Open your MySQL command line client or workbench and create the database:

```sql
CREATE DATABASE IF NOT EXISTS social_posts CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

### 6. Configure Environment Variables (`.env`)

Copy `.env.example` to `.env` or edit the existing `.env` file:

```env
DB_NAME=social_posts
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=your_django_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

> **Note**: Replace `your_mysql_password` with your actual MySQL root password.

---

### 7. Run Database Migrations

Apply database migrations to create all required tables:

```powershell
python manage.py makemigrations
python manage.py migrate
```

---

### 8. Create a Superuser (Admin)

Create an administrator account to access the Django Admin panel:

```powershell
python manage.py createsuperuser
```

Follow the interactive prompts to set a username, email, and password.

---

### 9. Run the Development Server

Start the local Django server:

```powershell
python manage.py runserver
```

---

### 10. Open in Browser

---

## 🐳 Running with Docker (Two Containers: Django + MySQL)

You can run the entire stack inside isolated Docker containers using **Docker Compose**.

### 1. Make sure Docker Desktop is running

Download and install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/) if you haven't already.

### 2. Build and Start the Containers

From the project root, run:

```bash
docker compose up --build
```

This single command will:
1. Spin up the **MySQL 8.0** container (`social_db`) with database health checks and a persistent data volume.
2. Build the **Django** container (`social_web`), install dependencies, wait for MySQL to be ready, automatically run database migrations, and seed initial demo accounts.
3. Bind the application to port `8000`.

### 3. Open in Browser

* **Application**: [http://localhost:8000/](http://localhost:8000/)
* **Admin Dashboard**: [http://localhost:8000/admin/](http://localhost:8000/admin/)

### 4. Useful Docker Commands

```bash
# Run in background (detached mode)
docker compose up -d

# Stop all containers
docker compose down

# Stop and wipe database volume (fresh start)
docker compose down -v

# View real-time container logs
docker compose logs -f web

# Execute commands inside the Django container (e.g. create superuser or run tests)
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py test
```

## 🧪 Running Tests

Execute the automated test suite covering authentication, permissions, CRUD, and validations:

```powershell
python manage.py test
```

All 19+ tests will run and pass cleanly.

---

## 📁 Project Structure

```text
Django-feed/
│
├── manage.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── social_app/                 # Core Project Configuration
│   ├── __init__.py             # PyMySQL / MySQLdb compatibility
│   ├── settings.py             # App settings, DB config & environment setup
│   ├── urls.py                 # URL routing & media serving
│   ├── views.py                # Custom 404, 403, 500 error handlers
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                   # User Authentication & Profiles
│   ├── models.py               # Profile model with avatar & bio
│   ├── views.py                # Register, Login, Logout, Profile View & Edit
│   ├── forms.py                # User & Profile ModelForms with validation
│   ├── urls.py                 # Accounts routing
│   ├── signals.py              # Automatic Profile creation on User signup
│   ├── admin.py                # Inline Profile admin integration
│   └── tests.py                # Auth & profile test cases
│
├── posts/                      # Feed & Posts Management
│   ├── models.py               # Post model (content, image, timestamps)
│   ├── views.py                # Feed, Create, Detail, Edit, Delete views
│   ├── forms.py                # Post form with image upload & file validation
│   ├── urls.py                 # Posts routing
│   ├── admin.py                # Admin with image thumbnails & previews
│   └── tests.py                # CRUD & authorization test cases
│
├── templates/                  # HTML Templates
│   ├── base.html               # Shared navbar, toasts, and footer layout
│   ├── home.html               # Public landing page with hero & previews
│   ├── accounts/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── profile.html
│   │   └── profile_edit.html
│   ├── posts/
│   │   ├── feed.html
│   │   ├── post_create.html
│   │   ├── post_edit.html
│   │   ├── post_detail.html
│   │   └── post_confirm_delete.html
│   └── errors/
│       ├── 404.html
│       ├── 403.html
│       └── 500.html
│
├── static/                     # Static Assets
│   ├── css/
│   │   └── custom.css          # Design system, cards, gradients & layout
│   ├── js/
│   │   └── main.js             # Image previews, toasts & clipboard helpers
│   └── images/
│       └── default-avatar.svg  # Vector default user avatar
│
└── media/                      # Uploaded User Files (Ignored in Git)
    ├── posts/
    └── profile_pictures/
```

---

## 🔒 Security Best Practices Implemented

1. **Database Secrets Isolation**: Credentials are exclusively read from `.env` via `python-dotenv`.
2. **CSRF Protection**: Enabled on all POST forms.
3. **Password Security**: Standard Django PBKDF2 with SHA-256 password hashing.
4. **Access Control**: `@login_required` on all modification endpoints; ownership checks raise `PermissionDenied` (HTTP 403) if users attempt to alter others' posts.
5. **File Validation**: Image upload types and size limits are verified on both client and server sides.

---

## 🚀 CI/CD Pipeline (GitHub Actions to Docker Hub)

This repository includes an automated CI/CD pipeline (`.github/workflows/docker-build-push.yml`) that builds the Docker image on GitHub runners and pushes it directly to Docker Hub.

### 🔑 1. Configure GitHub Repository Secrets

In your GitHub repository:
1. Navigate to **Settings** > **Secrets and variables** > **Actions**.
2. Click **New repository secret** and add:
   * `DOCKERHUB_USERNAME`: Your Docker Hub username (e.g. `sumanth4518`).
   * `DOCKERHUB_TOKEN`: Your Docker Hub Personal Access Token (created at [hub.docker.com/settings/security](https://hub.docker.com/settings/security)).

### 🔘 2. How to Trigger the Build (Manual "Run workflow" Button)

Whenever you push or update your code:
1. Go to the **Actions** tab on your GitHub repository.
2. Select **"Build and Push Docker Image to Docker Hub"** from the left sidebar.
3. Click the **"Run workflow"** button on the right.
4. *(Optional)* Provide a custom tag or use the default `django-feed` image name.
5. Click the green **Run workflow** button.

### 🏷️ 3. The Two Tags Generated Per Build

The workflow publishes **exactly 2 tags** for each build:
1. **Commit SHA**: `sha-<short-sha>` (e.g. `sha-a1b2c3d` — permanently tied to the exact Git commit).
2. **Your Custom Tag Text**: The text entered in the workflow popup (defaults to `latest`, or custom values like `v1.0.0`, `prod`, `dev`).

### 📥 4. Pulling the Image from Docker Hub

```bash
# Pull by the unique commit hash tag:
docker pull <your-dockerhub-username>/django-feed:sha-<short-sha>

# Pull by the custom tag text you entered (e.g. latest, v1.0.0):
docker pull <your-dockerhub-username>/django-feed:<custom-tag-text>
```

