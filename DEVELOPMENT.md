# Development Guide

This guide outlines the structure and provides instructions for developing the Customer Support Email Agent.

## Project Architecture

### Directory Structure

```
src/
├── api/                 # FastAPI routes and endpoints
│   ├── __init__.py
│   ├── app.py          # FastAPI application factory
│   └── routes/         # Route modules (TODO)
│       ├── __init__.py
│       ├── health.py   # Health check endpoints
│       ├── emails.py   # Email endpoints
│       └── graph.py    # Graph execution endpoints
│
├── graph/              # LangGraph workflow
│   ├── __init__.py
│   └── workflow.py     # Main graph definition (TODO)
│
├── nodes/              # Individual graph nodes
│   ├── __init__.py
│   ├── retrieval.py    # Email retrieval node
│   ├── classification.py  # Email classification node
│   ├── analysis.py     # Context analysis node
│   ├── response_gen.py # Response generation node
│   └── sending.py      # Response sending node
│
├── services/           # Business logic services
│   ├── __init__.py
│   ├── email_service.py    # Email operations
│   ├── llm_service.py      # LLM interactions
│   ├── db_service.py       # Database operations
│   └── vector_service.py   # Vector store operations
│
├── prompts/            # LLM prompt templates
│   ├── __init__.py
│   └── templates.py    # Prompt definitions
│
├── schemas/            # Pydantic models
│   ├── __init__.py
│   ├── email.py       # Email domain schemas
│   └── graph.py       # Graph state schemas
│
├── core/              # Core configuration
│   ├── __init__.py
│   ├── config.py      # Settings management
│   └── logging.py     # Logging configuration
│
└── utils/             # Utilities and helpers
    ├── __init__.py
    └── helpers.py     # Helper functions
```

## Development Phases

### Phase 1: Core Services (Current)
**Status**: ✅ Scaffold Complete

Completed:
- [x] Project structure
- [x] requirements.txt
- [x] .env template
- [x] Configuration system (Pydantic settings)
- [x] Logging setup (Loguru)
- [x] FastAPI application factory
- [x] Pydantic schemas
- [x] Test infrastructure

### Phase 2: Services Implementation
**Status**: ⏳ Next

Tasks:
- [ ] **EmailService** (`src/services/email_service.py`)
  - IMAP email fetching
  - Email parsing
  - SMTP sending
  - Error handling and retry logic

- [ ] **LLMService** (`src/services/llm_service.py`)
  - OpenAI API integration
  - Prompt formatting
  - Response parsing
  - Token management

- [ ] **DatabaseService** (`src/services/db_service.py`)
  - SQLAlchemy models
  - Database operations
  - Migrations

### Phase 3: LangGraph Workflow
**Status**: ⏳ Next

Tasks:
- [ ] **Graph Definition** (`src/graph/workflow.py`)
  - Define graph structure
  - State management
  - Edge conditions

- [ ] **Node Implementations** (`src/nodes/`)
  - Email retrieval node
  - Classification node
  - Analysis node
  - Response generation node
  - Sending node

### Phase 4: API Routes
**Status**: ⏳ Next

Tasks:
- [ ] **Health Routes** (`src/api/routes/health.py`)
  - Health check endpoint
  - Status endpoint

- [ ] **Email Routes** (`src/api/routes/emails.py`)
  - GET /emails - List emails
  - POST /emails/process - Process emails
  - GET /emails/{id} - Get email details

- [ ] **Graph Routes** (`src/api/routes/graph.py`)
  - POST /graph/trigger - Manual trigger
  - GET /graph/status - Check status

### Phase 5: Advanced Features
**Status**: ⏳ Later

Tasks:
- [ ] Vector store integration
- [ ] Customer history context
- [ ] Email scheduling
- [ ] Analytics and monitoring
- [ ] Multi-language support

## Key Implementation Patterns

### Service Layer Pattern

Services encapsulate business logic:

```python
from abc import ABC, abstractmethod
from loguru import logger

class BaseService(ABC):
    """Base service class."""

    @abstractmethod
    async def initialize(self):
        """Initialize service resources."""
        pass

    @abstractmethod
    async def cleanup(self):
        """Cleanup service resources."""
        pass


class EmailService(BaseService):
    """Email handling service."""

    def __init__(self, config):
        self.config = config

    async def initialize(self):
        """Connect to email servers."""
        logger.info("Initializing email service")
        # Implementation

    async def fetch_emails(self, limit: int = 10):
        """Fetch unread emails."""
        # Implementation
        pass
```

### Node Pattern with LangGraph

Nodes process state:

```python
from src.schemas.graph import GraphState

async def email_retrieval_node(state: GraphState) -> dict:
    """Retrieve and parse email."""
    logger.info(f"Processing email from {state.sender}")

    # Process state
    try:
        # Do work
        return {
            "status": "processed",
            "classification": "product_inquiry",
        }
    except Exception as e:
        logger.error(f"Error in node: {e}")
        return {"error_message": str(e)}
```

### Error Handling

Always use try-except with proper logging:

```python
try:
    result = await some_operation()
except SpecificException as e:
    logger.error(f"Specific error: {e}", exc_info=True)
    raise
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    raise
```

## Testing Strategy

### Test Structure

```
tests/
├── conftest.py              # Pytest configuration
├── test_health.py          # Endpoint tests
├── unit/
│   ├── test_services.py    # Service tests
│   └── test_nodes.py       # Node tests
├── integration/
│   ├── test_graph.py       # Graph workflow tests
│   └── test_email_flow.py  # End-to-end tests
└── fixtures/
    └── sample_emails.py    # Test data
```

### Running Tests

```bash
# All tests
pytest

# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# Specific test file
pytest tests/unit/test_services.py -v

# With coverage
pytest --cov=src tests/
```

## Code Quality

### Formatting

```bash
# Format code
black src/ tests/

# Check formatting
black --check src/ tests/
```

### Linting

```bash
# Check code with ruff
ruff check src/ tests/

# Fix issues
ruff check --fix src/ tests/
```

### Type Checking

```bash
mypy src/
```

## Environment Setup

### First Time Setup

```bash
# Create virtual environment
python -m venv venv

# Activate (on Windows)
venv\Scripts\activate

# Or on Unix/macOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure .env
cp .env .env.local
# Edit .env.local with your settings
```

### Running the Application

```bash
# With auto-reload
python main.py

# Or directly with uvicorn
uvicorn src.api.app:app --reload
```

## Database Setup

### Initial Migration

```bash
# Generate migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

### Database URL Examples

SQLite:
```
sqlite:///./customer_support.db
```

PostgreSQL:
```
postgresql://user:password@localhost:5432/customer_support_db
```

## Debugging Tips

1. **Enable Debug Logging**
   ```python
   # In .env
   LOG_LEVEL=DEBUG
   DEBUG=True
   ```

2. **Use FastAPI Docs**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Common Issues**
   - Check .env file is configured correctly
   - Verify email credentials
   - Check OpenAI API key validity
   - Review logs in `logs/app.log`

## Next Steps

1. Review this document and the project structure
2. Set up development environment per "Environment Setup" section
3. Implement Phase 2 (Services) following the patterns outlined
4. Create comprehensive tests
5. Implement Phase 3 (LangGraph Workflow)
6. Continue with phases 4 and 5

## References

- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Loguru Documentation](https://loguru.readthedocs.io/)
