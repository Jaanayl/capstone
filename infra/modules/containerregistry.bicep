param location string
param prefix string

resource acr 'Microsoft.ContainerRegistry/registries@2021-06-01-preview' = {
  name: '${prefix}acr'
  location: location
  sku: { name: 'Standard' }
  properties: {}
}

output acrName string = acr.name
