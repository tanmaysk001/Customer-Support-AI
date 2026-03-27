# FAISS Knowledge Base - Command Reference

## Installation & Setup

### 1. Install All Dependencies
```bash
cd c:\Users\Sunny\custmor-support-email-agent
uv pip install -r requirements.txt
```

### 2. Create Data Directory
```bash
mkdir data\vectors
```

---

## Populate Knowledge Base

### Run Setup Script (Creates FAISS Index)
```bash
python scripts/populate_knowledge_base.py
```

**What it does:**
- ✅ Loads embedding model (first run: ~2-5 seconds)
- ✅ Creates FAISS index with 20 documents
- ✅ Saves index to `data/vectors/faiss_index.bin`
- ✅ Saves metadata to `data/vectors/documents.json`
- ✅ Shows sample searches
- ✅ Displays total documents and statistics

**Expected output:**
```
Initializing Vector Knowledge Base Service...
Loading embedding model: all-MiniLM-L6-v2
Created new FAISS index (dimension: 384)
Adding 20 documents to knowledge base...
Added document 1: Product Overview - CloudSync Pro
Added document 2: CloudSync Pro Features
...
Knowledge Base Summary
==================================================
Total Documents: 20
Embedding Model: all-MiniLM-L6-v2
Vector Dimension: 384
✅ Knowledge base population complete!
```

---

## Test & Validate

### Test Integration
```bash
python scripts/test_kb_integration.py
```

**What it does:**
- ✅ Tests semantic search functionality
- ✅ Shows multiple customer scenarios
- ✅ Displays similarity scoring
- ✅ Demonstrates relevance matching

**Expected output:**
```
FAISS Knowledge Base Integration Test
================================================================================

1️⃣  Initializing FAISS Vector KB...
   Status: healthy
   Documents in KB: 20

2️⃣  Test Scenario 1: Customer asking about billing
Customer Question: How much does CloudSync cost?
Details: Hi, I want to know about your pricing plans...

🔍 Found 3 relevant documents:
   1. CloudSync Pricing Plans
      Relevance: 95%
   2. Billing FAQ - Common Questions
      Relevance: 87%
   3. Payment Methods and Refunds
      Relevance: 79%
```

### Run Workflow Example
```bash
python scripts/example_kb_usage.py
```

**What it does:**
- ✅ Simulates real customer email
- ✅ Shows KB retrieval process
- ✅ Demonstrates context formatting
- ✅ Shows response generation

**Expected output:**
```
FAISS KB Example: Real Workflow
================================================================================

📧 Step 1: Customer Email Received

From: john@example.com
Subject: Can't sync files on my phone
Body: Hi, I've been trying to sync my files between...

🔍 Step 3: Search Knowledge Base

Found 3 relevant documents:
   1. Troubleshooting Sync Issues
      Relevance: 92%
```

---

## Run Application

### Start the API Server
```bash
python main.py
```

**Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**API Endpoints:**
- Health: `http://localhost:8000/api/health`
- Docs: `http://localhost:8000/docs` (Swagger UI)
- ReDoc: `http://localhost:8000/redoc`

---

## Manual KB Operations

### Python REPL - Interactive Testing

```python
import asyncio
from src.services.vector_kb_service import VectorKBService

async def test_kb():
    # Initialize
    kb = VectorKBService()
    await kb.initialize()

    # Search
    results = await kb.search("How do I fix sync issues?", limit=3)

    # Display results
    for doc in results:
        print(f"{doc['title']} - {doc['similarity_score']:.1%}")

    # Check health
    health = await kb.health_check()
    print(f"Status: {health['status']}")
    print(f"Documents: {health['documents_count']}")

asyncio.run(test_kb())
```

### Add New Document
```python
async def add_doc():
    kb = VectorKBService()
    await kb.initialize()

    doc_id = await kb.add_document(
        title="Custom Document",
        content="Full document content here...",
        category="product_inquiry",
        source_url="https://example.com"
    )

    print(f"Added document {doc_id}")

asyncio.run(add_doc())
```

### Search by Category
```python
async def search_category():
    kb = VectorKBService()
    await kb.initialize()

    # Search billing documents only
    results = await kb.search(
        query="payment methods",
        category="billing",
        limit=5
    )

    for doc in results:
        print(f"{doc['title']} ({doc['category']})")

asyncio.run(search_category())
```

---

## Development Commands

### Format Code
```bash
black src/ tests/ scripts/
```

### Lint Code
```bash
ruff check src/ tests/ scripts/
```

### Type Check
```bash
mypy src/
```

### Run Tests
```bash
pytest tests/ -v
```

### Run Specific Test
```bash
pytest tests/test_kb_integration.py -v
```

---

## Troubleshooting Commands

### Check if FAISS Index Exists
```bash
ls -la data/vectors/
# Should show:
# - faiss_index.bin
# - documents.json
```

### Verify KB Health
```python
import asyncio
from src.services.vector_kb_service import VectorKBService

async def check_health():
    kb = VectorKBService()
    await kb.initialize()
    health = await kb.health_check()

    for key, value in health.items():
        print(f"{key}: {value}")

asyncio.run(check_health())
```

### View Document Metadata
```bash
cat data/vectors/documents.json | python -m json.tool
```

### Clear and Rebuild KB
```python
import asyncio
from src.services.vector_kb_service import VectorKBService

async def rebuild():
    kb = VectorKBService()
    await kb.initialize()

    # Clear all
    await kb.clear_all()
    print("Cleared KB")

    # Rebuild by running populate script

asyncio.run(rebuild())
```

