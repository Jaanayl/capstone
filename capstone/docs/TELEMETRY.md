# Telemetry Setup

This document shows how to enable Application Insights (Azure Monitor) for the backend and how to test telemetry locally.

Overview
- The backend reads `APPINSIGHTS_CONNECTION_STRING` (recommended) and uses the Azure Monitor OpenTelemetry exporter when present.
- If the connection string is not set, the code falls back to OTLP or console exporters (see `capstone/backend/app/telemetry.py`).

Required environment variables
- `APPINSIGHTS_CONNECTION_STRING` — Application Insights connection string (InstrumentationKey.../modern connection string).
- `OTEL_EXPORTER_OTLP_ENDPOINT` (optional) — OTLP collector endpoint, if you prefer a custom collector.

Local testing (PowerShell)
- Temporarily set the connection string and run the app locally:

  $env:APPINSIGHTS_CONNECTION_STRING = "InstrumentationKey=YOUR_KEY_HERE;IngestionEndpoint=https://<region>.api.applicationinsights.azure.com/"
  cd capstone/backend
  docker-compose up --build

- Visit `http://localhost:8000/health` and call `POST /ai/summarize` to generate traces and logs.

How the code uses the variable
- `capstone/backend/app/telemetry.py` initializes the Azure Monitor exporter when `APPINSIGHTS_CONNECTION_STRING` is set. No code change required beyond providing the environment variable.

Troubleshooting
- If you do not see telemetry:
  - Confirm the connection string is correct.
  - Confirm the container/process has the env var set.
  - Check app logs for exporter initialization warnings.

Next steps (recommended)
- Create an Application Insights resource and capture its connection string into `APPINSIGHTS_CONNECTION_STRING`.
- Add alerts (error rate, latency) in Azure Monitor and connect to runbook/email/Teams.
- Optionally deploy a Log Analytics workspace for advanced diagnostics and queries.
