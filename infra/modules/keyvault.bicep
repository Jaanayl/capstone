param location string
param prefix string

resource kv 'Microsoft.KeyVault/vaults@2021-10-01' = {
  name: '${prefix}-kv'
  location: location
  properties: {
    tenantId: subscription().tenantId
    sku: { family: 'A'; name: 'standard' }
    accessPolicies: []
    enabledForDeployment: false
    enablePurgeProtection: false
  }
}

output keyVaultName string = kv.name
