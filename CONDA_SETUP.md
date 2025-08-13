# 🐍 Conda Environment Setup for FER Project

Complete guide to set up your FER (Face Emotion Recognition) project using conda.

## 🚀 Quick Start (Recommended)

### Method 1: Automated Setup (Easiest)

#### On macOS/Linux:
```bash
# Make script executable
chmod +x setup_conda_env.sh

# Run the setup script
./setup_conda_env.sh
```

#### On Windows:
```cmd
# Run the batch file
setup_conda_env.bat
```

### Method 2: Manual Setup

```bash
# Create environment from yml file
conda env create -f environment.yml

# Activate environment
conda activate FER_ENV

# Verify installation
python -c "import cv2, deepface, mediapipe, streamlit; print('✅ All packages installed!')"
```

## 📋 Prerequisites

### 1. Install Conda

#### Option A: Miniconda (Recommended)
```bash
# macOS with Homebrew
brew install --cask miniconda

# Or download from website
# Visit: https://docs.conda.io/en/latest/miniconda.html
```

#### Option B: Anaconda
```bash
# Download from website
# Visit: https://www.anaconda.com/products/distribution
```

### 2. Verify Conda Installation
```bash
conda --version
# Should show: conda 4.x.x
```

## 🔧 Step-by-Step Manual Setup

### Step 1: Create Environment
```bash
# Create new environment with Python 3.9
conda create -n FER_ENV python=3.9 -y
```

### Step 2: Activate Environment
```bash
# Activate the environment
conda activate FER_ENV

# Verify activation (should show FER_ENV in prompt)
conda info --envs
```

### Step 3: Install Core Packages via Conda
```bash
# Install core packages from conda-forge
conda install -c conda-forge opencv numpy pillow matplotlib seaborn pandas scipy -y
```

### Step 4: Install AI/ML Packages via Pip
```bash
# Install remaining packages
pip install deepface==0.0.95 mediapipe==0.10.21 streamlit==1.48.1 tensorflow==2.19.1 keras==3.10.0 tf-keras==2.19.0 scikit-learn==1.3.0
```

### Step 5: Verify Installation
```bash
# Test all packages
python -c "
import cv2
import numpy as np
import deepface
import mediapipe as mp
import streamlit as st
import tensorflow as tf
import keras
print('✅ All packages installed successfully!')
print(f'OpenCV version: {cv2.__version__}')
print(f'TensorFlow version: {tf.__version__}')
print(f'Keras version: {keras.__version__}')
"
```

## 🎯 Environment.yml Details

The `environment.yml` file contains:

```yaml
name: FER_ENV
channels:
  - conda-forge    # Better package compatibility
  - defaults       # Fallback packages
dependencies:
  - python=3.9     # Specific Python version
  - opencv=4.12.0  # Computer vision
  - numpy=1.26.4   # Numerical computing
  - pillow=11.3.0  # Image processing
  - matplotlib=3.9.4 # Plotting
  - seaborn=0.13.2 # Statistical visualization
  - pandas=2.3.1   # Data manipulation
  - scipy=1.13.1   # Scientific computing
  - pip            # Python package installer
  - pip:           # Packages to install via pip
    - deepface==0.0.95      # Emotion recognition
    - mediapipe==0.10.21    # Face detection
    - streamlit==1.48.1     # Web interface
    - tensorflow==2.19.1    # Deep learning
    - keras==3.10.0         # Neural networks
    - tf-keras==2.19.0      # TensorFlow Keras
    - scikit-learn==1.3.0   # Machine learning
```

## 🔍 Troubleshooting

### Common Issues

#### 1. "Conda command not found"
```bash
# Add conda to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$HOME/miniconda3/bin:$PATH"

# Or initialize conda
conda init
# Restart terminal
```

#### 2. "Package not found in conda"
```bash
# Try conda-forge channel
conda install -c conda-forge package_name

# Or use pip instead
pip install package_name
```

#### 3. "Version conflicts"
```bash
# Remove environment and recreate
conda env remove -n FER_ENV -y
conda env create -f environment.yml
```

#### 4. "Permission denied" (macOS)
```bash
# Fix script permissions
chmod +x setup_conda_env.sh

# Or run manually
bash setup_conda_env.sh
```

#### 5. "CUDA/GPU issues"
```bash
# Install CPU-only TensorFlow
pip uninstall tensorflow
pip install tensorflow-cpu

# Or use conda
conda install tensorflow-cpu
```

### Package-Specific Issues

#### DeepFace Issues
```bash
# Clear cache
rm -rf ~/.deepface/

# Force reinstall
pip uninstall deepface
pip install deepface
```

#### MediaPipe Issues
```bash
# Check version compatibility
pip install mediapipe==0.10.21

# Or try latest
pip install mediapipe
```

#### OpenCV Issues
```bash
# Install from conda-forge
conda install -c conda-forge opencv

# Or use pip version
pip install opencv-python
```

## 🚀 Alternative Installation Methods

### Method 1: Conda-Only (Slower but more stable)
```bash
conda create -n FER_ENV python=3.9 -y
conda activate FER_ENV
conda install -c conda-forge opencv numpy pillow matplotlib seaborn pandas scipy tensorflow keras -y
pip install deepface mediapipe streamlit tf-keras scikit-learn
```

### Method 2: Pip-Only (Faster but potential conflicts)
```bash
conda create -n FER_ENV python=3.9 -y
conda activate FER_ENV
pip install opencv-python numpy pillow matplotlib seaborn pandas scipy deepface mediapipe streamlit tensorflow keras tf-keras scikit-learn
```

### Method 3: Minimal Setup (For testing)
```bash
conda create -n FER_ENV python=3.9 -y
conda activate FER_ENV
conda install -c conda-forge opencv numpy -y
pip install deepface mediapipe streamlit
```

## 📊 Environment Management

### Useful Commands
```bash
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

# List packages in environment
conda list

# Update conda
conda update conda
```

### Environment Cleanup
```bash
# Remove unused packages
conda clean --all

# Remove unused channels
conda config --remove-key channels

# Reset conda configuration
conda config --remove-key channels
```

## 🎯 Verification Steps

### 1. Environment Activation
```bash
conda activate FER_ENV
# Should see (FER_ENV) in prompt
```

### 2. Package Verification
```bash
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

### 3. Camera Test
```bash
# Test camera access
python camera_permission_test.py

# Test FER functionality
python test_camera.py
```

### 4. Web Interface Test
```bash
# Launch Streamlit app
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

### Add New Packages
```yaml
dependencies:
  # ... existing packages
  - pip:
    - existing-package
    - new-package==1.0.0  # Add new package
```

### Environment Variables
```bash
# Set environment variables
export CUDA_VISIBLE_DEVICES=0  # Use GPU 0
export TF_CPP_MIN_LOG_LEVEL=2  # Reduce TensorFlow logging
```

## 📞 Support

### Getting Help
1. **Check error messages** carefully
2. **Verify conda installation**: `conda --version`
3. **Check Python version**: `python --version`
4. **Verify environment activation**: `conda info --envs`
5. **Check package versions**: `conda list`

### Common Solutions
- **Restart terminal** after conda init
- **Clear package cache**: `conda clean --all`
- **Recreate environment** if conflicts persist
- **Use conda-forge channel** for better compatibility

---

**🎉 Your FER environment is ready!**

**Next steps:**
1. Activate: `conda activate FER_ENV`
2. Test: `python test_camera.py`
3. Launch: `streamlit run live_camera_app.py`

**Happy Emotion Detection! 😊🎭**
