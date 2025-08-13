# 🪟 Windows Setup Guide for FER Project

Complete guide to set up your FER (Face Emotion Recognition) project on Windows.

## 🚀 Quick Start Options

### Option 1: Automated Setup (Recommended)

#### **PowerShell Script (Most Features)**
```powershell
# Run PowerShell as Administrator (recommended)
# Right-click PowerShell → "Run as Administrator"

# Navigate to your FER project folder
cd C:\path\to\your\FER\project

# Run the setup script
.\setup_fer_windows.ps1

# Or with options
.\setup_fer_windows.ps1 -Force        # Force recreate environment
.\setup_fer_windows.ps1 -SkipTests    # Skip package verification
.\setup_fer_windows.ps1 -Help         # Show help
```

#### **Batch File (Standard)**
```cmd
# Run Command Prompt
# Navigate to your FER project folder
cd C:\path\to\your\FER\project

# Run the setup script
setup_fer_windows.bat
```

#### **Simple Batch File (Basic)**
```cmd
# For users who want minimal setup
setup_fer_simple.bat
```

### Option 2: Manual Setup

```cmd
# Create environment
conda create -n FER_ENV python=3.9 -y

# Activate environment
conda activate FER_ENV

# Install core packages
conda install -c conda-forge opencv numpy pillow matplotlib seaborn pandas scipy -y

# Install AI packages
pip install deepface mediapipe streamlit tensorflow keras tf-keras scikit-learn
```

## 📋 Prerequisites

### 1. Install Miniconda

#### **Download Method (Recommended)**
1. Visit: https://docs.conda.io/en/latest/miniconda.html
2. Download **Windows x86_64** installer
3. Run installer as Administrator
4. Choose **"Install for all users"** (recommended)
5. **Important**: Check "Add Miniconda3 to PATH"
6. Restart Command Prompt/PowerShell

#### **Chocolatey Method**
```cmd
# Install Chocolatey first (if not installed)
# Run PowerShell as Administrator
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Miniconda
choco install miniconda3
```

### 2. Verify Installation
```cmd
# Check conda
conda --version

# Check Python
python --version

# List conda environments
conda env list
```

## 🔧 Script Options

### PowerShell Script Features
- **Color-coded output** for better readability
- **Error handling** with detailed messages
- **Package verification** after installation
- **Command-line options** for customization
- **Administrator privilege detection**
- **Fallback installation methods**

### Batch File Features
- **Simple execution** - just double-click
- **Basic error checking**
- **User-friendly messages**
- **Automatic environment creation**

## 🎯 Step-by-Step Manual Setup

### Step 1: Open Command Prompt
```cmd
# Press Win + R, type "cmd", press Enter
# Or search "Command Prompt" in Start menu
```

### Step 2: Navigate to Project
```cmd
# Change to your FER project directory
cd C:\Users\YourUsername\Documents\FER
# or wherever you downloaded the project
```

### Step 3: Create Environment
```cmd
# Create new environment
conda create -n FER_ENV python=3.9 -y

# Activate environment
conda activate FER_ENV
```

### Step 4: Install Packages
```cmd
# Install core packages via conda
conda install -c conda-forge opencv numpy pillow matplotlib seaborn pandas scipy -y

# Install AI packages via pip
pip install deepface mediapipe streamlit tensorflow keras tf-keras scikit-learn
```

### Step 5: Verify Installation
```cmd
# Test packages
python -c "import cv2; print('OpenCV:', cv2.__version__)"
python -c "import deepface; print('DeepFace: OK')"
python -c "import mediapipe; print('MediaPipe: OK')"
python -c "import streamlit; print('Streamlit: OK')"
```

## 🔍 Troubleshooting

### Common Windows Issues

#### 1. **"conda is not recognized"**
```cmd
# Add conda to PATH manually
set PATH=%PATH%;C:\Users\YourUsername\miniconda3\Scripts;C:\Users\YourUsername\miniconda3

# Or restart Command Prompt after installation
# Or run conda init and restart
conda init
```

#### 2. **"Permission denied"**
```cmd
# Run Command Prompt as Administrator
# Right-click Command Prompt → "Run as Administrator"
```

#### 3. **"Microsoft Visual C++ 14.0 is required"**
```cmd
# Install Visual Studio Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
# Or install Visual Studio Community with C++ workload
```

#### 4. **"Failed to install package"**
```cmd
# Try alternative channels
conda install -c conda-forge package_name

# Or use pip instead
pip install package_name

# Or update conda
conda update conda
```

