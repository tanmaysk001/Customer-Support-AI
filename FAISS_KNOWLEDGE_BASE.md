# FAISS Knowledge Base Integration Guide

## Overview

The Customer Support Email Agent now includes a FAISS-based vector knowledge base that enables semantic similarity search across documents. This guide explains how to set up, populate, and use the knowledge base in your workflow.

## What is FAISS?

**FAISS** (Facebook AI Similarity Search) is a library for efficient similarity search and clustering of dense vectors. It's perfect for:
- Semantic document search
- Finding relevant knowledge base articles
- Contextual information retrieval for LLM prompts
- Fast similarity matching at scale

## Architecture

```
Customer Email
    ↓
[Classification + Extraction]
    ↓
[FAISS Vector Search]
    ├─ Convert query to embedding (Sentence Transformers)
    ├─ Search FAISS index
    └─ Return top-k relevant documents
    ↓
[LLM Context Enrichment]
    └─ Inject retrieved documents into prompt
    ↓
[Generate Response]
```

## Setup Instructions

### 1. Install Dependencies

The following packages have been added to `requirements.txt`:

```
faiss-cpu==1.7.4              # Vector search library
sentence-transformers==2.2.2  # Embedding model
numpy==1.24.3                 # Numerical computing
```

Install them:

```bash
uv pip install -r requirements.txt
```

Or install individually:

```bash
pip install faiss-cpu sentence-transformers numpy
```

### 2. Initialize FAISS Knowledge Base

```python
from src.services.vector_kb_service import VectorKBService

# Create and initialize service
kb = VectorKBService(model_name="all-MiniLM-L6-v2")
await kb.initialize()
```

**Available Models:**
- `all-MiniLM-L6-v2` (lightweight, fast, 384 dimensions)
- `all-mpnet-base-v2` (more accurate, larger, 768 dimensions)
- `multi-qa-MiniLM-L6-cos-v1` (optimized for QA)
- `paraphrase-MiniLM-L6-v2` (paraphrase similarity)

### 3. Populate Knowledge Base

Two ways to populate:

#### Option A: Use the Provided Script

```bash
# Populate with 20 sample customer support documents
python scripts/populate_knowledge_base.py
```

This will:
1. Create FAISS index
2. Add 20 sample documents covering:
   - Product information
   - Technical support
   - Billing
   - Account management
   - Enterprise features
3. Save index to `data/vectors/faiss_index.bin`
4. Save metadata to `data/vectors/documents.json`

#### Option B: Programmatically Add Documents

```python
from src.services.vector_kb_service import VectorKBService

kb = VectorKBService()
await kb.initialize()

# Add a document
doc_id = await kb.add_document(
    title="How to Reset Password",
    content="To reset your password: 1) Click Forgot Password 2) Enter your email 3) Check your inbox for reset link...",
    category="technical_support",
    source_url="https://docs.example.com/password-reset"
)

print(f"Added document {doc_id}")
```

## Usage

### Basic Search

```python
# Search for relevant documents
results = await kb.search(
    query="How do I reset my password?",
    limit=5,  # Return top 5 results
    threshold=0.3  # Minimum similarity (0-1)
)

# Results structure:
# [
#     {
#         "id": 1,
#         "title": "Password Reset Guide",
#         "content": "...",
#         "category": "technical_support",
#         "similarity_score": 0.85
#     },
#     ...
# ]
```

### Category-Filtered Search

```python
# Search only within a specific category
results = await kb.search(
    query="How much does it cost?",
    category="billing",  # Only billing documents
    limit=3
)
```

### Format for LLM Context

```python
# Get documents
results = await kb.search(query, limit=5)

# Format for LLM prompt injection
context = await kb.format_context(results)

# Use in LLM prompt:
prompt = f"""
Please answer the customer question based on this context:

{context}

Customer Question: {customer_question}
"""
```

## Integration with Email Workflow

The knowledge base is automatically integrated in the `context_analysis_node`:

```python
# In src/nodes/context_analysis.py

vector_kb = VectorKBService()
await vector_kb.initialize()

# Search is automatically called
kb_results = await vector_kb.search(search_query, category=category, limit=5)

# Results injected into response generation
context_summary = await vector_kb.format_context(kb_results)

# LLM uses context_summary in prompt
```

## API Methods

### Search

```python
results = await kb.search(
    query: str,                 # Search query
    category: Optional[str],    # Category filter (optional)
    limit: int = 5,            # Max results
    threshold: float = 0.5     # Min similarity score
) -> List[Dict]
```

### Add Document

```python
doc_id = await kb.add_document(
    title: str,
    content: str,
    category: Optional[str],
    source_url: Optional[str]
) -> int
```

### Get Document

```python
doc = await kb.get_document(doc_id: int) -> Optional[Dict]
```

### Get by Category

