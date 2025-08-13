#!/bin/bash

# 🎭 FER Project Conda Environment Setup Script
# This script will create and configure your FER environment

echo "🚀 Starting FER Project Conda Environment Setup..."
echo "=================================================="

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "❌ Conda is not installed!"
    echo "📥 Please install Miniconda first:"
    echo "   Visit: https://docs.conda.io/en/latest/miniconda.html"
    echo "   Or use Homebrew on macOS: brew install --cask miniconda"
    exit 1
fi

echo "✅ Conda is installed: $(conda --version)"

# Check if FER_ENV already exists
if conda env list | grep -q "FER_ENV"; then
    echo "⚠️  FER_ENV environment already exists!"
    read -p "Do you want to remove it and recreate? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing existing FER_ENV..."
        conda env remove -n FER_ENV -y
    else
        echo "🔄 Using existing FER_ENV environment..."
        echo "💡 To activate: conda activate FER_ENV"
        exit 0
    fi
fi

echo "🔧 Creating FER_ENV environment from environment.yml..."

# Create environment from yml file
if conda env create -f environment.yml; then
    echo "✅ Environment created successfully!"
else
    echo "❌ Failed to create environment from yml file."
    echo "🔄 Trying manual creation..."
    
    # Manual creation as fallback
    echo "📦 Creating environment with core packages..."
    conda create -n FER_ENV python=3.9 -y
    
    echo "📦 Installing core packages via conda..."
    conda install -n FER_ENV -c conda-forge opencv numpy pillow matplotlib seaborn pandas scipy -y
    
    echo "📦 Installing remaining packages via pip..."
    conda activate FER_ENV
    pip install deepface==0.0.95 mediapipe==0.10.21 streamlit==1.48.1 tensorflow==2.19.1 keras==3.10.0 tf-keras==2.19.0 scikit-learn==1.3.0
fi

echo ""
echo "🎉 Environment setup completed!"
echo "=================================================="
echo "📋 Next steps:"
echo "   1. Activate environment: conda activate FER_ENV"
echo "   2. Verify installation: python -c \"import cv2, deepface, mediapipe, streamlit; print('✅ All packages installed!')\""
echo "   3. Test camera: python camera_permission_test.py"
echo "   4. Run FER: python test_camera.py"
echo ""
echo "💡 Quick commands:"
echo "   conda activate FER_ENV"
echo "   python test_camera.py"
echo "   streamlit run live_camera_app.py"
echo ""
echo "🔗 For more help, see SETUP.md and README.md"
echo "=================================================="
