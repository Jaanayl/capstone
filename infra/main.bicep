// Infra main template - kutsuu moduuleja
param location string = resourceGroup().location
param prefix string = 'capstone'
param vnetAddressPrefix string = '10.0.0.0/16'
param appsSubnetPrefix string = '10.0.1.0/24'
param privatelinkSubnetPrefix string = '10.0.2.0/24'

module vnet 'modules/vnet.bicep' = {
  name: '${prefix}-vnet'
  params: {
    location: location
    prefix: prefix
    vnetAddressPrefix: vnetAddressPrefix
    appsSubnetPrefix: appsSubnetPrefix
    privatelinkSubnetPrefix: privatelinkSubnetPrefix
  }
}

module log 'modules/loganalytics.bicep' = {
  name: '${prefix}-log'
  params: {
    location: location
    prefix: prefix
  }
}

module kv 'modules/keyvault.bicep' = {
  name: '${prefix}-kv'
  params: {
    location: location
    prefix: prefix
  }
}

module acr 'modules/containerregistry.bicep' = {
  name: '${prefix}-acr'
  params: {
    location: location
    prefix: prefix
  }
}

module cae 'modules/containerapp_env.bicep' = {
  name: '${prefix}-cae'
  params: {
    location: location
    prefix: prefix
  }
}

// containerapp module deploys the app and wiring to ACR/CA env
module ca 'modules/containerapp.bicep' = {
  name: '${prefix}-app'
  params: {
    location: location
    prefix: prefix
    containerRegistryName: acr.outputs.acrName
    containerAppEnvName: cae.outputs.environmentName
  }
}
