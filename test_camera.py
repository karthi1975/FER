#!/usr/bin/env python3
"""
Simple Camera Test for FER Engine
Run this to test your laptop camera with emotion detection
"""

import cv2
import numpy as np
from fer_core import FEREngine
import time

def test_camera():
    """Test the camera with FER engine"""
    print("🎭 Starting Face Emotion Recognition Camera Test...")
    print("Press 'q' to quit, 's' to save current frame")
    
    # Initialize FER engine
    fer_engine = FEREngine()
    print("✅ FER Engine initialized successfully!")
    
    # Start camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Error: Could not open camera!")
        return
    
            # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
    
    print("📹 Camera started successfully!")
    print("🔍 Detecting faces and emotions in real-time...")
    print("Supported emotions:", list(fer_engine.emotion_mapping.values()))
    
    frame_count = 0
    start_time = time.time()
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Failed to read frame from camera")
                break
            
            # Process frame with FER engine
            processed_frame, results = fer_engine.process_frame(frame)
            
            # Display frame info
            frame_count += 1
            if frame_count % 30 == 0:  # Update every 30 frames
                elapsed_time = time.time() - start_time
                fps = frame_count / elapsed_time
                print(f"📊 FPS: {fps:.1f}, Frame: {frame_count}, Detections: {len(results)}")
            
            # Display results
            if results:
                for i, result in enumerate(results):
                    emotion = result['dominant_emotion']
                    confidence = max(result['emotions'].values()) if result['emotions'] else 0
                    print(f"😊 Face {i+1}: {emotion.upper()} (Confidence: {confidence:.2%})")
            
            # Show the frame
            cv2.imshow('FER Camera Test', processed_frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("👋 Quitting...")
                break
            elif key == ord('s'):
                # Save current frame
                timestamp = int(time.time())
                filename = f"fer_frame_{timestamp}.jpg"
                cv2.imwrite(filename, processed_frame)
                print(f"💾 Saved frame as {filename}")
    
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
    
    finally:
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        
        # Print final statistics
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            avg_fps = frame_count / elapsed_time
            print(f"\n📈 Final Statistics:")
            print(f"   Total Frames: {frame_count}")
            print(f"   Total Time: {elapsed_time:.1f} seconds")
            print(f"   Average FPS: {avg_fps:.1f}")
            print("✅ Camera test completed successfully!")

if __name__ == "__main__":
    test_camera()
