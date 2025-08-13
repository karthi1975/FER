# 🎭 FER Project Windows PowerShell Setup Script
# This script will create and configure your FER environment on Windows

param(
    [switch]$Force,
    [switch]$SkipTests,
    [switch]$Help
)

# Show help if requested
if ($Help) {
    Write-Host @"
🎭 FER Project Windows PowerShell Setup Script

Usage:
    .\setup_fer_windows.ps1 [options]

Options:
    -Force      Force recreation of existing environment
    -SkipTests  Skip package verification tests
    -Help       Show this help message

Examples:
    .\setup_fer_windows.ps1
    .\setup_fer_windows.ps1 -Force
    .\setup_fer_windows.ps1 -SkipTests

"@ -ForegroundColor Cyan
    exit 0
}

# Set execution policy for current session
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# Function to write colored output
function Write-Status {
    param(
        [string]$Message,
        [string]$Type = "Info"
    )
    
    switch ($Type) {
        "Success" { Write-Host "✅ $Message" -ForegroundColor Green }
        "Error"   { Write-Host "❌ $Message" -ForegroundColor Red }
        "Warning" { Write-Host "⚠️  $Message" -ForegroundColor Yellow }
        "Info"    { Write-Host "ℹ️  $Message" -ForegroundColor Blue }
        default   { Write-Host "$Message" -ForegroundColor White }
    }
}

function Write-Header {
    param([string]$Title)
    Write-Host "`n" -NoNewline
    Write-Host "=" * 60 -ForegroundColor DarkGray
    Write-Host " $Title" -ForegroundColor Cyan
    Write-Host "=" * 60 -ForegroundColor DarkGray
}

function Write-Section {
    param([string]$Title)
    Write-Host "`n" -NoNewline
    Write-Host "-" * 40 -ForegroundColor Gray
    Write-Host " $Title" -ForegroundColor Yellow
    Write-Host "-" * 40 -ForegroundColor Gray
}

