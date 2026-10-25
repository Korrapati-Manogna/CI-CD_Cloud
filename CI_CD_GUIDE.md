# Cloud CI/CD Pipeline & Containerization Guide

This project includes a cloud-native **Continuous Integration & Continuous Deployment (CI/CD)** pipeline configured with **GitHub Actions** and **Docker**.

---

## 🏗️ Architecture Overview

```
                      +-----------------------------+
                      |   Git Push / Pull Request   |
                      +--------------+--------------+
                                     |
                                     v
                 +---------------------------------------+
                 |       GitHub Actions CI Runner        |
                 +-------------------+-------------------+
                                     |
           +-------------------------+-------------------------+
           |                         |                         |
           v                         v                         v
+--------------------+    +--------------------+    +--------------------+
|  Backend Test Job  |    | Frontend Build Job |    |  Docker Build Job  |
|  - Python 3.12     |    | - Node.js 20       |    | - Backend Docker   |
|  - Flake8 Lint     |    | - Vite Build       |    | - Frontend Docker  |
|  - Pytest / Unittest|   | - Asset Bundle     |    | - Syntax Validate  |
+----------+---------+    +----------+---------+    +----------+---------+
           |                         |                         |
           +-------------------------+-------------------------+
                                     |
                             (All Tests Pass)
                                     |
                                     v
                 +---------------------------------------+
                 |       GitHub Actions CD Runner        |
                 +-------------------+-------------------+
                                     |
           +-------------------------+-------------------------+
           |                                                   |
           v                                                   v
+--------------------+                               +--------------------+
| Vercel Production  |                               | Docker Hub / Cloud |
| Zero-Downtime Live |                               | Container Registry |
+--------------------+                               +--------------------+
```

---

## 📁 CI/CD File Structure

- **`.github/workflows/ci.yml`**: Continuous Integration workflow that automatically triggers on every push and pull request. Runs:
  1. Backend unit tests and PEP8 lint checks.
  2. Frontend dependency installation and production Vite bundling.
  3. Multi-stage Docker container build verification.
- **`.github/workflows/deploy.yml`**: Continuous Deployment workflow that deploys to Vercel on merges to `main`.
- **`Dockerfile.backend`**: Containerized FastAPI microservice with health checks.
- **`Dockerfile.frontend`**: Multi-stage build with Node.js 20 and Alpine Nginx reverse proxy.
- **`docker-compose.yml`**: Multi-container local/cloud orchestration.
- **`tests/test_api.py`**: Automated API contract and endpoint test suite.

---

## 🐳 Running with Docker Locally

To run the entire full-stack application using Docker:

```bash
docker compose up --build
```

- **Frontend Application**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000/api/tickets`
- **Health Check**: `http://localhost:8000/api/health`

To stop the containers:
```bash
docker compose down
```

---

## 🔑 Configuring GitHub Secrets for Automated Deployment

To enable zero-touch automated deployments to Vercel via GitHub Actions:

1. Open your GitHub Repository: `https://github.com/Korrapati-Manogna/CI-CD_Cloud`
2. Navigate to **Settings** > **Secrets and variables** > **Actions** > **New repository secret**.
3. Add the following secrets:

| Secret Name | Value | Purpose |
| :--- | :--- | :--- |
| `VERCEL_TOKEN` | Your Vercel Personal Access Token | Allows GitHub Actions to deploy to Vercel |
| `VERCEL_ORG_ID` | Found in `.vercel/project.json` | Vercel Organization ID |
| `VERCEL_PROJECT_ID` | Found in `.vercel/project.json` | Vercel Project ID |
| `GROQ_API_KEY` | `gsk_MRTXewXnFW...` | LLM Inference API Key |
| `HINDSIGHT_API_KEY` | `hsk_c5b6d1809a...` | Memory Engine Key |

---

## 🧪 Running Tests Locally

```bash
# Run backend tests
python -m unittest discover -s tests -p "test_*.py"

# Build frontend
cd frontend && npm run build
```
