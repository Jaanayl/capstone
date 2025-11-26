# Capstone Project — Production-Ready Architecture & CI/CD

This project demonstrates a minimal production-ready Azure infrastructure with Bicep IaC, GitOps CI/CD (canary + rollback), Private Networking, RBAC/Managed Identity, and a containerized FastAPI backend with AI summarization and observability.

## Quick Start (Local Dev)

Requires: Docker, Docker Compose, Python 3.11+

```powershell
cd capstone/backend
docker-compose up --build
```

Visit `http://localhost:8000/health` and exercise `POST /ai/summarize` with a JSON body like:
```json
{"text": "Your text to summarize here."}
```

## Environment Variables

Backend service (`.env` or export in shell):
- `LLM_PROVIDER` — `mock`, `azure-openai`, `openrouter` (default: `mock`)
- `OPENAI_API_KEY` — OpenAI API key if using OpenRouter
- `AOAI_API_KEY` — Azure OpenAI API key
- `AOAI_ENDPOINT` — Azure OpenAI endpoint URL
- `APPINSIGHTS_CONNECTION_STRING` — Application Insights connection string (for telemetry)

## Telemetry & GitHub Secrets

See `capstone/docs/TELEMETRY.md` and `capstone/docs/GITHUB-SECRETS.md` for setup instructions and exact commands to enable Application Insights and configure GitHub repository secrets.

## Project Structure

```
capstone/
├── backend/                 # FastAPI application
│   ├── app/                 # Application code (main.py, routes, telemetry, AI adapter)
│   ├── tests/               # Unit tests
│   ├── Dockerfile           # Container image definition
│   ├── requirements.txt      # Python dependencies
│   └── docker-compose.yml   # Local dev services
├── infra/                   # Bicep infrastructure modules
│   ├── main.bicep           # Main orchestration template
│   ├── parameters.dev.json  # Development parameters
│   └── modules/             # Reusable modules (VNet, Key Vault, ACR, etc.)
├── docs/                    # Documentation
│   ├── architecture.md      # Architecture diagrams (Mermaid)
│   ├── TELEMETRY.md         # Telemetry setup guide
│   └── GITHUB-SECRETS.md    # GitHub secrets and commands
└── .github/workflows/       # GitHub Actions CI/CD pipeline

```

## Architecture Highlights

- **Private Networking**: Virtual Network with subnets, Private Endpoints, Private DNS zones
- **Managed Identity & RBAC**: Container App uses system-assigned identity; roles for ACR pull and Key Vault access
- **Key Vault**: Secrets management (integrated with Private Endpoint)
- **Observability**: JSON structured logging, OpenTelemetry instrumentation, Azure Monitor exporter
- **CI/CD Pipeline**: Build → Push image to ACR → Deploy with canary traffic (10%) → Smoke tests → Promote/Rollback
- **AI Feature**: Adapter pattern supporting mock, Azure OpenAI, and OpenRouter LLM providers

## Running the CI/CD Workflow

Prerequisites:
1. Set required GitHub repository secrets (see `capstone/docs/GITHUB-SECRETS.md`):
   - `AZURE_CREDENTIALS` — Service principal JSON
   - `CONTAINERAPP_NAME`, `RESOURCE_GROUP`
   - `APPINSIGHTS_CONNECTION_STRING`
   - `ACR_LOGIN_SERVER`, `ACR_NAME`, etc.

2. Manually trigger or push to `main`/`feature/m5-capstone`:
   ```powershell
   gh workflow run ci-cd.yml --ref feature/m5-capstone
   ```

## Next Steps

1. Create Azure resources using Bicep: `az deployment group create --template-file capstone/infra/main.bicep --parameters capstone/infra/parameters.dev.json -g <resource-group>`
2. Set GitHub repository secrets with your Azure and ACR credentials.
3. Run CI/CD workflow to deploy the application.
4. Monitor in Application Insights and configure alerts.

For detailed guides, see `capstone/docs/TELEMETRY.md` and `capstone/docs/GITHUB-SECRETS.md`.
