// ---------------------------------------------------------------------------
// Azure AI Services (Foundry Account) + Project + Model Deployments
// ---------------------------------------------------------------------------

@description('Location for the AI Services resource')
param location string

@description('Tags to apply to all resources')
param tags object

@description('Name for the Azure AI Services account')
param aiServicesName string

@description('Name for the Foundry project')
param projectName string

@description('Application Insights resource ID for project telemetry')
param applicationInsightsId string

@description('Application Insights connection string for project telemetry')
param applicationInsightsConnectionString string

// Model deployment parameters
@description('Primary model name')
param modelName string

@description('Primary model version')
param modelVersion string

@description('Primary model format')
param modelFormat string

@description('Primary model SKU')
param modelSkuName string

@description('Primary model capacity (TPM in thousands)')
param modelCapacity int

@description('Whether to deploy a second model for comparison')
param deploySecondModel bool

@description('Second model name')
param secondModelName string

@description('Second model version')
param secondModelVersion string

@description('Second model capacity')
param secondModelCapacity int

// ---------------------------------------------------------------------------
// Azure AI Services Account (Foundry) — new Foundry pattern
// ---------------------------------------------------------------------------
resource aiServices 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: aiServicesName
  location: location
  tags: tags
  kind: 'AIServices'
  sku: {
    name: 'S0'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    allowProjectManagement: true
    customSubDomainName: aiServicesName
    networkAcls: {
      defaultAction: 'Allow'
      virtualNetworkRules: []
      ipRules: []
    }
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: false
  }
}

// ---------------------------------------------------------------------------
// Foundry Project — with SystemAssigned identity
// ---------------------------------------------------------------------------
resource project 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' = {
  parent: aiServices
  name: projectName
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    description: 'ILL335 - Building & Deploying AI Agents with Microsoft Foundry'
    displayName: projectName
  }
}

// ---------------------------------------------------------------------------
// Application Insights Connection on the Project
// ---------------------------------------------------------------------------
resource appInsightsConnection 'Microsoft.CognitiveServices/accounts/projects/connections@2025-04-01-preview' = {
  parent: project
  name: 'appi-connection'
  properties: {
    category: 'AppInsights'
    target: applicationInsightsId
    authType: 'ApiKey'
    isSharedToAll: true
    credentials: {
      key: applicationInsightsConnectionString
    }
    metadata: {
      ApiType: 'Azure'
      ResourceId: applicationInsightsId
    }
  }
}

// ---------------------------------------------------------------------------
// Primary Model Deployment (e.g., gpt-5.4-mini)
// ---------------------------------------------------------------------------
resource modelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = {
  parent: aiServices
  name: modelName
  sku: {
    name: modelSkuName
    capacity: modelCapacity
  }
  properties: {
    model: {
      format: modelFormat
      name: modelName
      version: modelVersion
    }
    raiPolicyName: 'Microsoft.DefaultV2'
  }
}

// ---------------------------------------------------------------------------
// Secondary Model Deployment (e.g., gpt-5.4) — Optional
// ---------------------------------------------------------------------------
resource secondModelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = if (deploySecondModel) {
  parent: aiServices
  name: secondModelName
  sku: {
    name: modelSkuName
    capacity: secondModelCapacity
  }
  properties: {
    model: {
      format: modelFormat
      name: secondModelName
      version: secondModelVersion
    }
    raiPolicyName: 'Microsoft.DefaultV2'
  }
  dependsOn: [
    modelDeployment
  ]
}

// ---------------------------------------------------------------------------
// Outputs
// ---------------------------------------------------------------------------
output aiServicesName string = aiServices.name
output aiServicesEndpoint string = aiServices.properties.endpoint
output projectName string = project.name
output projectId string = project.id
output projectEndpoint string = project.properties.endpoints['AI Foundry API']
output projectPrincipalId string = project.identity.principalId
