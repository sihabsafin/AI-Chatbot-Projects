# Setup Guide - Apex AI

Complete setup instructions for running Apex AI locally or deploying to production.

## Prerequisites

- Python 3.9 or higher
- Firebase project with Firestore enabled
- Groq API key ([Get one here](https://console.groq.com))
- (Optional) Stripe account for payment processing
- (Optional) LangSmith account for tracing

## Step-by-Step Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/apex-ai.git
cd apex-ai
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Firebase Setup

#### Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com)
2. Create new project
3. Enable Firestore Database
4. Enable Authentication → Email/Password

#### Download Credentials
1. Project Settings → Service Accounts
2. Generate new private key
3. Save as `firebase-credentials.json` in project root

#### Firestore Security Rules
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
      
      match /chats/{chatId} {
        allow read, write: if request.auth != null && request.auth.uid == userId;
      }
    }
    
    match /analytics/{document=**} {
      allow read: if request.auth != null;
      allow write: if request.auth != null;
    }
  }
}
```

### 5. Create Streamlit Secrets

Create `.streamlit/secrets.toml`:

```toml
# Groq API
GROQ_API_KEY = "your_groq_api_key_here"

# Firebase (copy from firebase-credentials.json)
[firebase]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n"
client_email = "firebase-adminsdk@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-cert-url"

# Optional: Stripe
STRIPE_SECRET_KEY = "sk_test_..."
STRIPE_PRICE_ID = "price_..."

# Optional: LangSmith
LANGSMITH_API_KEY = "your_langsmith_key"
LANGCHAIN_PROJECT = "apex-ai-rag"
```

### 6. Create Knowledge Base

Create `knowledge.txt` with your documents:

```text
# Your Knowledge Base

Add your documents, FAQs, or content here.
The RAG system will use this to answer questions.

Example:
Q: What is Apex AI?
A: Apex AI is an enterprise RAG chatbot platform...
```

### 7. Update firebase_config.py

Ensure your `firebase_config.py` has the correct structure:

```python
import firebase_admin
from firebase_admin import credentials, firestore, auth
import streamlit as st

def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase-credentials.json")
        firebase_admin.initialize_app(cred)

def get_db():
    initialize_firebase()
    return firestore.client()

# Add all other functions from your existing firebase_config.py
```

### 8. Run Application

```bash
streamlit run app.py
```

Open browser to `http://localhost:8501`

## Deployment

### Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Add secrets in dashboard (copy from secrets.toml)
5. Deploy

### Deploy to Other Platforms

#### Heroku
```bash
# Create Procfile
web: streamlit run app.py --server.port=$PORT

# Deploy
heroku create your-app-name
git push heroku main
```

#### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

## Troubleshooting

### Firebase Connection Issues
- Verify credentials.json is in project root
- Check Firebase project permissions
- Ensure Firestore is enabled

### Groq API Errors
- Verify API key is correct
- Check rate limits
- Ensure model name is valid

### Streamlit Errors
- Clear cache: `.streamlit/cache`
- Update Streamlit: `pip install --upgrade streamlit`
- Check Python version

## Environment Variables

For production, use environment variables instead of secrets.toml:

```bash
export GROQ_API_KEY="your_key"
export FIREBASE_CREDENTIALS="path_to_json"
export STRIPE_SECRET_KEY="your_key"
```

## Testing

Basic functionality test:

```bash
# Test imports
python -c "import streamlit; import langchain; import firebase_admin; print('All imports successful')"

# Test Firebase connection
python -c "from firebase_config import get_db; db = get_db(); print('Firebase connected')"
```

## Performance Optimization

1. **Vector Store Caching**: Already implemented with `@st.cache_resource`
2. **Firebase Indexes**: Create indexes for frequent queries
3. **CDN**: Use CDN for static assets in production
4. **Monitoring**: Enable LangSmith for production debugging

## Security Checklist

- [ ] Firebase credentials not in version control
- [ ] API keys stored in secrets/environment variables
- [ ] Firestore security rules configured
- [ ] HTTPS enabled in production
- [ ] Rate limiting configured
- [ ] Input validation implemented

## Support

For issues or questions:
1. Check existing GitHub issues
2. Review documentation
3. Contact: [your-email@example.com]

---

**Next Steps:**
1. Customize knowledge.txt with your content
2. Configure branding/styling
3. Set up monitoring
4. Deploy to production
