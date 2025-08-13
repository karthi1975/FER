@echo off
echo 🎭 FER Project - Simple Windows Setup
echo ======================================
echo.

echo 📋 This script will create your FER environment
echo.

REM Check if conda is available
conda --version >nul 2>&nul
if errorlevel 1 (
    echo ❌ Conda not found! Please install Miniconda first.
    echo    Download from: https://docs.conda.io/en/latest/miniconda.html
    pause
    exit /b 1
)

echo ✅ Conda found
echo.

REM Create environment
echo 📦 Creating FER_ENV environment...
conda create -n FER_ENV python=3.9 -y

REM Install packages
echo 📦 Installing packages...
conda install -n FER_ENV -c conda-forge opencv numpy pillow matplotlib seaborn pandas scipy -y

REM Activate and install pip packages
echo 📦 Installing AI packages...
call conda activate FER_ENV
pip install deepface mediapipe streamlit tensorflow keras tf-keras scikit-learn

echo.
echo 🎉 Setup complete!
echo.
echo 💡 To use your environment:
echo    1. conda activate FER_ENV
echo    2. python test_camera.py
echo    3. streamlit run live_camera_app.py
echo.
pause
