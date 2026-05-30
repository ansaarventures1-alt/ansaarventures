# LLM Auto-Installer for Windows (PowerShell)
# This script automatically installs Ollama and downloads all major free LLMs

param(
    [string]$ModelPath = "$env:USERPROFILE\.ollama\models",
    [switch]$SkipOllama = $false,
    [switch]$SkipModels = $false
)

# Colors for output
$InfoColor = "Cyan"
$SuccessColor = "Green"
$ErrorColor = "Red"
$WarningColor = "Yellow"

Write-Host "╔════════════════════════════════════════╗" -ForegroundColor $InfoColor
Write-Host "║   Free LLM Auto-Installer for Windows  ║" -ForegroundColor $InfoColor
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor $InfoColor
Write-Host ""

# Check if running as admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "⚠️  This script is not running as Administrator." -ForegroundColor $WarningColor
    Write-Host "Some features may not work. Run PowerShell as Administrator for best results." -ForegroundColor $WarningColor
    Write-Host ""
}

# Step 1: Check and install Ollama
if (-not $SkipOllama) {
    Write-Host "Step 1: Installing Ollama..." -ForegroundColor $InfoColor
    
    $ollamaPath = "C:\Program Files\Ollama\ollama.exe"
    
    if (Test-Path $ollamaPath) {
        Write-Host "✓ Ollama is already installed" -ForegroundColor $SuccessColor
    } else {
        Write-Host "Downloading Ollama for Windows..." -ForegroundColor $InfoColor
        
        $ollamaUrl = "https://ollama.ai/download/windows"
        $installerPath = "$env:TEMP\OllamaSetup.exe"
        
        try {
            # Download Ollama installer
            Invoke-WebRequest -Uri $ollamaUrl -OutFile $installerPath -UseBasicParsing
            Write-Host "✓ Downloaded Ollama installer" -ForegroundColor $SuccessColor
            
            # Run installer
            Write-Host "Running Ollama installer (this may take a few minutes)..." -ForegroundColor $InfoColor
            Start-Process -FilePath $installerPath -Wait
            
            # Verify installation
            if (Test-Path $ollamaPath) {
                Write-Host "✓ Ollama installed successfully" -ForegroundColor $SuccessColor
            } else {
                Write-Host "✗ Ollama installation failed" -ForegroundColor $ErrorColor
                exit 1
            }
            
            # Clean up installer
            Remove-Item $installerPath -Force -ErrorAction SilentlyContinue
        } catch {
            Write-Host "✗ Error downloading Ollama: $_" -ForegroundColor $ErrorColor
            Write-Host "Please download manually from: https://ollama.ai/download" -ForegroundColor $WarningColor
            exit 1
        }
    }
}

Write-Host ""

# Step 2: Download LLMs
if (-not $SkipModels) {
    Write-Host "Step 2: Downloading LLM Models..." -ForegroundColor $InfoColor
    Write-Host "This may take 30+ minutes depending on your internet speed" -ForegroundColor $WarningColor
    Write-Host ""
    
    # Ensure Ollama is in PATH
    $env:Path += ";C:\Program Files\Ollama"
    
    # List of models to download
    $models = @(
        @{ name = "llama2"; display = "Llama 2 (7B)" },
        @{ name = "mistral"; display = "Mistral (7B)" },
        @{ name = "phi"; display = "Phi-3 Mini (3.8B)" },
        @{ name = "gemma:7b"; display = "Gemma (7B)" },
        @{ name = "neural-chat"; display = "Neural Chat (7B)" }
    )
    
    $successCount = 0
    $failureCount = 0
    
    foreach ($model in $models) {
        Write-Host "Downloading: $($model.display)" -ForegroundColor $InfoColor
        
        try {
            # Pull the model using Ollama
            & ollama pull $model.name
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✓ Successfully installed $($model.display)" -ForegroundColor $SuccessColor
                $successCount++
            } else {
                Write-Host "✗ Failed to install $($model.display)" -ForegroundColor $ErrorColor
                $failureCount++
            }
        } catch {
            Write-Host "✗ Error installing $($model.display): $_" -ForegroundColor $ErrorColor
            $failureCount++
        }
        
        Write-Host ""
    }
    
    # Summary
    Write-Host "════════════════════════════════════════" -ForegroundColor $InfoColor
    Write-Host "Download Summary:" -ForegroundColor $InfoColor
    Write-Host "  ✓ Successful: $successCount" -ForegroundColor $SuccessColor
    Write-Host "  ✗ Failed: $failureCount" -ForegroundColor $(if ($failureCount -gt 0) { $ErrorColor } else { $InfoColor })
    Write-Host "════════════════════════════════════════" -ForegroundColor $InfoColor
}

Write-Host ""
Write-Host "✅ Installation Complete!" -ForegroundColor $SuccessColor
Write-Host ""
Write-Host "🚀 Next Steps:" -ForegroundColor $InfoColor
Write-Host "1. Open PowerShell or Command Prompt" -ForegroundColor $InfoColor
Write-Host "2. Run any model with: ollama run llama2" -ForegroundColor $InfoColor
Write-Host "3. Or start the API server: ollama serve" -ForegroundColor $InfoColor
Write-Host ""
Write-Host "📚 For more info, visit: https://ollama.ai" -ForegroundColor $InfoColor
Write-Host "💾 Models stored in: $ModelPath" -ForegroundColor $InfoColor
Write-Host ""

# Option to run a model now
$runNow = Read-Host "Would you like to run a model now? (y/n)"
if ($runNow -eq "y" -or $runNow -eq "Y") {
    Write-Host ""
    Write-Host "Available models:" -ForegroundColor $InfoColor
    Write-Host "1. llama2" -ForegroundColor $InfoColor
    Write-Host "2. mistral" -ForegroundColor $InfoColor
    Write-Host "3. phi" -ForegroundColor $InfoColor
    Write-Host "4. gemma:7b" -ForegroundColor $InfoColor
    Write-Host "5. neural-chat" -ForegroundColor $InfoColor
    Write-Host ""
    $choice = Read-Host "Enter model number or name (or press Enter to skip)"
    
    if ($choice) {
        Write-Host "Starting: $choice" -ForegroundColor $InfoColor
        & ollama run $choice
    }
}
