# 🚀 FER Project Setup Guide

Complete setup instructions for the Face Emotion Recognition (FER) project.

## 📋 Prerequisites

- **Operating System**: macOS, Linux, or Windows
- **Python**: 3.8 or 3.9 (recommended)
- **RAM**: 4GB+ (8GB recommended)
- **Camera**: Built-in laptop camera or USB webcam
- **Git**: For version control

## 🔧 Step-by-Step Setup

### 1. Clone the Repository

```bash
# Clone the repository
git clone <your-github-repo-url>
cd FER

# Or if you already have the files locally
cd /path/to/your/FER/project
```

### 2. Install Conda (if not already installed)

```bash
# Download and install Miniconda
# Visit: https://docs.conda.io/en/latest/miniconda.html

# Or use Homebrew on macOS
brew install --cask miniconda
```

### 3. Create and Activate Conda Environment

```bash
# Create the FER environment
conda create -n FER_ENV python=3.9 -y

# Activate the environment
conda activate FER_ENV
```

### 4. Install Dependencies

```bash
# Install core packages via conda
conda install -c conda-forge opencv numpy pillow matplotlib seaborn -y

# Install remaining packages via pip
pip install deepface mediapipe streamlit tensorflow keras tf-keras
```

### 5. Verify Installation

```bash
# Test if all packages are installed correctly
python -c "import cv2, deepface, mediapipe, streamlit, tensorflow; print('✅ All packages installed successfully!')"
```

## 🎯 Quick Start Guide

### Option 1: Simple Camera Test

```bash
# Test your camera with basic emotion detection
python test_camera.py

# Controls:
# - Press 'q' to quit
# - Press 's' to save current frame
```

### Option 2: Web Interface

```bash
# Launch the Streamlit web application
streamlit run live_camera_app.py

# Open your browser and go to: http://localhost:8501
```

### Option 3: Camera Permission Test

```bash
# If you have camera issues, run this first
python camera_permission_test.py
```

## 🔍 Troubleshooting

### Camera Permission Issues (macOS)

1. **System Preferences > Security & Privacy > Privacy > Camera**
2. **Add your terminal/IDE to the allowed list**
3. **Restart your terminal/IDE**
4. **Run the permission test again**

### Common Error: "No module named 'tf_keras'"

```bash
# Install the missing package
pip install tf-keras
```

### Camera Not Working

```bash
# Check camera devices
ls /dev/video*

# Test with OpenCV
python -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened())"
```

### Performance Issues

```bash
# Reduce frame resolution in the code
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
```

## 📊 Dataset Integration

### Kaggle FER Dataset

1. **Download the dataset**: [Kaggle FER Dataset](https://www.kaggle.com/datasets/ananthu017/emotion-detection-fer)
2. **Extract to a folder** (e.g., `fer_dataset/`)
3. **Update the path** in `dataset_integration.py`
4. **Run training**:

```bash
python dataset_integration.py
```

### Dataset Structure

```
fer_dataset/
├── train/
│   ├── angry/
│   ├── disgust/
│   ├── fear/
│   ├── happy/
│   ├── sad/
│   ├── surprise/
│   └── neutral/
└── test/
    └── (same structure)
```

## 🎮 Usage Examples

### Basic Emotion Detection

```python
from fer_core import FEREngine
import cv2

# Initialize engine
fer_engine = FEREngine()

# Load image
image = cv2.imread('face.jpg')

# Analyze emotions
processed_image, results = fer_engine.process_frame(image)

# Print results
for result in results:
    print(f"Emotion: {result['dominant_emotion']}")
    print(f"Confidence: {result['emotions']}")
```

### Live Camera Processing

```python
from fer_core import FEREngine
import cv2

# Initialize engine
fer_engine = FEREngine()

# Start camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if ret:
        # Process frame
        processed_frame, results = fer_engine.process_frame(frame)
        
        # Display results
        cv2.imshow('FER Test', processed_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
```

## 📈 Performance Optimization

### For Better FPS
- Reduce frame resolution
- Process every nth frame
- Use GPU acceleration (if available)
- Optimize face detection confidence

### For Better Accuracy
- Ensure good lighting
- Face should be clearly visible
- Avoid extreme angles
- Use higher resolution input

## 🐛 Debugging

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Model Downloads

```bash
# Clear DeepFace cache
rm -rf ~/.deepface/

# Force model download
python -c "from deepface import DeepFace; DeepFace.analyze('test.jpg', actions=['emotion'])"
```

## 📱 Mobile/Remote Access

### Streamlit Remote Access

```bash
# Allow external access
streamlit run live_camera_app.py --server.address 0.0.0.0 --server.port 8501
```

### Access from other devices
- **Local Network**: `http://your-computer-ip:8501`
- **Internet**: Use ngrok or similar service

## 🔒 Security Considerations

- **Camera Access**: Only grant to trusted applications
- **Network Access**: Be careful with remote access
- **Model Files**: Keep trained models secure
- **Data Privacy**: Don't share sensitive images

## 📞 Support

### Common Issues
1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Check camera permissions
4. Ensure sufficient system resources

### Getting Help
1. Check the README.md file
2. Review error messages carefully
3. Test with the permission test script
4. Create an issue with detailed information

## 🎉 Success Checklist

- [ ] Repository cloned/downloaded
- [ ] Conda environment created and activated
- [ ] All dependencies installed
- [ ] Camera permissions granted
- [ ] Basic camera test working
- [ ] FER engine initializing without errors
- [ ] Live camera app launching
- [ ] Emotions being detected in real-time

---

**Happy Emotion Detection! 😊🎭**

If you encounter any issues, refer to the troubleshooting section or create an issue in the repository.
