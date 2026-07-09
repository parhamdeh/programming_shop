# Django programming 

A Django-based blog backend featuring post management, public/private user profiles, and a subscription (follow) system between users.

## ✨ Features

- 🔐 User authentication (Auth API)
- 📝 Post management (create, view, edit)
- 👤 User profiles with public/private visibility (`is_private`)
- 🔔 Subscription system — follow other users
- 🔒 Access control on posts based on ownership and subscription status
- ✅ Full test coverage with `pytest-django` and `factory_boy`

## 🛠 Tech Stack

| Layer | Tool |
|---|---|
| Framework | Django 6.0.6 |
| Database | PostgreSQL |
| Testing | pytest, pytest-django, factory-boy, Faker |
| Language | Python 3.14+ |

## 📁 Project Structure

```
blog_with_Django/
├── config/
│   └── django/
│       ├── base.py
│       ├── local.py
│       └── production.py
├── blog_version2/
│   ├── home/
│   │   └── selectors/
│   │       └── posts.py
│   ├── users/
│   │   └── models.py
│   └── tests/
│       ├── apis/
│       ├── test_selectors/
│       └── test_services/
├── conftest.py
├── pytest.ini
├── requirements.txt
└── manage.py
```

> The structure above is based on the paths observed in the project — adjust as needed.

## ⚙️ Prerequisites

- Python 3.14+
- PostgreSQL 16+
- pip / virtualenv

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/blog-with-django.git
cd blog-with-django
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

## 📡 API Documentation

> List the main API endpoints here, for example:

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/register/` | Register a new user |
| `POST` | `/api/auth/login/` | Log in and receive a token |
| `GET` | `/api/posts/` | List posts |
| `GET` | `/api/posts/<slug>/` | Retrieve post details |
| `POST` | `/api/subscriptions/` | Subscribe/follow a user |

## 🤝 Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 📬 Contact

For questions or suggestions, please open an issue in this repository.