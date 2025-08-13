#!/usr/bin/env python3
"""
Camera Permission Test for macOS
This script helps troubleshoot camera access issues
"""

import cv2
import sys
import os

def test_camera_permissions():
    """Test camera access and provide troubleshooting steps"""
    print("📹 Camera Permission Test for macOS")
    print("=" * 50)
    
    # Check if we're on macOS
    if sys.platform == "darwin":
        print("🖥️  Detected macOS")
        print("\n📋 Camera Permission Steps:")
        print("1. Go to System Preferences > Security & Privacy > Privacy")
        print("2. Select 'Camera' from the left sidebar")
        print("3. Make sure your terminal/IDE is checked")
        print("4. If not, click the lock icon and add it")
        print("5. Restart your terminal/IDE after granting permission")
        
        # Check common camera devices
        print("\n🔍 Checking camera devices...")
        for i in range(5):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                print(f"✅ Camera {i} is accessible")
                ret, frame = cap.read()
                if ret:
                    print(f"   Resolution: {frame.shape[1]}x{frame.shape[0]}")
                cap.release()
            else:
                print(f"❌ Camera {i} is not accessible")
    
    else:
        print("🖥️  Detected non-macOS system")
    
    print("\n🚀 Testing camera access...")
    
    # Try to open camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Failed to open camera!")
        print("\n🔧 Troubleshooting steps:")
        print("1. Check if another application is using the camera")
        print("2. Try restarting your computer")
        print("3. Check if camera works in other apps (FaceTime, Photo Booth)")
        print("4. Try different camera index (0, 1, 2...)")
        
        # Try different camera indices
        print("\n🔄 Trying different camera indices...")
        for i in range(1, 5):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                print(f"✅ Camera {i} works! Use this index in your code.")
                cap.release()
                return i
            cap.release()
        
        return None
    else:
        print("✅ Camera opened successfully!")
        
        # Get camera properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        print(f"   Resolution: {width}x{height}")
        print(f"   FPS: {fps}")
        
        # Try to read a frame
        ret, frame = cap.read()
        if ret:
            print("✅ Successfully read frame from camera!")
            print(f"   Frame shape: {frame.shape}")
        else:
            print("❌ Failed to read frame from camera")
        
        cap.release()
        return 0

def test_opencv_camera():
    """Test OpenCV camera functionality"""
    print("\n🔧 Testing OpenCV camera functionality...")
    
    # Test basic OpenCV
    try:
        import cv2
        print(f"✅ OpenCV version: {cv2.__version__}")
    except ImportError as e:
        print(f"❌ OpenCV import error: {e}")
        return False
    
    # Test camera capture
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ OpenCV camera capture works")
            cap.release()
            return True
        else:
            print("❌ OpenCV camera capture failed")
            return False
    except Exception as e:
        print(f"❌ OpenCV camera error: {e}")
        return False

if __name__ == "__main__":
    print("🎭 FER Camera Permission Test")
    print("=" * 40)
    
    # Test OpenCV
    opencv_ok = test_opencv_camera()
    
    if opencv_ok:
        # Test camera permissions
        camera_index = test_camera_permissions()
        
        if camera_index is not None:
            print(f"\n🎉 Camera test completed successfully!")
            print(f"   Use camera index: {camera_index}")
            print("\n💡 Next steps:")
            print("   1. Run: python test_camera.py")
            print("   2. Or run: streamlit run live_camera_app.py")
        else:
            print("\n❌ Camera test failed!")
            print("   Please check camera permissions and try again")
    else:
        print("\n❌ OpenCV test failed!")
        print("   Please check your OpenCV installation")
