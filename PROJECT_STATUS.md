# Project Status & Continuation Guide

**Project:** Capstone — Production-Ready Azure Architecture with CI/CD, Bicep IaC, and AI Feature
**Last Updated:** 2025-11-27
**Status:** ~80% Complete — Code & Infrastructure Ready, Awaiting Azure Deployment

---

## ✅ COMPLETED WORK

### Backend Application
- FastAPI server with health check (`GET /health`) and AI summarize endpoint (`POST /ai/summarize`)
- Adapter pattern for LLM providers (mock, Azure OpenAI, OpenRouter)
- JSON structured logging with request ID correlation
- Request-ID middleware for tracing
- Global exception handler with error tracking
- Local testing verified: `http://localhost:8000/health` returns `{"status":"ok"}`
- Interactive API docs at `http://localhost:8000/docs` (Swagger UI)

### Infrastructure as Code (Bicep)
- Main orchestration template: `capstone/infra/main.bicep`
- Modular Bicep components:
  - `vnet.bicep` — Virtual Network with app & privatelink subnets
  - `keyvault.bicep` — Key Vault with disabled public access (Private Endpoint ready)
  - `privatelink.bicep` — Private DNS zone + Private Endpoint for Key Vault
  - `containerregistry.bicep` — Azure Container Registry
  - `loganalytics.bicep` — Log Analytics workspace
  - `containerapp_env.bicep` — Container Apps environment
  - `containerapp.bicep` — Container App with system-assigned Managed Identity & RBAC role assignments
- Parameters file: `capstone/infra/parameters.dev.json`

### CI/CD Pipeline (GitHub Actions)
- Workflow file: `.github/workflows/ci-cd.yml`
- Steps implemented:
  1. Build Docker image (tagged by commit SHA, no `latest`)
  2. Push to Azure Container Registry (ACR)
  3. Deploy to Container Apps with updated image
  4. Set canary traffic to 10% (gradual rollout)
  5. Run smoke tests (health check)
  6. Promote to 100% traffic on success, or rollback on failure
- Workflow injects `APPINSIGHTS_CONNECTION_STRING` as container environment variable

### Documentation
- `README.md` — Quick start, env vars, project overview
- `capstone/docs/TELEMETRY.md` — Application Insights setup guide with local testing instructions
- `capstone/docs/GITHUB-SECRETS.md` — GitHub secrets list and `gh secret set` command examples
- `capstone/docs/architecture.md` — Mermaid diagrams (logical & network architecture)
- `PRD.md` — Project requirements and non-functional constraints
- `AGENTS.md` — AI-assisted coding guidelines
- `Harjoitusseuranta/paivakirja.md` — Exercise journal/diary (Finnish)

### Local Development
- `docker-compose.yml` — Defines `backend` (FastAPI + reload) and `redis` services
- `Dockerfile` — Multi-stage build for production image
- `requirements.txt` — Python dependencies (FastAPI, uvicorn, redis, logging, pytest, httpx)
- `capstone/backend/app/` — Application modules:
  - `main.py` — FastAPI app initialization, middleware, exception handler
  - `routes.py` — Health & AI summarize endpoints
  - `ai_adapter.py` — LLM adapter pattern (supports mock, AOAI, OpenRouter)
  - `cache.py` — Async cache wrapper (Redis or in-memory)
  - `logging_config.py` — JSON structured logging setup
- Tests: `capstone/backend/tests/test_health.py` — Basic health check test

### Repository
- Git repo initialized at `C:\Users\jaana\capstone`
- Remote: `https://github.com/Jaanayl/capstone`
- Branches:
  - `main` — Current stable branch with all merged work
  - `feature/m5-capstone` — Feature branch (merged into main on 2025-11-27)
- All code committed and pushed to GitHub

---

## ⚠️ WORK IN PROGRESS / PARTIALLY COMPLETE

### Telemetry Integration
- **Status:** Code structure ready, but not tested with live Azure Monitor
- **What's done:**
  - `capstone/backend/app/telemetry.py` has OpenTelemetry scaffold
  - `requirements.txt` originally included Azure Monitor exporter (removed due to dependency conflicts)
- **What's missing:**
  - Live Application Insights resource in Azure
  - Actual telemetry metrics flowing to Azure Monitor
  - Alerts configured in Application Insights
- **Next action:** Create Application Insights resource in Azure, set `APPINSIGHTS_CONNECTION_STRING` secret, verify traces appear in portal

### Azure Deployment
- **Status:** Code ready, infrastructure not deployed
- **What's done:**
  - Bicep templates fully authored (VNet, Key Vault, ACR, Container Apps, RBAC, Managed Identity)
  - GitHub Actions workflow ready to deploy
  - Deployment commands documented in `capstone/docs/GITHUB-SECRETS.md`
- **What's missing:**
  - Azure subscription & resource group created
  - Service principal credentials generated and added to GitHub Secrets
  - `az deployment group create` command executed
  - Container App image deployed and running
- **Next action:** Create Azure resources using Bicep, set GitHub Secrets, trigger CI/CD workflow

