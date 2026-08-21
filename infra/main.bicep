targetScope = 'subscription'

// ---------------------------------------------------------------------------
// Parameters
// ---------------------------------------------------------------------------
@minLength(1)
@maxLength(64)
@description('Name of the environment (used to generate resource names)')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string

@description('Resource group name supplied by the Microsoft Foundry provider')
param resourceGroupName string

@description('Foundry project name supplied by the Microsoft Foundry provider')
param foundryProjectName string

@description('Salt supplied by the Microsoft Foundry provider for deterministic resource names')
param resourceTokenSalt string

@description('Tags supplied by the Microsoft Foundry provider')
param tags object

@description('Name of the model to deploy')
param modelName string = 'gpt-5.4-mini'

@description('Version of the model to deploy')
param modelVersion string = '2026-03-17'

@description('Model format (OpenAI for GPT models)')
param modelFormat string = 'OpenAI'

@description('SKU name for the model deployment')
param modelSkuName string = 'GlobalStandard'

@description('Capacity (tokens-per-minute in thousands) for the model')
param modelCapacity int = 10

@description('Optional: deploy a second model for comparison lab')
param deploySecondModel string = 'false'

@description('Second model name (for comparison lab)')
param secondModelName string = 'gpt-5.4'

@description('Second model version')
param secondModelVersion string = '2026-03-05'

@description('Second model capacity')
param secondModelCapacity int = 10

@description('Id of the user or app to assign application roles')
param principalId string = ''

@description('Type of the principal referenced by principalId (User, ServicePrincipal, or Group)')
@allowed([
  'User'
  'ServicePrincipal'
  'Group'
])
param principalType string = 'User'

// ---------------------------------------------------------------------------
// Variables
// ---------------------------------------------------------------------------
var abbrs = loadJsonContent('./abbreviations.json')
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location, resourceTokenSalt))
var shouldDeploySecondModel = toLower(deploySecondModel) == 'true'
var resourceTags = union(tags, {
  'azd-env-name': environmentName
  session: 'ill335'
})

// ---------------------------------------------------------------------------
// Resource Group
// ---------------------------------------------------------------------------
resource rg 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: resourceGroupName
  location: location
  tags: resourceTags
}

// ---------------------------------------------------------------------------
// Monitoring (Log Analytics + Application Insights)
// ---------------------------------------------------------------------------
module monitoring './modules/monitoring.bicep' = {
  name: 'monitoring'
  scope: rg
  params: {
    location: location
    tags: resourceTags
    logAnalyticsName: '${abbrs.operationalInsightsWorkspaces}${resourceToken}'
    applicationInsightsName: '${abbrs.insightsComponents}${resourceToken}'
  }
}

// ---------------------------------------------------------------------------
// Azure AI Services (Foundry Account) + Project + Model Deployment
// ---------------------------------------------------------------------------
module aiServices './modules/ai-services.bicep' = {
  name: 'ai-services'
  scope: rg
  params: {
    location: location
    tags: resourceTags
    aiServicesName: '${abbrs.cognitiveServicesAccounts}${resourceToken}'
    projectName: foundryProjectName
    applicationInsightsId: monitoring.outputs.applicationInsightsId
    applicationInsightsConnectionString: monitoring.outputs.applicationInsightsConnectionString
    modelName: modelName
    modelVersion: modelVersion
    modelFormat: modelFormat
    modelSkuName: modelSkuName
    modelCapacity: modelCapacity
    deploySecondModel: shouldDeploySecondModel
    secondModelName: secondModelName
    secondModelVersion: secondModelVersion
    secondModelCapacity: secondModelCapacity
  }
}

// ---------------------------------------------------------------------------
// Role Assignments (for the signed-in user)
// ---------------------------------------------------------------------------
module roleAssignments './modules/role-assignments.bicep' = if (!empty(principalId)) {
  name: 'role-assignments'
  scope: rg
  params: {
    principalId: principalId
    principalType: principalType
    aiServicesName: aiServices.outputs.aiServicesName
  }
}

// ---------------------------------------------------------------------------
// Outputs (consumed by azd env get-values)
// ---------------------------------------------------------------------------
output AZURE_RESOURCE_GROUP string = rg.name
output AZURE_AI_SERVICES_NAME string = aiServices.outputs.aiServicesName
output AZURE_AI_PROJECT_NAME string = aiServices.outputs.projectName
output AZURE_AI_PROJECT_ID string = aiServices.outputs.projectId
output AZURE_AI_PROJECT_ENDPOINT string = aiServices.outputs.projectEndpoint
output FOUNDRY_PROJECT_ENDPOINT string = aiServices.outputs.projectEndpoint
output AZURE_APPLICATION_INSIGHTS_NAME string = monitoring.outputs.applicationInsightsName
output MODEL_DEPLOYMENT_NAME string = modelName
output MODEL_DEPLOYMENT_NAME_2 string = shouldDeploySecondModel ? secondModelName : ''
