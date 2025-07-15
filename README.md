# 🚀 Auth Service - FastAPI Clean Architecture

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.31-red?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://sqlalchemy.org)
[![Alembic](https://img.shields.io/badge/Alembic-1.13.2-orange?style=for-the-badge)](https://alembic.sqlalchemy.org)

## 📋 Description
**Modern Authentication Service** built with FastAPI following clean architecture principles. This service provides robust JWT-based authentication with role-based access control, designed for scalability and maintainability.

<!-- ![openapi-docs](./doc/images/openapi-docs-v2.png) -->

## ✨ Key Features
- 🔐 **JWT Authentication** with refresh tokens
- 👥 **Role-based Access Control** 
- 🏗️ **Clean Architecture** with dependency injection
- 📊 **Database Migrations** with Alembic
- 🧪 **Comprehensive Testing** with pytest
- 🐳 **Docker Ready** for containerized deployment
- 📝 **Auto-generated OpenAPI** documentation

## 🏛️ Architecture Principles
- ✅ **Minimal functionality** - Keep it simple
- 🎯 **Convincing architecture** - Well-structured codebase
- 📖 **Easy to read** - Clean and maintainable code
- 🔄 **Compatibility** - Works across environments
- 🛠️ **Versatility** - Adaptable to various use cases

## 📊 Data Models
- 👤 **User** - Authentication and user management
- 📝 **Post** - Content management [user (1:n) post]
- 🏷️ **Tag** - Content categorization [post (n:n) tag]

## 🛠️ Tech Stack
| Category | Technology | Version |
|----------|------------|---------|
| **Language** | Python | 3.10+ |
| **Framework** | FastAPI | 0.111.0 |
| **Server** | Uvicorn | 0.30.1 |
| **Database** | PostgreSQL | - |
| **ORM** | SQLAlchemy | 2.0.31 |
| **Migration** | Alembic | 1.13.2 |
| **Validation** | Pydantic | 2.8.0 |
| **DI Container** | dependency-injector | 4.41.0 |
| **Authentication** | python-jose | 3.3.0 |
| **Password Hashing** | bcrypt | 4.1.3 |
| **Testing** | pytest | 8.2.2 |
| **Database Driver** | psycopg2 | 2.9.9 |

## 🎯 Core Features
### 🔐 Authentication & Security
- JWT token-based authentication
- Password hashing with bcrypt
- Refresh token mechanism
- Role-based access control

### 🗄️ Database
- **PostgreSQL** support with connection pooling
- **Alembic** migrations for schema management
- **SQLAlchemy 2.0** ORM with async support
- **Real database testing** with pytest
- **Flexible loading** strategies (eager, lazy)
- **Complex relationships** modeling (1:1, 1:n, n:n)

### 🏗️ Architecture
- **Service-Repository** pattern with dependency injection
- **Clean separation** of concerns
- **Testable** and **maintainable** codebase

### 🚀 Deployment
- **Container-ready** (Docker, Kubernetes)
- **Traditional WAS** deployment support
- **Environment-based** configuration

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL database
- Poetry (recommended) or pip

### 📦 Installation
```bash
# Clone the repository
git clone <repository-url>
cd auth-service

# Install dependencies with Poetry (recommended)
poetry install

# OR install with pip
pip install -r requirements.txt
```

### 🗄️ Database Setup
```bash
# 1. Create PostgreSQL database
createdb auth_service

# 2. Set up environment variables
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# 3. Run database migrations
alembic upgrade head
```

### 🚀 Starting the Server

#### Development Mode (Recommended for development)
```bash
# Using Poetry
poetry run uvicorn app.main:app --reload

# OR using pip/system Python
uvicorn app.main:app --reload
```

#### Production Mode
```bash
# Basic production server
uvicorn app.main:app --host 0.0.0.0 --port 4000

# Production with multiple workers
uvicorn app.main:app --host 0.0.0.0 --port 4000 --workers 4

# With Poetry
poetry run uvicorn app.main:app --host 0.0.0.0 --port 4000 --workers 4
```

#### Using Docker (Alternative)
```bash
# Build Docker image
docker build -t auth-service .

# Run container
docker run -p 4000:4000 auth-service
```

### 🌐 Accessing the Service

Once the server is running, you can access:

- **API Documentation (Swagger)**: http://localhost:4000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:4000/redoc
- **Health Check**: http://localhost:4000/health (if implemented)

### 🔧 Development Setup

```bash
# Install development dependencies
poetry install --with dev

# Run pre-commit hooks
pre-commit install

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html
```

## 📚 Commands Reference

### 🗄️ Database (Alembic)
```bash
# Apply all migrations
alembic upgrade head

# Rollback all migrations
alembic downgrade base

# Create new migration
alembic revision --autogenerate -m "revision_name"

# View migration history
alembic history
```

### 🔄 Migration Workflow
1. **Modify models** in `app/model/*.py`
2. **Generate migration**: `alembic -x ENV=[dev|stage|prod] revision --autogenerate -m "description"`
3. **Review** auto-generated migration in `migrations/versions/*.py`
4. **Apply migration**: `alembic -x ENV=[dev|stage|prod] upgrade head`

> 💡 **Note**: If ENV is not specified, it defaults to test environment

### 🖥️ Server
```bash
# Basic server
uvicorn app.main:app --reload

# Custom host and port
uvicorn app.main:app --host 0.0.0.0 --port 4000

# Production with workers
uvicorn app.main:app --workers 4
```

### 🧪 Testing
```bash
# Run all tests
pytest

# Run with coverage (terminal)
pytest --cov=app --cov-report=term-missing

# Run with coverage (HTML report)
pytest --cov=app --cov-report=html
```

## ⚙️ Environment Configuration

Create a `.env` file in the root directory:

```dotenv
# Environment
ENV=dev

# Database Configuration
DB=postgresql
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=auth_service

# Security
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Optional: Logging
LOG_LEVEL=INFO
```

## 🏗️ Project Structure
```
auth-service/
├── app/
│   ├── api/v1/           # API routes and endpoints
│   ├── core/             # Core configurations and utilities
│   ├── model/            # Database models
│   ├── repository/       # Data access layer
│   ├── schema/           # Pydantic schemas
│   ├── services/         # Business logic
│   └── util/             # Utility functions
├── migrations/           # Alembic migrations
├── tests/               # Test suite
├── alembic.ini         # Alembic configuration
├── pyproject.toml      # Poetry dependencies
└── README.md           # This file
```

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📚 References
- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [Alembic Official Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Dependency Injector](https://python-dependency-injector.ets-labs.org/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

---
<div align="center">
    <strong>Built with ❤️ using FastAPI and Clean Architecture principles</strong>
</div>
