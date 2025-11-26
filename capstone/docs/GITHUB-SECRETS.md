# GitHub Secrets & Commands

List of recommended repository secrets (names used by CI/CD workflow and app):
- `AZURE_CREDENTIALS` — Service principal JSON for `az login` used by GitHub Actions (preferred single secret).
- `AZURE_SUBSCRIPTION_ID` — Azure subscription id (optional if included in `AZURE_CREDENTIALS`).
- `RESOURCE_GROUP` — Resource group name used by infra deploy.
- `LOCATION` — Azure region.
- `ACR_NAME` — Azure Container Registry name.
- `ACR_LOGIN_SERVER` — e.g. `myregistry.azurecr.io`.
- `ACR_USERNAME` / `ACR_PASSWORD` — optional if pipeline uses `az acr login`.
- `CONTAINERAPP_ENVIRONMENT` — Container Apps environment name.
- `CONTAINERAPP_NAME` — Container App resource name.
- `APPINSIGHTS_CONNECTION_STRING` — Application Insights connection string.
- LLM keys:
  - `OPENAI_API_KEY` or `AOAI_API_KEY` / `AOAI_ENDPOINT` / `OPENROUTER_API_KEY` as required by your AI provider.

Examples — set secrets using GitHub CLI (PowerShell)

Set AZURE_CREDENTIALS from file azure-credentials.json:

```powershell
$az = Get-Content .\azure-credentials.json -Raw
gh secret set AZURE_CREDENTIALS --body "$az"
```

Set Application Insights connection string:

```powershell
gh secret set APPINSIGHTS_CONNECTION_STRING --body "InstrumentationKey=YOUR_KEY;IngestionEndpoint=https://<region>.api.applicationinsights.azure.com/"
```

Set ACR and container app names:

```powershell
gh secret set ACR_LOGIN_SERVER --body "myregistry.azurecr.io"
gh secret set ACR_NAME --body "myregistry"
gh secret set CONTAINERAPP_NAME --body "my-container-app"
gh secret set CONTAINERAPP_ENVIRONMENT --body "my-containerapps-env"
```

Notes and tips
- `AZURE_CREDENTIALS` is recommended: create a service principal with:
  ```
  az ad sp create-for-rbac --name "gh-actions-sp" --role Contributor --scopes /subscriptions/<sub-id>/resourceGroups/<rg>
  ```
  Save the JSON output to `azure-credentials.json` and upload with `gh secret set AZURE_CREDENTIALS --body "$az"`.

- Alternatively use GitHub UI: Settings → Secrets → Actions → New repository secret.

Verify workflow run (manual trigger)
- After secrets are set and branch is pushed, trigger the GitHub Actions workflow via UI: Actions → workflow → Run workflow → choose branch & inputs.
- Or via `gh`:
  ```powershell
  gh workflow run ci-cd.yml --ref feature/m5-capstone
  ```
