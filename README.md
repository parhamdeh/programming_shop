# Django Programming Course Platform

A Django-based platform for programming video courses, where users purchase a subscription to gain access to watch the videos.

## ✨ Features

- 🔐 User authentication
- 📝 Course & video content management
- 💳 Subscription-based access — users must subscribe to watch videos
- 👤 User profiles with public/private visibility (`is_private`)
- 🔒 Access control on content based on subscription status
- ✅ Full test coverage with `pytest-django` and `factory_boy`

## 🏗 Architecture

The project follows a **Service Layer** architecture, separating concerns across distinct layers:

- **Selectors** — handle read/query logic
- **Services** — handle business logic and write operations
- **Models** — define the data structure
- **Views** — handle request/response and delegate to services/selectors

This separation keeps business logic decoupled from the views and database access, making the codebase easier to test and maintain.

## 🛠 Tech Stack

| Layer | Tool |
|---|---|
| Framework | Django 6.0.6 |
| Database | PostgreSQL |
| Testing | pytest, pytest-django, factory-boy, Faker |
| Language | Python 3.14+ |

## ⚙️ Prerequisites

- Python 3.14+
- PostgreSQL 16+
- pip / virtualenv

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/parhamdeh/programming_shop.git
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here

DB_ENGINE=django.db.backends.postgresql
DB_NAME=mydatabase
DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=localhost
DB_PORT=5432
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

The project will be available at `http://127.0.0.1:8000/`.

## 🧪 Running Tests

```bash
pytest
```

Run tests with coverage report:

```bash
pytest --cov=.
```

Run a specific test file:

```bash
pytest blog_version2/tests/test_selectors/test_posts_selectors.py
```