```python
docs = await kb.get_by_category(
    category: str,
    limit: int = 10
) -> List[Dict]
```

### Format Context

```python
context_str = await kb.format_context(documents: List[Dict]) -> str
```

### Delete Document

```python
success = await kb.delete_document(doc_id: int) -> bool
```

### Clear All

```python
success = await kb.clear_all() -> bool
```

### Health Check

```python
health = await kb.health_check() -> Dict
# Returns: {
#     "status": "healthy",
#     "documents_count": 20,
#     "embedding_model": "all-MiniLM-L6-v2",
#     "index_dimension": 384
# }
```

## Test the Integration

Run the test script:

```bash
python scripts/test_kb_integration.py
```

This will:
1. Load the knowledge base
2. Simulate customer queries
3. Show relevant documents retrieved
4. Display context formatting
5. Demonstrate similarity matching

## File Locations

```
project/
├── src/services/
│   └── vector_kb_service.py       # Main FAISS service
├── scripts/
│   ├── populate_knowledge_base.py  # Setup script
│   └── test_kb_integration.py      # Test script
├── data/vectors/
│   ├── faiss_index.bin            # FAISS index (binary)
│   └── documents.json             # Document metadata
└── FAISS_KNOWLEDGE_BASE.md        # This file
```

## Performance Characteristics

| Operation | Time | Notes |
|-----------|------|-------|
| Initialize | ~2-5s | One-time, loads embedding model |
| Add Document | ~50-100ms | Per document |
| Search (100 docs) | ~5-10ms | Very fast |
| Format Context | <1ms | Formatting only |

## Advanced Features

### Custom Embedding Models

```python
kb = VectorKBService(model_name="all-mpnet-base-v2")  # More accurate
await kb.initialize()
```

### Batch Operations

```python
documents = [
    {"title": "...", "content": "...", "category": "..."},
    # ... more documents
]

for doc in documents:
    await kb.add_document(**doc)
```

### Similarity Threshold Tuning

Lower threshold (0.2-0.4): More results, less relevant
Higher threshold (0.7-0.9): Fewer results, more relevant

```python
# Broad search
results = await kb.search(query, threshold=0.2, limit=10)

# Strict search
results = await kb.search(query, threshold=0.8, limit=3)
```

## Troubleshooting

### Issue: "Module not found: faiss"

**Solution:** Install FAISS
```bash
pip install faiss-cpu
# Or for GPU: pip install faiss-gpu
```

### Issue: "No results found"

**Solutions:**
1. Lower the threshold: `threshold=0.2`
2. Check if KB is populated: `await kb.health_check()`
3. Try broader query without category filter
4. Check document content is relevant

### Issue: Slow searches

**Solutions:**
1. Use lightweight model: `"all-MiniLM-L6-v2"`
2. Reduce `limit` parameter
3. Use category filters to narrow search space
4. Consider upgrading to GPU: `pip install faiss-gpu`

## Sample Documents Coverage

The provided sample documents cover:

**Product Information (4 docs)**
- Overview and features
- Pricing plans
- Security and compliance
- Enterprise features

**Technical Support (7 docs)**
- Sync troubleshooting
- Installation guide
- Network requirements
- Mobile app help
- Password reset
- API documentation
- Large file handling

**Billing (3 docs)**
- Pricing plans
- FAQ and refunds
- Payment methods
- Update billing

**Account Management (3 docs)**
- Security practices
- Account recovery
- Data export
- Team management

## Example Workflow

```python
# 1. Customer sends email
email = {
    "subject": "How do I enable two-factor authentication?",
    "body": "For security, I want to enable 2FA on my account..."
}

# 2. Classification happens
category = "product_inquiry"

# 3. KB search is performed (automatically in context_analysis_node)
kb_results = await vector_kb.search(
    query=f"{email['subject']} {email['body']}",
    category=category,
    limit=5
)

# 4. Context is formatted
context = await vector_kb.format_context(kb_results)
# Output: "Relevant documentation:\n1. **Account Security Best Practices** (Relevance: 92%)\n..."

# 5. LLM generates response using context
response = await llm_service.generate_response(
    subject=email['subject'],
    body=email['body'],
    category=category,
    priority="medium",
    context=context  # <- KB results injected here
)

# 6. Response sent to customer
```

## Next Steps

1. **Run populate script:** `python scripts/populate_knowledge_base.py`
2. **Run test script:** `python scripts/test_kb_integration.py`
3. **Start the app:** `python main.py`
4. **Process an email** with knowledge base retrieval

## Additional Resources

- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [Sentence Transformers](https://www.sbert.net/)
- [Vector Search Best Practices](https://github.com/facebookresearch/faiss/wiki)

## Support

For issues:
1. Check the troubleshooting section
2. Run `await kb.health_check()` to verify status
3. Review logs in `logs/app.log`
4. Check FAISS index exists: `data/vectors/faiss_index.bin`
