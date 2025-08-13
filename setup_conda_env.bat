@echo off
REM 🎭 FER Project Conda Environment Setup Script for Windows
REM This script will create and configure your FER environment

echo 🚀 Starting FER Project Conda Environment Setup...
echo ==================================================

REM Check if conda is installed
where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Conda is not installed!
    echo 📥 Please install Miniconda first:
    echo    Visit: https://docs.conda.io/en/latest/miniconda.html
    pause
    exit /b 1
)

echo ✅ Conda is installed
conda --version

REM Check if FER_ENV already exists
conda env list | findstr "FER_ENV" >nul
if %errorlevel% equ 0 (
    echo ⚠️  FER_ENV environment already exists!
    set /p choice="Do you want to remove it and recreate? (y/n): "
    if /i "%choice%"=="y" (
        echo 🗑️  Removing existing FER_ENV...
        conda env remove -n FER_ENV -y
    ) else (
        echo 🔄 Using existing FER_ENV environment...
        echo 💡 To activate: conda activate FER_ENV
        pause
        exit /b 0
    )
)

echo 🔧 Creating FER_ENV environment from environment.yml...

REM Create environment from yml file
conda env create -f environment.yml
if %errorlevel% equ 0 (
    echo ✅ Environment created successfully!
) else (
    echo ❌ Failed to create environment from yml file.
    echo 🔄 Trying manual creation...
    
    REM Manual creation as fallback
    echo 📦 Creating environment with core packages...
    conda create -n FER_ENV python=3.9 -y
    
    echo 📦 Installing core packages via conda...
    conda install -n FER_ENV -c conda-forge opencv numpy pillow matplotlib seaborn pandas scipy -y
    
    echo 📦 Installing remaining packages via pip...
    call conda activate FER_ENV
    pip install deepface==0.0.95 mediapipe==0.10.21 streamlit==1.48.1 tensorflow==2.19.1 keras==3.10.0 tf-keras==2.19.0 scikit-learn==1.3.0
)

echo.
echo 🎉 Environment setup completed!
echo ==================================================
echo 📋 Next steps:
echo    1. Activate environment: conda activate FER_ENV
echo    2. Verify installation: python -c "import cv2, deepface, mediapipe, streamlit; print('✅ All packages installed!')"
echo    3. Test camera: python camera_permission_test.py
echo    4. Run FER: python test_camera.py
echo.
echo 💡 Quick commands:
echo    conda activate FER_ENV
echo    python test_camera.py
echo    streamlit run live_camera_app.py
echo.
echo 🔗 For more help, see SETUP.md and README.md
echo ==================================================
pause
