# Architecture Documentation

## System Overview

Apex AI is a full-stack conversational AI platform implementing production-grade RAG (Retrieval-Augmented Generation) with enterprise features.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                    (Streamlit + Custom CSS)                  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer (app.py)                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Auth Manager │  │ Chat Handler │  │ Admin Panel  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
┌──────────────┐ ┌─────────────┐ ┌──────────────┐
│   Firebase   │ │  RAG System │ │    Stripe    │
│              │ │             │ │              │
│ • Auth       │ │ • LangChain │ │ • Payments   │
│ • Firestore  │ │ • Groq LLM  │ │ • Webhooks   │
│ • Analytics  │ │ • FAISS     │ │              │
└──────────────┘ └─────────────┘ └──────────────┘
```

## Core Components

### 1. RAG Pipeline

#### Document Processing
```python
Input Document → Chunking → Embedding → Vector Store

Chunking Strategy:
- Size: 1500 tokens (optimal for context vs cost)
- Overlap: 200 tokens (preserves context across boundaries)
- Separators: Hierarchical (paragraphs → sentences → words)
```

#### Retrieval Flow
```python
User Query → Embedding → Similarity Search → MMR Filter → Top-K Results

MMR Parameters:
- k: 6 (results returned)
- fetch_k: 12 (candidates evaluated)
- lambda_mult: 0.7 (relevance vs diversity balance)
```

#### Generation Process
```python
Query + Retrieved Context → Prompt Template → LLM → Response

Prompt Engineering:
- System context establishment
- Instruction clarity
- Source attribution requirements
- Multi-step reasoning guidance
```

### 2. LangChain LCEL Implementation

```python
rag_chain = (
    {
        "context": itemgetter("question") | retriever,
        "question": itemgetter("question")
    }
    | prompt
    | llm
    | StrOutputParser()
)
```

**Why LCEL?**
- Type safety with input/output schemas
- Composability for complex workflows
- Built-in tracing and debugging
- Better error handling than legacy chains

### 3. State Management

```python
Session State Structure:
├── authenticated (bool)
├── uid (str)
├── email (str)
├── role (str)
├── chat_history (list)
├── current_chat_id (str)
├── all_chats (list)
├── rag_chain (RunnableSequence)
└── show_history_sidebar (bool)
```

**Persistence Strategy:**
- In-memory: Current session state
- Firebase: Long-term storage
- Sync: On every user action

### 4. Firebase Schema

```
users/{uid}
├── email: string
├── full_name: string
├── plan: "free" | "premium"
├── created_at: timestamp
├── last_active: timestamp
├── messages_sent: number
├── documents_uploaded: number
└── chats/{chat_id}
    ├── title: string
    ├── messages: array
    ├── created_at: timestamp
    └── updated_at: timestamp

analytics/
├── usage_logs/{log_id}
│   ├── uid: string
│   ├── event: string
│   ├── timestamp: timestamp
│   └── metadata: object
├── performance_logs/{log_id}
│   ├── uid: string
│   ├── response_time_ms: number
│   ├── success: boolean
│   └── timestamp: timestamp
└── ratings/{rating_id}
    ├── uid: string
    ├── rating: number (1-5)
    └── timestamp: timestamp
```

## Data Flow

### Chat Message Flow
```
1. User Input
   └─→ UI validation
       └─→ Rate limit check
           └─→ Save to session state
               └─→ Track analytics

2. RAG Processing
   └─→ Embed query
       └─→ Retrieve context (MMR)
           └─→ Build prompt
               └─→ LLM inference
                   └─→ Parse response

3. Response Handling
   └─→ Save to session state
       └─→ Save to Firebase
           └─→ Track performance
               └─→ Update UI
```

### Authentication Flow
```
1. User submits credentials
   └─→ Firebase Auth verification
       └─→ Create/update Firestore document
           └─→ Initialize session state
               └─→ Load user data
                   └─→ Redirect to chat
```

## Performance Optimizations

### 1. Caching Strategy
```python
@st.cache_resource  # Shared across sessions
def load_embeddings():
    return HuggingFaceEmbeddings(...)

