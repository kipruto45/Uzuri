<#
Setup script for the frontend.

What it does:
- Detects `node` and `npm`.
- If missing, attempts to install Node.js LTS using `winget`.
- Runs `npm install` inside the `frontend` folder.
- Starts the dev server in a new PowerShell window (unless -NoStart is passed).

Usage (run from repository root or the frontend folder):
  # from repo root
  powershell -ExecutionPolicy Bypass -File .\frontend\setup-node-and-run.ps1

  # don't open the dev server after install
  powershell -ExecutionPolicy Bypass -File .\frontend\setup-node-and-run.ps1 -NoStart
#>

param(
  [switch]$NoStart,
  [string]$FrontendDir = "${PSScriptRoot}\..\frontend"
)

function Test-CommandExists {
  param([string]$cmd)
  try {
    $proc = Start-Process -FilePath $cmd -ArgumentList "--version" -NoNewWindow -RedirectStandardOutput "$env:TEMP\$($cmd)-ver.txt" -PassThru -ErrorAction Stop
    $proc.WaitForExit()
    $out = Get-Content "$env:TEMP\$($cmd)-ver.txt" -ErrorAction SilentlyContinue
    if ($out) { return $true }
    return $false
  } catch {
    return $false
  }
}

Write-Host "== Uzuri frontend setup helper =="
Write-Host "Checking for node and npm..."

$nodeExists = Test-CommandExists -cmd "node"
$npmExists = Test-CommandExists -cmd "npm"

if ($nodeExists -and $npmExists) {
  Write-Host "Node and npm detected."
} else {
  Write-Host "Node/npm not found. Attempting to install Node.js LTS using winget..."
  if (-not (Test-CommandExists -cmd "winget")) {
    Write-Host "winget not found. Please install Node.js manually from https://nodejs.org/ or install winget. Exiting." -ForegroundColor Red
    exit 2
  }

  Write-Host "Running: winget install OpenJS.NodeJS.LTS -e --source winget"
  try {
    # Run winget and wait. Don't force elevation here; winget will prompt if necessary.
    $args = 'install','OpenJS.NodeJS.LTS','-e','--source','winget'
    $p = Start-Process -FilePath winget -ArgumentList $args -NoNewWindow -Wait -PassThru -ErrorAction Stop
    Write-Host "winget finished with exit code $($p.ExitCode)"
  } catch {
    Write-Host "winget install failed: $_" -ForegroundColor Red
    Write-Host "Please install Node.js LTS manually and re-run this script. Exiting."
    exit 3
  }

  # Re-check
  Start-Sleep -Seconds 2
  $nodeExists = Test-CommandExists -cmd "node"
  $npmExists = Test-CommandExists -cmd "npm"
  if (-not ($nodeExists -and $npmExists)) {
    Write-Host "Node/npm still not available. You may need to open a new terminal or sign out/in. Please open a new PowerShell and re-run this script." -ForegroundColor Yellow
    exit 4
  }
}

# Change to frontend directory and run npm install
$frontendPath = Resolve-Path -Path $FrontendDir -ErrorAction SilentlyContinue
if (-not $frontendPath) {
  # Try relative
  $candidate = Join-Path -Path (Get-Location) -ChildPath "frontend"
  if (Test-Path $candidate) { $frontendPath = Resolve-Path $candidate }
}

if (-not $frontendPath) {
  Write-Host "Cannot find frontend directory at $FrontendDir. Please run this script from the repository root or pass -FrontendDir." -ForegroundColor Red
  exit 5
}

$frontendPath = $frontendPath.Path
Write-Host "Changing to frontend directory: $frontendPath"
Push-Location $frontendPath

Write-Host "Running npm install... (this may take a minute)"
$ni = Start-Process -FilePath npm -ArgumentList 'install' -NoNewWindow -Wait -PassThru -ErrorAction Stop
if ($ni.ExitCode -ne 0) {
  Write-Host "npm install failed with exit code $($ni.ExitCode)." -ForegroundColor Red
  Pop-Location
  exit 6
}
Write-Host "npm install completed."

if (-not $NoStart) {
  Write-Host "Starting dev server in a new PowerShell window..."
  $startCmd = "cd `"$frontendPath`"; npm run dev"
  Start-Process -FilePath powershell -ArgumentList "-NoExit","-Command",$startCmd
  Write-Host "Dev server started in a new window. If it didn't launch, run `npm run dev` in $frontendPath manually." -ForegroundColor Green
} else {
  Write-Host "Skipping starting dev server (NoStart supplied). You can run 'npm run dev' in $frontendPath." -ForegroundColor Yellow
}

Pop-Location
Write-Host "Done."
exit 0
