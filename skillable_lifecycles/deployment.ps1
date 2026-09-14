$env:PSExecutionPolicyPreference = "Bypass"

# =========================================
# ILL335 Skillable Foundry deployment
# =========================================
$logPath = "C:\Users\LabUser\Desktop\lifecycle-165767.log"
Start-Transcript -Path $logPath -Force

try {
    # === Variables ===
    $appId     = "@lab.CloudSubscription.AppId"
    $appSecret = "@lab.CloudSubscription.AppSecret"
    $tenantId  = "@lab.CloudSubscription.TenantId"
    $subId     = "@lab.CloudSubscription.Id"
    $region    = "@lab.CloudResourceGroup(ResourceGroup1).Location"
    $envName   = "build@lab.LabInstance.Id"
    $userUpn   = "@lab.CloudPortalCredential(User1).Username"

    $ErrorActionPreference = "Stop"

    # Run an external command and preserve its full output in the lifecycle log.
    function Invoke-External($label, [ScriptBlock]$cmd) {
        Write-Host ">>> $label"
        $prev = $ErrorActionPreference
        $ErrorActionPreference = "Continue"
        try {
            & $cmd 2>&1 | ForEach-Object { Write-Host $_ }
            $exitCode = $LASTEXITCODE
        } finally {
            $ErrorActionPreference = $prev
        }
        if ($exitCode -ne 0) { throw "$label failed (exit $exitCode)." }
    }

    function Get-AzdEnvValue([string[]]$names, [string]$label) {
        foreach ($name in $names) {
            $output = & azd env get-value $name -e $envName 2>&1
            $exitCode = $LASTEXITCODE
            if ($exitCode -eq 0) {
                $value = ($output | Out-String).Trim()
                if ($value) { return $value }
            }
        }

        throw "azd did not publish $label (checked: $($names -join ', '))."
    }

    function Grant-Role($principalId, $roleId, $scope, $label) {
        try {
            New-AzRoleAssignment -RoleDefinitionId $roleId -ObjectId $principalId -Scope $scope -ErrorAction Stop | Out-Null
            Write-Host "Granted $label to $principalId"
        } catch {
            if ($_.Exception.Message -match "already exists|RoleAssignmentExists|Conflict") {
                Write-Host "Skip (already exists): $label for $principalId"
            } else { throw }
        }
    }

    # Retry until a newly provisioned resource is available through ARM.
    function Invoke-WithRetry([ScriptBlock]$sb, [string]$label, [int]$maxAttempts = 12, [int]$delaySec = 15) {
        for ($i = 1; $i -le $maxAttempts; $i++) {
            try {
                $result = & $sb
                if ($result) { return $result }
                Write-Host "  $label attempt $i/${maxAttempts}: empty result, retrying in ${delaySec}s..."
            } catch {
                Write-Host "  $label attempt $i/${maxAttempts}: $($_.Exception.Message)"
                if ($i -eq $maxAttempts) { throw }
            }
            Start-Sleep -Seconds $delaySec
        }
        throw "$label did not return a result after $maxAttempts attempts."
    }

    # === Authentication ===
    Write-Host ">>> Connect-AzAccount"
    $securePwd = ConvertTo-SecureString $appSecret -AsPlainText -Force
    $psCred    = New-Object System.Management.Automation.PSCredential ($appId, $securePwd)
    Connect-AzAccount -ServicePrincipal -Tenant $tenantId -Credential $psCred -Subscription $subId -SkipContextPopulation | Out-Null

    # === Resolve lab user object ID (with retry) ===
    Write-Host ">>> Resolve user $userUpn"
    $userId  = $null
    $retries = 0
    while (-not $userId -and $retries -lt 10) {
        try { $userId = (Get-AzADUser -UserPrincipalName $userUpn -ErrorAction Stop).Id }
        catch { Write-Host "  attempt $($retries+1): $($_.Exception.Message)" }
        if (-not $userId) { Start-Sleep -Seconds 15; $retries++ }
    }
    if (-not $userId) { throw "Could not resolve user '$userUpn'." }
    Write-Host "userId = $userId"

    # === azd up ===
    $env:PATH += ";C:\utils\azd\bin"
    $env:AZD_SKIP_FIRST_RUN = "true"

    # Do not let the Skillable image's pre-created resource group override the
    # provider-managed resource group for this azd environment.
    Remove-Item Env:AZURE_RESOURCE_GROUP -ErrorAction SilentlyContinue

    $labPath = @(
        "C:\Users\LabUser\Desktop\ILL335"
    ) | Where-Object { Test-Path $_ } | Select-Object -First 1
    if (-not $labPath) {
        throw "Lab folder not found. Expected AI-Tour-ILL335-main or ILL335 on the LabUser desktop."
    }
    Set-Location $labPath

    # Prepare the interpreter used by the VS Code Agent Inspector tasks.
    $venvPython = Join-Path $labPath ".venv\Scripts\python.exe"
    if (-not (Test-Path $venvPython)) {
        Invoke-External "create Python virtual environment" {
            python -m venv (Join-Path $labPath ".venv")
        }
    }
    if (-not (Test-Path $venvPython)) {
        throw "Python virtual environment was not created at '$venvPython'."
    }
    Invoke-External "install lab Python dependencies" {
        & $venvPython -m pip install -r (Join-Path $labPath "requirements.txt")
    }
    Invoke-External "install hosted-agent Python dependencies" {
        & $venvPython -m pip install -r (Join-Path $labPath "src\agent\requirements.txt")
    }
    Invoke-External "verify Python dependencies" {
        & $venvPython -m pip check
    }

    Invoke-External "verify azd version" {
        azd version
    }
    Invoke-External "update azure.ai.agents provider" {
        azd ext update azure.ai.agents --no-prompt
    }
    Invoke-External "update azure.ai.projects provider" {
        azd ext update azure.ai.projects --no-prompt
    }
    Invoke-External "install microsoft.foundry provider bundle" {
        azd ext install microsoft.foundry --force --no-prompt
    }

    Invoke-External "azd auth login" {
        azd auth login --client-id $appId --client-secret $appSecret --tenant-id $tenantId
    }
    Invoke-External "azd env new" {
        azd env new $envName --location $region --subscription $subId
    }

    Invoke-External "configure azd tenant" {
        azd env set AZURE_TENANT_ID $tenantId -e $envName
    }
    Invoke-External "azd up" {
        azd up -e $envName --no-prompt
    }

    # === Post-deploy role assignments ===
    $foundryUserRoleId           = "53ca6127-db72-4b80-b1b0-d745d6d5456d"  # Foundry User
    $foundryProjectManagerRoleId = "eadc314b-1a2d-4efa-be10-5d325db5065e"  # Foundry Project Manager
    $openAIUserRoleId            = "5e0bd9bd-7b93-4f28-af87-19fc36ad61bd"  # Cognitive Services OpenAI User

    $azdRg = Get-AzdEnvValue @("AZURE_RESOURCE_GROUP") "the resource group"
    Write-Host "azd resource group: $azdRg"

    $aiResource = Invoke-WithRetry {
        Get-AzCognitiveServicesAccount -ResourceGroupName $azdRg -ErrorAction Stop | Select-Object -First 1
    } "Get Foundry account"
    if (-not $aiResource) { throw "No Foundry account found in RG '$azdRg'." }
    $aiResourceId = $aiResource.Id
    Write-Host "aiResourceId = $aiResourceId"

    $aiProject = Invoke-WithRetry {
        Get-AzResource `
            -ResourceType "Microsoft.CognitiveServices/accounts/projects" `
            -ResourceGroupName $azdRg -ErrorAction Stop | Select-Object -First 1
    } "Get Foundry project"
    $aiProjectId = $aiProject.ResourceId

    Grant-Role $userId $foundryUserRoleId           $aiProjectId  "Foundry User (learner)"
    Grant-Role $userId $foundryProjectManagerRoleId $aiProjectId  "Foundry Project Manager (learner)"
    Grant-Role $userId $openAIUserRoleId            $aiResourceId "Cognitive Services OpenAI User (learner)"

    # Labs 2-5 consume a local .env rendered from the repository template.
    $projectEndpoint = Get-AzdEnvValue `
        @("FOUNDRY_PROJECT_ENDPOINT", "AZURE_AI_PROJECT_ENDPOINT") `
        "the Foundry project endpoint"
    $envSamplePath = Join-Path $labPath ".env.sample"
    if (-not (Test-Path $envSamplePath)) { throw ".env.sample not found at '$envSamplePath'." }

    $envValues = @{
        PROJECT_ENDPOINT        = $projectEndpoint
        MODEL_DEPLOYMENT_NAME   = "gpt-5.4-mini"
        MODEL_DEPLOYMENT_NAME_2 = "gpt-5.4"
        AZURE_LOCATION          = $region.ToLowerInvariant()
        AZURE_PRICING_CURRENCY  = "USD"
    }
    $envContent = foreach ($line in Get-Content -Path $envSamplePath) {
        if ($line -match "^([A-Z][A-Z0-9_]+)=" -and $envValues.ContainsKey($Matches[1])) {
            "$($Matches[1])=$($envValues[$Matches[1]])"
        } else {
            $line
        }
    }
    $envContent | Set-Content -Path (Join-Path $labPath ".env") -Encoding ASCII

    Write-Host ">>> Lifecycle action complete."
}
catch {
    Write-Host "FATAL: $($_.Exception.Message)"
    Write-Host $_.ScriptStackTrace
    throw
}
finally {
    Stop-Transcript
}