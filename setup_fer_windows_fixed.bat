@echo off
setlocal enabledelayedexpansion

REM 🎭 FER Project Windows Setup Script (Fixed Version)
REM This script will create and configure your FER environment on Windows

echo.
echo ========================================================
echo 🚀 FER Project Windows Setup Script
echo ========================================================
echo.

REM Set title
title FER Project Setup - Windows

REM Check if running as administrator
net session >nul 2>nul
if %errorLevel% == 0 (
    echo ✅ Running with administrator privileges
) else (
    echo ⚠️  Not running as administrator (this is usually fine)
)

echo.
echo 📋 Checking prerequisites...
echo ========================================================

REM Check if conda is installed
where conda >nul 2>nul
if %errorLevel% neq 0 (
    echo ❌ Conda is not installed or not in PATH!
    echo.
    echo 📥 Please install Miniconda first:
    echo    1. Download from: https://docs.conda.io/en/latest/miniconda.html
    echo    2. Choose Windows x86_64 installer
    echo    3. Install with default settings
    echo    4. Restart your command prompt
    echo.
    echo 💡 Or use Chocolatey: choco install miniconda3
    echo.
    pause
    exit /b 1
)

echo ✅ Conda is installed
for /f "tokens=*" %%i in ('conda --version') do echo    Version: %%i

REM Check if Python is available
python --version >nul 2>nul
if %errorLevel% neq 0 (
    echo ❌ Python is not available in PATH
    echo 💡 This will be fixed when we create the conda environment
) else (
    echo ✅ Python is available
    for /f "tokens=*" %%i in ('python --version') do echo    Version: %%i
)

echo.
echo 🔧 Environment Setup
echo ========================================================

REM Check if FER_ENV already exists
conda env list | findstr "FER_ENV" >nul 2>nul
if %errorLevel% equ 0 (
    echo ⚠️  FER_ENV environment already exists!
    echo.
    set /p choice="Do you want to remove it and recreate? (y/n): "
    if /i "!choice!"=="y" (
        echo 🗑️  Removing existing FER_ENV...
        conda env remove -n FER_ENV -y
        if !errorLevel! neq 0 (
            echo ❌ Failed to remove environment
            pause
            exit /b 1
        )
        echo ✅ Environment removed successfully
    ) else (
        echo 🔄 Using existing FER_ENV environment...
        echo 💡 To activate: conda activate FER_ENV
        goto :activate_environment
    )
)

echo.
echo 📦 Creating FER_ENV environment...

REM Try to create environment from yml file
if exist "environment.yml" (
    echo 🔧 Creating environment from environment.yml...
    conda env create -f environment.yml
    if !errorLevel! equ 0 (
        echo ✅ Environment created successfully from yml file!
    ) else (
        echo ❌ Failed to create environment from yml file.
        echo 🔄 Trying manual creation...
        goto :manual_creation
    )
) else (
    echo ⚠️  environment.yml not found, using manual creation...
    goto :manual_creation
)

:manual_creation
echo.
echo 📦 Creating environment manually...

REM Create base environment
echo    Creating base environment with Python 3.9...
conda create -n FER_ENV python=3.9 -y
if !errorLevel! neq 0 (
    echo ❌ Failed to create base environment
    pause
    exit /b 1
)

REM Install core packages via conda
echo    Installing core packages via conda...
conda install -n FER_ENV -c conda-forge opencv numpy pillow matplotlib seaborn pandas scipy -y
if !errorLevel! neq 0 (
    echo ❌ Failed to install core packages
    echo 💡 Trying alternative channels...
    conda install -n FER_ENV opencv numpy pillow matplotlib seaborn pandas scipy -y
)

REM Install AI/ML packages via pip
echo    Installing AI/ML packages via pip...
call conda activate FER_ENV
if !errorLevel! neq 0 (
    echo ❌ Failed to activate environment
    pause
    exit /b 1
)

echo    Installing DeepFace...
pip install deepface==0.0.95
echo    Installing MediaPipe...
pip install mediapipe==0.10.21
echo    Installing Streamlit...
pip install streamlit==1.48.1
echo    Installing TensorFlow...
pip install tensorflow==2.19.1
echo    Installing Keras...
pip install keras==3.10.0
echo    Installing tf-keras...
pip install tf-keras==2.19.0
echo    Installing Scikit-learn...
pip install scikit-learn==1.3.0

:activate_environment
echo.
echo 🔄 Activating FER_ENV environment...
call conda activate FER_ENV
if !errorLevel! neq 0 (
    echo ❌ Failed to activate environment
    pause
    exit /b 1
)

echo ✅ Environment activated successfully!

echo.
echo 🧪 Testing Installation
echo ========================================================

echo 📦 Verifying package installation...
python -c "import cv2; print('✅ OpenCV:', cv2.__version__)" 2>nul
if !errorLevel! neq 0 echo ❌ OpenCV not working

python -c "import numpy; print('✅ NumPy:', numpy.__version__)" 2>nul
if !errorLevel! neq 0 echo ❌ NumPy not working

python -c "import deepface; print('✅ DeepFace: OK')" 2>nul
if !errorLevel! neq 0 echo ❌ DeepFace not working

python -c "import mediapipe; print('✅ MediaPipe: OK')" 2>nul
if !errorLevel! neq 0 echo ❌ MediaPipe not working

python -c "import streamlit; print('✅ Streamlit: OK')" 2>nul
if !errorLevel! neq 0 echo ❌ Streamlit not working

python -c "import tensorflow; print('✅ TensorFlow:', tensorflow.__version__)" 2>nul
if !errorLevel! neq 0 echo ❌ TensorFlow not working

echo.
echo 🎯 Testing FER Core...
python -c "from fer_core import FEREngine; print('✅ FER Engine: OK')" 2>nul
if !errorLevel! neq 0 (
    echo ❌ FER Engine not working
    echo 💡 This might be normal if files are missing
)

echo.
echo 🎉 Setup Completed Successfully!
echo ========================================================
echo.
echo 📋 Next Steps:
echo    1. ✅ Environment created and activated
echo    2. 🔍 Test camera: python camera_permission_test.py
echo    3. 🎭 Run FER: python test_camera.py
echo    4. 🌐 Launch web app: streamlit run live_camera_app.py
echo.
echo 💡 Quick Commands:
echo    conda activate FER_ENV
echo    python test_camera.py
echo    streamlit run live_camera_app.py
echo.
echo 🔗 For more help, see:
echo    - CONDA_SETUP.md
echo    - SETUP.md
echo    - README.md
echo.
echo ========================================================
echo 🎭 Happy Emotion Detection! 😊
echo ========================================================
echo.

REM Keep window open
pause
