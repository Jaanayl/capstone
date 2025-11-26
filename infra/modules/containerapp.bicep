param location string
param prefix string
param containerRegistryName string
param containerAppEnvName string

// Skeleton for Container App resource. Fill image and config via parameters/CI.
resource ca 'Microsoft.App/containerApps@2022-03-01' = {
  name: '${prefix}-app'
  location: location
  properties: {
    managedEnvironmentId: resourceId('Microsoft.App/managedEnvironments', containerAppEnvName)
    configuration: {
      ingress: { external: true; targetPort: 80 }
    }
    template: {
      containers: [
        {
          name: 'backend'
          properties: { image: 'REPLACE_WITH_IMAGE', resources: { cpu: 0.25; memory: '0.5Gi' } }
        }
      ]
    }
  }
}

output containerAppName string = ca.name
