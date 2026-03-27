# Quick Start: FAISS Knowledge Base

## 🚀 5-Minute Setup

### 1. Install Dependencies
```bash
uv pip install -r requirements.txt
```

### 2. Populate Knowledge Base with Sample Documents
```bash
python scripts/populate_knowledge_base.py
```

**Output:**
- Creates FAISS vector index
- Adds 20 sample documents
- Saves to `data/vectors/`
- Shows sample search results

### 3. Test the Integration
```bash
python scripts/test_kb_integration.py
```

### 4. See Real Workflow Example
```bash
python scripts/example_kb_usage.py
```

---

## 📁 What Was Added

### New Files

```
src/services/
└── vector_kb_service.py          # FAISS KB service (340 lines)

scripts/
├── populate_knowledge_base.py     # Setup script with 20 sample docs
├── test_kb_integration.py         # Integration tests
└── example_kb_usage.py            # Real workflow example

FAISS_KNOWLEDGE_BASE.md            # Full documentation
QUICKSTART_FAISS.md                # This file
```

### Updated Files

```
requirements.txt                   # Added faiss-cpu, sentence-transformers, numpy
src/nodes/context_analysis.py      # Updated to use FAISS KB
```

---

## 🎯 What FAISS Does

### Before (Keyword Search)
```
Customer: "How do I fix sync?"
Search: Look for exact keywords
Result: No match or irrelevant results
```

### After (Vector Similarity Search)
```
Customer: "How do I fix sync?"
Search: Convert to vector → Find similar embeddings
Result: "Troubleshooting Sync Issues" (92% match)
```

---

## 📊 Sample Documents Included

20 documents across 4 categories:

- **Product Information** (4): Features, pricing, security, enterprise
- **Technical Support** (7): Installation, troubleshooting, mobile, API
- **Billing** (3): Pricing, payments, refunds
- **Account Management** (3): Security, recovery, data export

---

## 💡 Usage Examples

### Example 1: Customer Asks About Pricing
```python
customer_query = "How much does CloudSync cost?"

results = await kb.search(customer_query, category="billing", limit=3)
# Returns:
# [
#   {
#     "title": "CloudSync Pricing Plans",
#     "similarity_score": 0.95,
#     "content": "Free Plan: Up to 5GB... Pro Plan: $9.99/month..."
#   },
#   ...
# ]
```

### Example 2: Use KB Results in LLM Response
```python
# Search KB
kb_results = await kb.search(query, category="technical_support", limit=5)

# Format for LLM
context = await kb.format_context(kb_results)

# Use in prompt
response = await llm_service.generate_response(
    subject=email['subject'],
    body=email['body'],
    category=category,
    context=context  # <- KB info injected
)
```

### Example 3: Search by Category
```python
# Billing questions
billing_docs = await kb.get_by_category("billing", limit=5)

# Technical support
tech_docs = await kb.get_by_category("technical_support", limit=5)
```

---

## 🔧 Key API Methods

```python
# Search with semantic similarity
results = await kb.search(
    query="user question here",
    category="billing",  # optional
    limit=5,            # top 5 results
    threshold=0.3       # minimum relevance
)

# Add new document
doc_id = await kb.add_document(
    title="Document Title",
    content="Full content...",
    category="technical_support",
    source_url="https://..."
)

# Get document by ID
doc = await kb.get_document(doc_id)

# Delete document
await kb.delete_document(doc_id)

# Get all by category
docs = await kb.get_by_category("billing")

# Format results for LLM
context = await kb.format_context(results)

# Check health
health = await kb.health_check()
```

---

## 📈 How It Improves Your Email Agent

| Aspect | Before | After |
|--------|--------|-------|
| **Search Accuracy** | Keyword matching | Semantic similarity |
| **Irrelevant Results** | Common | Rare |
| **Missing Context** | LLM guesses | KB informed |
| **Response Quality** | Generic | Knowledge-based |
| **Consistency** | Variable | Standardized |

