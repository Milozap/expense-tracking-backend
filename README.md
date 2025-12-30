# Expense Tracking API

Django REST Framework backend for tracking personal expenses and income.

## Features

- **User Registration & Authentication** - JWT-based auth with token rotation and blacklisting
- **Transaction Management** - Track income and expenses with categorization
- **Categories** - Organize transactions by customizable categories
- **Budgets** - Set and monitor spending limits
- **Reports** - Generate expense reports and analytics
- **Audit Logging** - Track changes for compliance

## Tech Stack

- **Framework**: Django 5.x + Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (Simple JWT)
- **API Documentation**: drf-spectacular (OpenAPI/Swagger)
- **Testing**: pytest + pytest-django
- **Code Quality**: black, isort, flake8, mypy

## Quick Start

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
- Make (optional, for convenience commands)

### Setup

1. **Clone and navigate to project**
   ```bash
   cd expense_tracking_backend
   ```

2. **Create environment file**
   ```bash
   cp .env.dev.example .env.dev
   ```

3. **Start with Docker**
   ```bash
   make up-dev
   # Or: docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
   ```

4. **Run migrations**
   ```bash
   make migrate
   # Or: docker compose exec expense_web python manage.py migrate
   ```

5. **Seed categories (optional)**
   ```bash
   make seed-categories
   ```

The API will be available at `http://localhost:8000`

## API Documentation

- **Swagger UI**: http://localhost:8000/api/docs/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## Development

### Running Tests
```bash
make test                    # Run all tests with coverage
pytest apps/users/tests/ -v  # Run specific app tests
```

### Code Quality
```bash
make lint        # Check code style
make format      # Auto-format code
make typecheck   # Run mypy type checking
make precommit   # Run all pre-commit hooks
```

### Docker Commands
```bash
make up-dev      # Start development environment
make down        # Stop and remove containers
make logs        # View application logs
make shell       # Open Django shell
```

See `Makefile` for all available commands.

## Authentication

### Register a new user
```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!"
  }'
```

Response includes `access` and `refresh` JWT tokens.

### Using the API
Include the access token in requests:
```bash
curl http://localhost:8000/api/v1/transactions/ \
  -H "Authorization: Bearer <access_token>"
```

### Token Refresh
```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<refresh_token>"}'
```

**Token Lifetimes:**
- Access: 15 minutes
- Refresh: 7 days

## Project Structure

```
apps/
├── api/v1/          # API versioning and routing
├── users/           # User management and authentication
├── categories/      # Transaction categories
├── transactions/    # Income/expense tracking
├── budgets/         # Budget management
├── reports/         # Reporting and analytics
├── audit/           # Audit logging
└── common/          # Shared utilities

expense_tracking/    # Django project settings
```

## Contributing

This project follows Test-Driven Development (TDD).

### Workflow
1. Write tests first
2. Implement feature
3. Run tests: `make test`
4. Check code quality: `make lint typecheck`
5. Format code: `make format`

