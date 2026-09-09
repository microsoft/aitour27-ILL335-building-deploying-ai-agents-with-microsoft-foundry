# ======================================
# ILL335 azd and Foundry provider install
# ======================================
$ErrorActionPreference = "Stop"

function Get-LogPath {
    param([string]$Name)
    $desktop = [Environment]::GetFolderPath("Desktop")
    if ($desktop -and (Test-Path $desktop)) { return Join-Path $desktop $Name }
    return Join-Path $env:TEMP $Name
}

$logPath = Get-LogPath "azd-install.log"
Start-Transcript -Path $logPath -Force | Out-Null

function Log($m){ Write-Host "$(Get-Date -Format o) $m" }

function Download-AZD {
    param([string]$InstallerPath)

    for ($i = 1; $i -le 10; $i++) {
        try {
            Log ("Attempt {0}: Downloading AZD installer" -f $i)

            Invoke-RestMethod https://aka.ms/install-azd.ps1 `
                -OutFile $InstallerPath `
                -ErrorAction Stop

            return
        }
        catch {
            Log ("Attempt {0} failed: {1}" -f $i, $_.Exception.Message)
            Start-Sleep 10
        }
    }

    throw "Failed to download AZD installer after retries"
}

try {
    Log "Starting azd installation"

    $script = Join-Path $env:TEMP "install-azd.ps1"
    Download-AZD -InstallerPath $script

    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $script -InstallFolder "C:\utils\azd"

    if ($LASTEXITCODE -ne 0) {
        throw "AZD installer failed"
    }

    $env:PATH += ";C:\utils\azd\bin"

    # Wait for azd to be usable.
    $azdAvailable = $false
    for ($i = 1; $i -le 10; $i++) {
        cmd /c azd version > $null 2>&1
        if ($LASTEXITCODE -eq 0) {
            $azdAvailable = $true
            break
        }
        Start-Sleep 5
    }
    if (-not $azdAvailable) { throw "azd not available after install" }

    $versionOutput = (& azd version 2>&1 | Out-String)
    if ($versionOutput -notmatch '(\d+\.\d+\.\d+)') {
        throw "Could not determine azd version from: $versionOutput"
    }
    $azdVersion = [version]$Matches[1]
    if ($azdVersion -lt [version]"1.27.1") {
        throw "azd 1.27.1 or later is required; installed version is $azdVersion"
    }
    Log "azd $azdVersion available"

    Log "Installing microsoft.foundry provider bundle"
    & azd ext install microsoft.foundry
    if ($LASTEXITCODE -ne 0) {
        throw "microsoft.foundry extension installation failed"
    }

    Log "azd and microsoft.foundry installation complete"
}
catch {
    Log "ERROR: $($_.Exception.Message)"
    throw
}
finally {
    Stop-Transcript | Out-Null
}