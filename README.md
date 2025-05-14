# FastAPI Project Template
A production-ready FastAPI boilerplate featuring robust authentication with [FastAPI-Users](https://fastapi-users.github.io/fastapi-users/) and clean architecture using the [Unit of Work](https://en.wikipedia.org/wiki/Unit_of_work) pattern.

## Getting Started

### Quick Start with Docker
```bash
docker-compose up --build
```
The application will be available at [http://0.0.0.0:9999](http://0.0.0.0:9999)

### Manual Setup with Python

#### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Database Migrations
Using Alembic directly:
```bash
# Generate migration
alembic revision --autogenerate -m "Initial check"

# Apply migration
alembic upgrade head
```

Or using Make commands:
```bash
# Generate migration
make generate

# Apply migration
make migrate
```

#### 3. Run the Application
From the root directory:

**Development Mode**
```bash
fastapi dev src/main.py
```

**Production Mode**
```bash
fastapi run src/main.py
```

## Testing
Used [Pytest](https://pypi.org/project/pytest/) for testing.

Run tests from the root directory:
```bash
pytest -v tests/
```

## Features
- User authentication with FastAPI-Users
- SQLAlchemy with Unit of Work pattern
- Alembic migrations
- Docker support
- Comprehensive test coverage
- Ruff support
- Pre-commit hooks
- Makefile for common tasks