@st.cache_resource  # Shared across sessions
def build_vector_store():
    return FAISS.from_texts(...)
```

### 2. Lazy Loading
- RAG chain: Initialized on first use
- Chat history: Loaded on demand
- Vector store: Cached after first build

### 3. Async Operations
- Firebase writes: Non-blocking
- Analytics tracking: Fire-and-forget
- UI updates: Optimistic rendering

## Security Considerations

### 1. Authentication
- Firebase handles password hashing
- JWT tokens for session management
- Role-based access control

### 2. Data Protection
- API keys in environment variables
- Firebase credentials not in version control
- Firestore security rules enforced

### 3. Input Validation
- User input sanitization
- File upload restrictions
- Rate limiting per user

## Monitoring & Analytics

### Tracked Metrics
```python
User Metrics:
- DAU, WAU, MAU
- Retention rates
- Churn analysis

Usage Metrics:
- Messages per user
- Documents uploaded
- Peak usage times

Performance Metrics:
- Response times (p50, p95, p99)
- Success/error rates
- API latency

Business Metrics:
- MRR, ARPU, LTV
- Conversion rates
- Revenue per user
```

## Scalability Considerations

### Current Limits
- Concurrent users: 100+
- Vector store size: 10K+ documents
- Chat history: Unlimited per user

### Scaling Path
1. **Horizontal scaling**: Multiple Streamlit instances
2. **Database**: Firebase auto-scales
3. **Vector store**: Partition by user/domain
4. **LLM**: Groq handles inference scaling

## Technology Choices & Tradeoffs

### LangChain vs Custom
**Chose**: LangChain LCEL
**Why**: Built-in observability, community support
**Tradeoff**: Some abstraction overhead

### Firebase vs PostgreSQL
**Chose**: Firebase
**Why**: Real-time sync, managed infrastructure
**Tradeoff**: Less flexible querying

### Streamlit vs React
**Chose**: Streamlit
**Why**: Rapid development, Python-native
**Tradeoff**: Less control over frontend

### Groq vs OpenAI
**Chose**: Groq
**Why**: 10x faster inference, lower latency
**Tradeoff**: Smaller model selection

## Future Architecture Enhancements

1. **Microservices**: Separate RAG, auth, analytics
2. **Message Queue**: Async job processing
3. **CDN**: Static asset delivery
4. **Load Balancer**: Multi-region deployment
5. **Caching Layer**: Redis for hot data

## Development Workflow

```
1. Local Development
   └─→ Virtual environment
       └─→ Firebase emulators (optional)
           └─→ Hot reload with Streamlit

2. Testing
   └─→ Unit tests (pytest)
       └─→ Integration tests
           └─→ Manual QA

3. Deployment
   └─→ Git push to main
       └─→ Streamlit Cloud auto-deploy
           └─→ Health checks
               └─→ Production monitoring
```

## Error Handling Strategy

```python
Levels:
1. User-facing errors: Friendly messages
2. Technical logs: Detailed for debugging
3. Critical failures: Graceful degradation

Example:
try:
    result = rag_chain.invoke(query)
except Exception as e:
    log_error(e)  # Technical log
    show_fallback_ui()  # User sees retry option
    track_failure()  # Analytics
```

## Code Organization

```
app.py (1700+ lines):
├── Imports & Config
├── CSS Styling
├── Firebase Functions
├── RAG Pipeline
├── Auth Handlers
├── Chat Interface
├── Admin Dashboard
└── Main Router
```

## Performance Benchmarks

- **Cold start**: ~2-3 seconds (vector store load)
- **Hot path**: <500ms (cached vectors)
- **RAG inference**: 1-2 seconds (Groq + retrieval)
- **UI render**: <100ms (Streamlit)
- **Firebase write**: <200ms (async)

## Lessons Learned

1. **Chunk size matters**: 1500 tokens optimal for Llama 70B
2. **MMR improves diversity**: Better than pure similarity
3. **Session state is tricky**: Careful with Streamlit reruns
4. **Error handling is critical**: LLMs fail in unexpected ways
5. **Analytics from day one**: Can't add retroactively