#### 5. **PowerShell Execution Policy**
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or for current session only
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

### Package-Specific Issues

#### **OpenCV Issues**
```cmd
# Try conda version
conda install -c conda-forge opencv

# Or pip version
pip install opencv-python
```

#### **TensorFlow Issues**
```cmd
# Install CPU-only version
pip install tensorflow-cpu

# Or specific version
pip install tensorflow==2.19.1
```

#### **DeepFace Issues**
```cmd
# Clear cache
rmdir /s /q %USERPROFILE%\.deepface

# Reinstall
pip uninstall deepface
pip install deepface
```

## 🚀 Alternative Installation Methods

### Method 1: Conda-Only
```cmd
conda create -n FER_ENV python=3.9 -y
conda activate FER_ENV
conda install -c conda-forge opencv numpy pillow matplotlib seaborn pandas scipy tensorflow keras -y
pip install deepface mediapipe streamlit tf-keras scikit-learn
```

### Method 2: Pip-Only
```cmd
conda create -n FER_ENV python=3.9 -y
conda activate FER_ENV
pip install opencv-python numpy pillow matplotlib seaborn pandas scipy deepface mediapipe streamlit tensorflow keras tf-keras scikit-learn
```

### Method 3: Minimal Setup
```cmd
conda create -n FER_ENV python=3.9 -y
conda activate FER_ENV
conda install -c conda-forge opencv numpy -y
pip install deepface mediapipe streamlit
```

## 📊 Environment Management

### Useful Commands
```cmd
# List environments
conda env list

# Activate environment
conda activate FER_ENV

# Deactivate environment
conda deactivate

# Remove environment
conda env remove -n FER_ENV -y

# Export environment
conda env export > environment_backup.yml

# List packages
conda list

# Update conda
conda update conda
```

### Environment Cleanup
```cmd
# Remove unused packages
conda clean --all

# Remove unused channels
conda config --remove-key channels
```

## 🎯 Verification Steps

### 1. Environment Activation
```cmd
conda activate FER_ENV
# Should see (FER_ENV) in prompt
```

### 2. Package Verification
```cmd
python -c "
import cv2; print(f'OpenCV: {cv2.__version__}')
import numpy; print(f'NumPy: {numpy.__version__}')
import deepface; print('DeepFace: OK')
import mediapipe; print('MediaPipe: OK')
import streamlit; print('Streamlit: OK')
import tensorflow; print(f'TensorFlow: {tensorflow.__version__}')
import keras; print(f'Keras: {keras.__version__}')
"
```

### 3. FER Test
```cmd
# Test FER functionality
python test_camera.py

# Or test web interface
streamlit run live_camera_app.py
```

## 🔧 Customization

### Modify Package Versions
Edit `environment.yml`:
```yaml
dependencies:
  - python=3.9
  - opencv=4.12.0  # Change version here
  # ... other packages
```

### Environment Variables
```cmd
# Set environment variables
set CUDA_VISIBLE_DEVICES=0
set TF_CPP_MIN_LOG_LEVEL=2
```

## 📱 Windows-Specific Features

### PowerShell Benefits
- **Better error handling**
- **Color-coded output**
- **Advanced scripting capabilities**
- **Better integration with Windows**

### Command Prompt Benefits
- **Simple execution**
- **Wide compatibility**
- **No execution policy issues**
- **Familiar to most users**

## 🔒 Security Considerations

### Execution Policies
```powershell
# Check current policy
Get-ExecutionPolicy

# Set for current user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Set for current session only
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

### Administrator Rights
- **Not required** for most operations
- **May be needed** for system-wide installations
- **Use with caution** when running scripts

## 📞 Support

### Getting Help
1. **Check error messages** carefully
2. **Verify conda installation**: `conda --version`
3. **Check Python version**: `python --version`
4. **Verify environment activation**: `conda info --envs`
5. **Check package versions**: `conda list`

### Common Solutions
- **Restart Command Prompt** after conda init
- **Clear package cache**: `conda clean --all`
- **Recreate environment** if conflicts persist
- **Use conda-forge channel** for better compatibility

---

**🎉 Your FER environment is ready on Windows!**

**Next steps:**
1. Activate: `conda activate FER_ENV`
2. Test: `python test_camera.py`
3. Launch: `streamlit run live_camera_app.py`

**Happy Emotion Detection on Windows! 😊🎭🪟**
