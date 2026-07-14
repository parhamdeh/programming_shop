# Programming Course Platform API

A Django REST Framework based platform for selling programming courses with a subscription system. Users can register, purchase subscriptions, and access premium course content through REST APIs.

---

# ✨ Features

- 🔐 JWT Authentication
- 👤 User Registration with OTP Verification
- 👥 User Management
- 📝 Programming Posts (CRUD)
- 📂 Categories (Tree Structure using django-mptt)
- 💬 Comments
- ❤️ Likes
- 💳 Subscription Plans
- 💰 Subscription Payment (ZarinPal Sandbox)
- 🔒 Premium Post Access Control
- 👤 Public / Private User Profiles
- 📖 Interactive Swagger Documentation
- ✅ Unit & API Tests

---

# 🏗 Architecture

The project follows the **Service Layer Architecture**.

```
Request
   │
   ▼
Views (APIView)
   │
   ├────────► Selectors (Read Operations)
   │
   └────────► Services (Business Logic)
                    │
                    ▼
                 Models
```

### Project Layers

- **Views** → Handle HTTP Requests & Responses
- **Selectors** → Database Read Operations
- **Services** → Business Logic
- **Models** → Database Models
- **Serializers** → Validation & Serialization

---

# 🛠 Tech Stack

| Layer | Technology |
|--------|------------|
| Framework | Django |
| API | Django REST Framework |
| Documentation | drf-spectacular (Swagger) |
| Database | PostgreSQL |
| Authentication | JWT (SimpleJWT) |
| Payment Gateway | ZarinPal Sandbox |
| Testing | pytest, pytest-django, factory-boy |
| Language | Python 3.14 |

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/parhamdeh/programming_shop.git

cd programming_shop
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / macOS

```bash
python -m venv venv

source venv/bin/activate
```

---

## Install Packages

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create `.env`

```env
DEBUG=True

SECRET_KEY=your-secret-key

DB_ENGINE=django.db.backends.postgresql

DB_NAME=programming_shop

DB_USER=postgres

DB_PASSWORD=password

DB_HOST=localhost

DB_PORT=5432

MERCHANT=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

---

## Migrate

```bash
python manage.py migrate
```

---

## Create Superuser

```bash
python manage.py createsuperuser
```

---

## Run Server

```bash
python manage.py runserver
```

---

# 📖 API Documentation

Swagger UI

```
/api/schema/swagger-ui/
```

OpenAPI Schema

```
/api/schema/
```

---

# 🔑 Authentication APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/jwt/login/` | Get Access & Refresh Token |
| POST | `/api/jwt/refresh/` | Refresh Access Token |
| POST | `/api/jwt/verify/` | Verify JWT Token |

---

# 👤 User APIs

| Method | Endpoint |
|---------|----------|
| GET | `/api/users/` |
| POST | `/api/users/` |
| GET | `/api/users/{id}/` |
| PUT | `/api/users/{id}/` |
| PATCH | `/api/users/{id}/` |
| DELETE | `/api/users/{id}/` |

---

# 📝 Registration

| Method | Endpoint |
|---------|----------|
| POST | `/api/register/` |
| POST | `/api/register/verify/` |

---

# 👤 Profile

| Method | Endpoint |
|---------|----------|
| GET | `/api/profile/{id}/` |

---

# 📚 Posts

| Method | Endpoint |
|---------|----------|
| GET | `/api/posts/` |
| POST | `/api/posts/` |
| GET | `/api/posts/{id}/` |
| PUT | `/api/posts/{id}/` |
| PATCH | `/api/posts/{id}/` |
| DELETE | `/api/posts/{id}/` |

---

# ❤️ Likes

| Method | Endpoint |
|---------|----------|
| GET | `/api/likes/{post_id}/` |
| POST | `/api/likes/{post_id}/` |

---

# 💬 Comments

| Method | Endpoint |
|---------|----------|
| GET | `/api/comments/{post_id}/` |
| POST | `/api/comments/{post_id}/` |

---

# 📂 Categories

| Method | Endpoint |
|---------|----------|
| GET | `/api/categories/` |
| POST | `/api/categories/` |
| GET | `/api/categories/{id}/` |
| PUT | `/api/categories/{id}/` |
| PATCH | `/api/categories/{id}/` |
| DELETE | `/api/categories/{id}/` |

---

# 💳 Subscription Plans

| Method | Endpoint |
|---------|----------|
| GET | `/api/subscriptions/` |
| POST | `/api/subscriptions/` |
| GET | `/api/subscriptions/{id}/` |
| PUT | `/api/subscriptions/{id}/` |
| PATCH | `/api/subscriptions/{id}/` |
| DELETE | `/api/subscriptions/{id}/` |

---

# 💰 Subscription Payment

| Method | Endpoint |
|---------|----------|
| POST | `/api/subscriptions/{id}/pay/` |
| GET | `/api/subscriptions/verify/` |

---

# 🏠 Home

| Method | Endpoint |
|---------|----------|
| GET | `/api/` |

Returns:

- Latest Posts
- Categories
- Subscription Plans

---

# 🔒 Permissions

| Resource | Permission |
|-----------|------------|
| Users | Authenticated |
| Posts | Admin CRUD / Public Read |
| Categories | Admin CRUD / Authenticated Read |
| Subscriptions | Admin CRUD / Authenticated Read |
| Premium Posts | Active Subscription Required |
| Payment | Authenticated Users |

---

# 🧪 Running Tests

Run all tests

```bash
pytest
```

Coverage

```bash
pytest --cov=.
```

Specific test

```bash
pytest path/to/test_file.py
```

---

# 📂 Project Structure

```
posts/
    selectors/
    services/
    models.py

users/
    selectors/
    services/

view_api/
    apps_api/
    permissions.py
    throttle.py

config/
```

---

# 📜 License

This project is intended for educational and portfolio purposes.