---

## Database Operations

### Initialize Database
```bash
python -c "from src.db.database import init_db; init_db()"
```

### Check Database Contents
```python
from src.db.database import SessionLocal
from src.db.models import Email

db = SessionLocal()
emails = db.query(Email).all()
print(f"Total emails: {len(emails)}")
```

---

## File Locations

### Key Files
```
src/services/vector_kb_service.py       ← Main service (340 lines)
src/nodes/context_analysis.py           ← Integration point
scripts/populate_knowledge_base.py       ← Setup script
scripts/test_kb_integration.py          ← Test script
scripts/example_kb_usage.py             ← Example script
```

### Data Files
```
data/vectors/faiss_index.bin            ← FAISS index (binary)
data/vectors/documents.json             ← Document metadata (JSON)
logs/app.log                            ← Application logs
```

### Documentation
```
FAISS_KNOWLEDGE_BASE.md                 ← Full guide (500+ lines)
QUICKSTART_FAISS.md                     ← Quick start (5 minutes)
FAISS_IMPLEMENTATION_SUMMARY.md         ← Implementation summary
FAISS_COMMANDS.md                       ← This file
```

---

## Complete Workflow

### 1. Initial Setup (One Time)
```bash
# Clone/Navigate to project
cd c:\Users\Sunny\custmor-support-email-agent

# Install dependencies
uv pip install -r requirements.txt

# Populate knowledge base
python scripts/populate_knowledge_base.py

# Test integration
python scripts/test_kb_integration.py
```

### 2. Run Application
```bash
# Start API server
python main.py

# In another terminal, process emails via API
curl -X POST http://localhost:8000/api/emails/process -H "Content-Type: application/json" \
  -d '{"email_id": 1}'
```

### 3. Monitor
```bash
# Check logs
tail -f logs/app.log

# Check FAISS KB health
python scripts/test_kb_integration.py
```

---

## Performance Verification

### Measure Search Speed
```python
import asyncio
import time
from src.services.vector_kb_service import VectorKBService

async def benchmark():
    kb = VectorKBService()
    await kb.initialize()

    # Warm up
    await kb.search("test query", limit=1)

    # Benchmark
    queries = [
        "How do I reset my password?",
        "What are the pricing plans?",
        "How do I fix sync issues?",
        "Tell me about enterprise features",
    ]

    total_time = 0
    for query in queries:
        start = time.time()
        results = await kb.search(query, limit=5)
        elapsed = time.time() - start
        total_time += elapsed
        print(f"Query: {query}")
        print(f"  Results: {len(results)}")
        print(f"  Time: {elapsed*1000:.1f}ms\n")

    avg_time = total_time / len(queries) * 1000
    print(f"Average search time: {avg_time:.1f}ms")
    print(f"Throughput: {1000/avg_time:.0f} queries/second")

asyncio.run(benchmark())
```

---

## Environment Variables

### .env File
```bash
# Optional - FAISS will use defaults
VECTOR_STORE_PATH=./data/vectors

# Other settings
OPENAI_API_KEY=your-key-here
EMAIL_ADDRESS=your-email@example.com
DATABASE_URL=sqlite:///./customer_support.db
```

---

## Documentation Quick Links

| File | Purpose | Read Time |
|------|---------|-----------|
| QUICKSTART_FAISS.md | Get started in 5 minutes | 5 min |
| FAISS_COMMANDS.md | Command reference (this file) | 10 min |
| FAISS_IMPLEMENTATION_SUMMARY.md | Overview of implementation | 10 min |
| FAISS_KNOWLEDGE_BASE.md | Complete documentation | 30 min |

---

## Common Issues & Solutions

### Issue: "No module named 'faiss'"
```bash
# Solution
pip install faiss-cpu
```

### Issue: "Vector store path not found"
```bash
# Solution
mkdir -p data/vectors
python scripts/populate_knowledge_base.py
```

### Issue: "Empty knowledge base"
```bash
# Solution
python scripts/populate_knowledge_base.py
```

### Issue: "Search returns no results"
```python
# Try lowering threshold
results = await kb.search(query, threshold=0.2)  # was 0.5
```

---

## Useful Aliases (Optional)

Create a `Makefile`:

```makefile
.PHONY: install setup test run clean

install:
	uv pip install -r requirements.txt

setup:
	python scripts/populate_knowledge_base.py

test:
	python scripts/test_kb_integration.py

example:
	python scripts/example_kb_usage.py

run:
	python main.py

clean:
	rm -rf data/vectors/*.bin data/vectors/*.json
	find . -type d -name __pycache__ -exec rm -rf {} +
```

Usage:
```bash
make install
make setup
make test
make run
```

---

## Success Indicators

✅ You've successfully set up FAISS when:
- [ ] `python scripts/populate_knowledge_base.py` runs without errors
- [ ] `data/vectors/faiss_index.bin` exists (~1MB)
- [ ] `data/vectors/documents.json` has 20 documents
- [ ] `python scripts/test_kb_integration.py` shows 3+ results per query
- [ ] `python main.py` starts successfully
- [ ] Logs show KB retrieval happening (check `logs/app.log`)

---

## Next Actions

1. **Run populate script**
   ```bash
   python scripts/populate_knowledge_base.py
   ```

2. **Test integration**
   ```bash
   python scripts/test_kb_integration.py
   ```

3. **See workflow example**
   ```bash
   python scripts/example_kb_usage.py
   ```

4. **Start application**
   ```bash
   python main.py
   ```

5. **Process emails with KB-enriched responses**

**You're ready to go! 🚀**