---

## 🎓 Understanding FAISS

**FAISS = Facebook AI Similarity Search**

1. **Embedding**: Converts text to vectors using Sentence Transformers
2. **Index**: Stores vectors in optimized data structure
3. **Search**: Finds most similar vectors using L2 distance
4. **Results**: Returns most relevant documents

```
Customer Query
    ↓
[Embed: "How to reset password?"]
    ↓
[Vector: [0.23, -0.45, 0.12, ...]]
    ↓
[Search in FAISS Index]
    ↓
[Find Similar Vectors]
    ↓
[Return Matching Documents]
```

---

## 🚦 Troubleshooting

### Issue: "No results found"
```python
# Lower threshold to get more results
results = await kb.search(query, threshold=0.2)  # was 0.5

# Or remove category filter
results = await kb.search(query, category=None)
```

### Issue: "FAISS not found"
```bash
pip install faiss-cpu
```

### Issue: "Empty knowledge base"
```bash
# Populate it
python scripts/populate_knowledge_base.py

# Or add documents programmatically
await kb.add_document(title="...", content="...")
```

---

## 📚 File Structure

```
project/
├── src/
│   └── services/
│       └── vector_kb_service.py       # FAISS implementation
│
├── scripts/
│   ├── populate_knowledge_base.py      # Setup (RUN THIS FIRST!)
│   ├── test_kb_integration.py          # Tests
│   └── example_kb_usage.py             # Examples
│
├── data/
│   └── vectors/
│       ├── faiss_index.bin             # Vectorized documents
│       └── documents.json              # Document metadata
│
├── src/nodes/
│   └── context_analysis.py             # Updated to use FAISS
│
└── FAISS_KNOWLEDGE_BASE.md             # Full documentation
```

---

## ✅ Checklist

- [ ] Run `python scripts/populate_knowledge_base.py`
- [ ] Run `python scripts/test_kb_integration.py`
- [ ] Run `python scripts/example_kb_usage.py`
- [ ] Check `data/vectors/` contains `faiss_index.bin`
- [ ] Start app: `python main.py`
- [ ] Test with email containing a question about:
  - Pricing (billing category)
  - Technical issues (technical_support category)
  - Product features (product_inquiry category)

---

## 🎯 Next Steps

1. **Run populate script** to create knowledge base
2. **Test with sample queries** using test script
3. **Start the application** and process emails
4. **Monitor logs** to see KB retrieval happening
5. **Add your own documents** as needed

---

## 💬 How It Works in Your Workflow

```
Email arrives → Classification → FAISS Search ← NEW!
                                    ↓
                            Find relevant docs
                                    ↓
                          Inject into LLM prompt ← NEW!
                                    ↓
                         Generate better response ← IMPROVED!
                                    ↓
                            Send to customer
```

---

## 🔍 Example Output

When you run the test script:

```
Found 3 relevant documents via FAISS vector search:

1. Troubleshooting Sync Issues (Relevance: 92%)
   "If files aren't syncing: 1) Check internet connection..."

2. Network Connection Requirements (Relevance: 85%)
   "CloudSync requires a stable internet connection with minimum 1 Mbps..."

3. Mobile App Troubleshooting (Relevance: 78%)
   "For iOS/Android issues: Ensure app is updated to latest version..."
```

---

## 📖 Full Documentation

See `FAISS_KNOWLEDGE_BASE.md` for:
- Advanced configuration
- Custom embedding models
- Performance tuning
- API reference
- Troubleshooting

---

## 🎉 You're Ready!

The FAISS knowledge base is fully integrated and ready to use. Your email agent will now:
- ✅ Find relevant documentation automatically
- ✅ Inject context into LLM responses
- ✅ Provide more accurate, knowledge-based answers
- ✅ Maintain consistency across responses

**Start here:** `python scripts/populate_knowledge_base.py`
