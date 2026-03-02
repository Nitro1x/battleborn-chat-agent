# Deployment Guide - BattleBorn Chat Agent

## Quick Start: Streamlit Cloud (Recommended)

### Step 1: Prepare Your Repository
Your code is already on GitHub (`Nitro1x/battleborn-chat-agent`). Ensure all changes are committed:

```bash
git status
git add .
git commit -m "Ready for deployment"
git push
```

### Step 2: Deploy to Streamlit Cloud

1. Visit [streamlit.io/cloud](https://streamlit.io/cloud)
2. Click **"New app"**
3. Select deployment method: **GitHub**
4. Authenticate with your GitHub account
5. Fill in:
   - **Repository**: `Nitro1x/battleborn-chat-agent`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
6. Click **"Deploy"**

Your app will begin deploying and be accessible at:
```
https://<your-username>-battleborn-chat-agent.streamlit.app
```

### Step 3: Add Secrets

1. In the Streamlit Cloud dashboard, select your app
2. Click **⚙️ Settings** (bottom right)
3. Click **"Secrets"**
4. Add your Google API key:
   ```toml
   GOOGLE_API_KEY = "your-actual-google-api-key-here"
   ```
5. Click **"Save"**
6. The app will automatically redeploy with the secret available

---

## Alternative: Docker Deployment

### Option A: Docker Hub

Create a `Dockerfile` in your repo root:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY streamlit_app.py .
RUN mkdir -p ~/.streamlit

# Create config
RUN echo "[server]\nheadless = true\nport = 8501\nenableXsrfProtection = false" > ~/.streamlit/config.toml

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py"]
```

Build and push:

```bash
docker build -t nitro1x/battleborn-chat-agent .
docker login
docker push nitro1x/battleborn-chat-agent
```

### Option B: AWS App Runner / Google Cloud Run

Deploy the Docker image:

```bash
# Google Cloud Run
gcloud run deploy battleborn-chat-agent \
  --image nitro1x/battleborn-chat-agent \
  --platform managed \
  --region us-central1 \
  --set-env-vars GOOGLE_API_KEY="your-key-here"

# AWS App Runner
aws apprunner create-service \
  --service-name battleborn-chat-agent \
  --source-configuration ImageRepository={ImageRepositoryType=ECR,ImageIdentifier=your-ecr-uri/battleborn-chat-agent}
```

---

## Testing Before Deployment

### Local Test
```bash
streamlit run streamlit_app.py
```

Then open `http://localhost:8501` in your browser.

### Production Readiness Checklist
- [ ] All tests pass locally
- [ ] API key works and has access to models
- [ ] All dependencies in `requirements.txt`
- [ ] No hardcoded secrets in code
- [ ] Error handling covers edge cases
- [ ] README.md has clear setup instructions

---

## Monitoring & Troubleshooting

### Check Logs
**Streamlit Cloud**: Dashboard → App → **Logs**

**Docker/Cloud Run**: Use your cloud provider's logging service

### Common Issues

| Issue | Solution |
|-------|----------|
| API Key error | Verify in Secrets → `GOOGLE_API_KEY=value` |
| Model not found | App auto-detects available models; check API quota |
| Empty responses | Might be rate-limited; wait a moment and retry |
| Dependencies fail | Run `pip install -r requirements.txt` locally first |

---

## Environment Variables

Required:
- `GOOGLE_API_KEY` — Google Generative AI API key

Optional (for development):
- `DEBUG=true` — Enable verbose logging

---

## Scaling

For high traffic, consider:
- **Streamlit Cloud**: Automatic scaling (paid tier)
- **Cloud Run**: Set max concurrent requests
- **Load Balancer**: Place in front of multiple instances

---

## Rollback

If deployment breaks:

```bash
# Revert to previous commit
git revert HEAD
git push

# Streamlit Cloud auto-deploys from main branch
# Docker: tag and redeploy previous image version
```

---

## Support

- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)
- **Google Generative AI**: [ai.google.dev](https://ai.google.dev)
