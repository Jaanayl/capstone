param location string
param prefix string

resource cae 'Microsoft.App/managedEnvironments@2022-03-01' = {
  name: '${prefix}-cae'
  location: location
  sku: { name: 'Consumption' }
}

output environmentName string = cae.name
