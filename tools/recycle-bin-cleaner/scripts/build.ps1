param(
    [switch]$Clean
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ToolRoot = Resolve-Path (Join-Path $ScriptDir "..")
$DistDir = Join-Path $ToolRoot "dist"
$VenvDir = Join-Path $ToolRoot ".venv"

if ($Clean) {
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue (Join-Path $ToolRoot "build")
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $DistDir
}

if (-not (Test-Path $VenvDir)) {
    python -m venv $VenvDir
    if ($LASTEXITCODE -ne 0) { throw "Failed to create virtual environment." }
}

$Py = Join-Path $VenvDir "Scripts\python.exe"

& $Py -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw "Failed to upgrade pip." }

& $Py -m pip install -e $ToolRoot
if ($LASTEXITCODE -ne 0) { throw "Failed to install package in editable mode." }

& $Py -m pip install -r (Join-Path $ToolRoot "requirements-dev.txt")
if ($LASTEXITCODE -ne 0) { throw "Failed to install dev dependencies." }

& $Py -m PyInstaller --noconfirm --clean --windowed --onefile `
  --name RecycleBinCleaner `
  --paths (Join-Path $ToolRoot "src") `
  (Join-Path $ToolRoot "src\recycle_bin_cleaner\__main__.py")
if ($LASTEXITCODE -ne 0) { throw "PyInstaller build failed." }

if (-not (Test-Path (Join-Path $DistDir "RecycleBinCleaner.exe"))) {
    throw "Build completed without RecycleBinCleaner.exe output."
}

Write-Host "Build complete: $(Join-Path $DistDir 'RecycleBinCleaner.exe')"
