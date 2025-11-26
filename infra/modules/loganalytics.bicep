param location string
param prefix string

resource la 'Microsoft.OperationalInsights/workspaces@2021-06-01' = {
  name: '${prefix}-law'
  location: location
  properties: {
    sku: { name: 'PerGB2018' }
    retentionInDays: 30
  }
}

output workspaceId string = la.id
