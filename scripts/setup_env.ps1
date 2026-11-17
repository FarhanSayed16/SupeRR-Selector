# PressurePulse Environment Setup Script
Write-Host "=== Setting up PressurePulse Environment ===" -ForegroundColor Magenta

# Check Python
$pythonVersion = python --version 2>&1
Write-Host "Python detected: $pythonVersion" -ForegroundColor Cyan

# Install Python requirements
Write-Host "Installing/Verifying Python dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt

# Check Node & npm
$nodeVersion = node --version 2>&1
$npmVersion = npm --version 2>&1
Write-Host "Node.js detected: $nodeVersion" -ForegroundColor Cyan
Write-Host "npm detected: $npmVersion" -ForegroundColor Cyan

# Setup Dashboard
if (Test-Path "dashboard/package.json") {
    Write-Host "Installing dashboard frontend dependencies..." -ForegroundColor Cyan
    Push-Location dashboard
    npm install
    Pop-Location
}

Write-Host "=== Environment Setup Complete ===" -ForegroundColor Green