# Main setup function
function Setup-FEREnvironment {
    Write-Header "🚀 FER Project Windows PowerShell Setup"
    
    # Check if running as administrator
    $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
    if ($isAdmin) {
        Write-Status "Running with administrator privileges" "Success"
    } else {
        Write-Status "Not running as administrator (this is usually fine)" "Warning"
    }
    
    Write-Section "📋 Checking Prerequisites"
    
    # Check if conda is installed
    try {
        $condaVersion = conda --version 2>$null
        if ($condaVersion) {
            Write-Status "Conda is installed: $condaVersion" "Success"
        } else {
            throw "Conda not found"
        }
    } catch {
        Write-Status "Conda is not installed or not in PATH!" "Error"
        Write-Host @"

📥 Please install Miniconda first:
   1. Download from: https://docs.conda.io/en/latest/miniconda.html
   2. Choose Windows x86_64 installer
   3. Install with default settings
   4. Restart your PowerShell/Command Prompt
   5. Or use Chocolatey: choco install miniconda3

"@ -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    # Check if Python is available
    try {
        $pythonVersion = python --version 2>$null
        if ($pythonVersion) {
            Write-Status "Python is available: $pythonVersion" "Success"
        } else {
            Write-Status "Python not in PATH (will be fixed with conda environment)" "Warning"
        }
    } catch {
        Write-Status "Python not available (will be fixed with conda environment)" "Warning"
    }
    
    Write-Section "🔧 Environment Setup"
    
    # Check if FER_ENV already exists
    $envExists = conda env list | Select-String "FER_ENV"
    if ($envExists) {
        if ($Force) {
            Write-Status "Removing existing FER_ENV environment..." "Warning"
            conda env remove -n FER_ENV -y
            if ($LASTEXITCODE -ne 0) {
                Write-Status "Failed to remove environment" "Error"
                Read-Host "Press Enter to exit"
                exit 1
            }
            Write-Status "Environment removed successfully" "Success"
        } else {
            Write-Status "FER_ENV environment already exists!" "Warning"
            $choice = Read-Host "Do you want to remove it and recreate? (y/N)"
            if ($choice -eq "y" -or $choice -eq "Y") {
                Write-Status "Removing existing FER_ENV..." "Warning"
                conda env remove -n FER_ENV -y
                if ($LASTEXITCODE -ne 0) {
                    Write-Status "Failed to remove environment" "Error"
                    Read-Host "Press Enter to exit"
                    exit 1
                }
                Write-Status "Environment removed successfully" "Success"
            } else {
                Write-Status "Using existing FER_ENV environment" "Info"
                goto :activate_environment
            }
        }
    }
    
    Write-Status "Creating FER_ENV environment..." "Info"
    
    # Try to create environment from yml file
    if (Test-Path "environment.yml") {
        Write-Status "Creating environment from environment.yml..." "Info"
        conda env create -f environment.yml
        if ($LASTEXITCODE -eq 0) {
            Write-Status "Environment created successfully from yml file!" "Success"
        } else {
            Write-Status "Failed to create environment from yml file, trying manual creation..." "Warning"
            goto :manual_creation
        }
    } else {
        Write-Status "environment.yml not found, using manual creation..." "Warning"
        goto :manual_creation
    }
    
    :manual_creation
    Write-Status "Creating environment manually..." "Info"
    
    # Create base environment
    Write-Status "Creating base environment with Python 3.9..." "Info"
    conda create -n FER_ENV python=3.9 -y
    if ($LASTEXITCODE -ne 0) {
        Write-Status "Failed to create base environment" "Error"
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    # Install core packages via conda
    Write-Status "Installing core packages via conda..." "Info"
    conda install -n FER_ENV -c conda-forge opencv numpy pillow matplotlib seaborn pandas scipy -y
    if ($LASTEXITCODE -ne 0) {
        Write-Status "Failed to install core packages, trying alternative channels..." "Warning"
        conda install -n FER_ENV opencv numpy pillow matplotlib seaborn pandas scipy -y
    }
    
    # Install AI/ML packages via pip
    Write-Status "Installing AI/ML packages via pip..." "Info"
    conda activate FER_ENV
    if ($LASTEXITCODE -ne 0) {
        Write-Status "Failed to activate environment" "Error"
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    $packages = @(
        @{Name="DeepFace"; Version="0.0.95"},
        @{Name="MediaPipe"; Version="0.10.21"},
        @{Name="Streamlit"; Version="1.48.1"},
        @{Name="TensorFlow"; Version="2.19.1"},
        @{Name="Keras"; Version="3.10.0"},
        @{Name="tf-keras"; Version="2.19.0"},
        @{Name="Scikit-learn"; Version="1.3.0"}
    )
    
    foreach ($package in $packages) {
        Write-Status "Installing $($package.Name)..." "Info"
        pip install "$($package.Name)==$($package.Version)"
        if ($LASTEXITCODE -ne 0) {
            Write-Status "Warning: Failed to install $($package.Name)" "Warning"
        }
    }
    
    :activate_environment
    Write-Status "Activating FER_ENV environment..." "Info"
    conda activate FER_ENV
    if ($LASTEXITCODE -ne 0) {
        Write-Status "Failed to activate environment" "Error"
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    Write-Status "Environment activated successfully!" "Success"
    
    if (-not $SkipTests) {
        Write-Section "🧪 Testing Installation"
        
        Write-Status "Verifying package installation..." "Info"
        
        $testPackages = @(
            @{Name="OpenCV"; Import="cv2"; Version="__version__"},
            @{Name="NumPy"; Import="numpy"; Version="__version__"},
            @{Name="DeepFace"; Import="deepface"; Version=""},
            @{Name="MediaPipe"; Import="mediapipe"; Version=""},
            @{Name="Streamlit"; Import="streamlit"; Version=""},
            @{Name="TensorFlow"; Import="tensorflow"; Version="__version__"}
        )
        
        foreach ($pkg in $testPackages) {
            try {
                if ($pkg.Version) {
                    $result = python -c "import $($pkg.Import); print('$($pkg.Import).$($pkg.Version)')" 2>$null
                    if ($result) {
                        Write-Status "$($pkg.Name): OK" "Success"
                    } else {
                        Write-Status "$($pkg.Name): Not working" "Error"
                    }
                } else {
                    $result = python -c "import $($pkg.Import); print('OK')" 2>$null
                    if ($result) {
                        Write-Status "$($pkg.Name): OK" "Success"
                    } else {
                        Write-Status "$($pkg.Name): Not working" "Error"
                    }
                }
            } catch {
                Write-Status "$($pkg.Name): Not working" "Error"
            }
        }
        
        Write-Status "Testing FER Core..." "Info"
        try {
            $result = python -c "from fer_core import FEREngine; print('OK')" 2>$null
            if ($result) {
                Write-Status "FER Engine: OK" "Success"
            } else {
                Write-Status "FER Engine: Not working (this might be normal if files are missing)" "Warning"
            }
        } catch {
            Write-Status "FER Engine: Not working (this might be normal if files are missing)" "Warning"
        }
    }
    
    Write-Header "🎉 Setup Completed Successfully!"
    
    Write-Host @"

📋 Next Steps:
    1. ✅ Environment created and activated
    2. 🔍 Test camera: python camera_permission_test.py
    3. 🎭 Run FER: python test_camera.py
    4. 🌐 Launch web app: streamlit run live_camera_app.py

💡 Quick Commands:
    conda activate FER_ENV
    python test_camera.py
    streamlit run live_camera_app.py

🔗 For more help, see:
    - CONDA_SETUP.md
    - SETUP.md
    - README.md

"@ -ForegroundColor Green
    
    Write-Header "🎭 Happy Emotion Detection! 😊"
}

# Run the setup
try {
    Setup-FEREnvironment
} catch {
    Write-Status "Setup failed with error: $($_.Exception.Message)" "Error"
    Write-Status "Please check the error and try again" "Warning"
} finally {
    Write-Host "`nPress Enter to exit..." -NoNewline
    Read-Host
}