### GitHub Secrets
- **Status:** Documentation ready, secrets not yet set
- **Required secrets (from `capstone/docs/GITHUB-SECRETS.md`):**
  - `AZURE_CREDENTIALS` — Service principal JSON (create with `az ad sp create-for-rbac`)
  - `RESOURCE_GROUP` — Resource group name
  - `ACR_NAME` — Container Registry name
  - `ACR_LOGIN_SERVER` — e.g., `myregistry.azurecr.io`
  - `CONTAINERAPP_NAME` — Container App resource name
  - `CONTAINERAPP_ENVIRONMENT` — Container Apps environment name
  - `APPINSIGHTS_CONNECTION_STRING` — Application Insights connection string
  - Optional: `OPENAI_API_KEY`, `AOAI_API_KEY`, etc. for LLM providers
- **Next action:** Set secrets via GitHub UI (Settings → Secrets → Actions) or `gh secret set` commands

---

## ❌ NOT STARTED

### Advanced Telemetry & Monitoring
- Application Insights dashboards
- Custom alerts (error rate > X%, latency > X ms)
- Log Analytics KQL queries
- Distributed tracing visualization

### Production Hardening
- Load testing
- Security scanning (container image, code)
- Network security groups (NSG) rules
- WAF (Web Application Firewall) policies
- Backup & disaster recovery procedures

### Advanced CI/CD
- Multi-region deployment
- Blue-green deployments
- Automated rollback based on Application Insights metrics
- Dependency scanning and SCA (Software Composition Analysis)

---

## HOW TO CONTINUE

### Phase 1: Azure Deployment (Next Steps)
1. **Create service principal:**
   ```powershell
   az ad sp create-for-rbac --name "gh-actions-sp" --role Contributor --scopes /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP> --sdk-auth > azure-credentials.json
   ```

2. **Set GitHub Secrets:**
   - Open GitHub repo → Settings → Secrets → Actions
   - Or use `gh secret set` commands (see `capstone/docs/GITHUB-SECRETS.md`)
   - Upload `azure-credentials.json` as `AZURE_CREDENTIALS`

3. **Deploy Bicep infrastructure:**
   ```powershell
   az deployment group create `
     --template-file capstone/infra/main.bicep `
     --parameters capstone/infra/parameters.dev.json `
     -g <resource-group> `
     -l <location>
   ```

4. **Verify resources created** in Azure portal (VNet, Key Vault, ACR, Container Apps)

### Phase 2: CI/CD Validation
1. **Trigger workflow manually:**
   ```powershell
   gh workflow run ci-cd.yml --ref main
   ```

2. **Monitor workflow in GitHub Actions** — verify build, push, deploy, canary, smoke test, promote steps

3. **Test Container App endpoint:**
   ```powershell
   curl https://<containerapp-fqdn>/health
   ```

### Phase 3: Telemetry & Monitoring
1. **Create Application Insights resource** (if not created by Bicep)

2. **Set `APPINSIGHTS_CONNECTION_STRING` GitHub secret**

3. **Redeploy Container App** with secret:
   ```powershell
   az containerapp update `
     --name <containerapp-name> `
     --resource-group <resource-group> `
     --set-env-vars APPINSIGHTS_CONNECTION_STRING='<connection-string>'
   ```

4. **Generate telemetry traffic** and verify traces in Application Insights portal

5. **Configure alerts** (error rate, latency, etc.)

---

## KEY FILES REFERENCE

| File | Purpose |
|------|---------|
| `capstone/backend/app/main.py` | FastAPI entrypoint |
| `capstone/backend/app/routes.py` | API endpoints |
| `capstone/backend/app/ai_adapter.py` | LLM adapter pattern |
| `capstone/infra/main.bicep` | Main Bicep orchestration |
| `capstone/infra/parameters.dev.json` | Development parameters |
| `.github/workflows/ci-cd.yml` | GitHub Actions workflow |
| `capstone/docs/TELEMETRY.md` | Telemetry setup guide |
| `capstone/docs/GITHUB-SECRETS.md` | Secrets configuration |
| `README.md` | Project overview & quick start |

---

## ENVIRONMENT DETAILS

- **Local dev directory:** `C:\Users\jaana\capstone`
- **Git remote:** `https://github.com/Jaanayl/capstone`
- **Current branch:** `main` (on 2025-11-27)
- **Python version:** 3.11.9
- **Local testing:** `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
- **Verified working:** Health endpoint returns `{"status":"ok"}`

---

## NOTES FOR CONTINUATION

1. **Azure Credentials:** Required to deploy Bicep templates and run CI/CD. Follow Phase 1 setup above.
2. **No OpenTelemetry in local requirements.txt:** Removed due to dependency conflicts. Can be re-added when deploying to Azure if needed.
3. **Canary traffic:** Set to 10% by default in workflow. Adjust in `.github/workflows/ci-cd.yml` if needed.
4. **Image tagging:** Uses commit SHA instead of `latest` for production safety.
5. **Cost note:** Azure resources (VNet, Key Vault, Container Apps, Log Analytics) incur costs — delete or pause if not in use.

---

**Status Last Updated:** 2025-11-27 23:30 UTC  
**Next Checkpoint:** Complete Phase 1 (Azure Deployment) and verify resources are created
