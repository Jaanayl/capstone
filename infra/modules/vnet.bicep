param location string
param prefix string
param vnetAddressPrefix string
param appsSubnetPrefix string
param privatelinkSubnetPrefix string

resource vnet 'Microsoft.Network/virtualNetworks@2021-05-01' = {
  name: '${prefix}-vnet'
  location: location
  properties: {
    addressSpace: { addressPrefixes: [vnetAddressPrefix] }
    subnets: [
      { name: 'apps'; properties: { addressPrefix: appsSubnetPrefix } }
      { name: 'privatelink'; properties: { addressPrefix: privatelinkSubnetPrefix } }
    ]
  }
}

output vnetId string = vnet.id
