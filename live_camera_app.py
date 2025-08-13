import cv2
import numpy as np
import streamlit as st
from fer_core import FEREngine
import time
import threading
from collections import deque
import matplotlib.pyplot as plt
import seaborn as sns

class LiveCameraFER:
    """
    Live Camera Face Emotion Recognition Application
    """
    
    def __init__(self):
        self.fer_engine = FEREngine()
        self.cap = None
        self.is_running = False
        self.emotion_history = deque(maxlen=100)  # Store last 100 emotion detections
        self.frame_count = 0
        
    def start_camera(self):
        """Start the camera capture"""
        self.cap = cv2.VideoCapture(0)  # Use default camera (usually laptop camera)
        if not self.cap.isOpened():
            st.error("Error: Could not open camera!")
            return False
        
        # Set camera properties for better performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        return True
    
    def stop_camera(self):
        """Stop the camera capture"""
        if self.cap:
            self.cap.release()
        self.is_running = False
    
    def process_frame(self, frame):
        """Process a single frame and return results"""
        try:
            # Process frame with FER engine
            processed_frame, results = self.fer_engine.process_frame(frame)
            
            # Store emotion results for statistics
            if results:
                for result in results:
                    self.emotion_history.append({
                        'emotion': result['dominant_emotion'],
                        'confidence': max(result['emotions'].values()) if result['emotions'] else 0,
                        'timestamp': time.time()
                    })
            
            return processed_frame, results
            
        except Exception as e:
            st.error(f"Error processing frame: {str(e)}")
            return frame, []
    
    def get_emotion_statistics(self):
        """Get emotion statistics from history"""
        if not self.emotion_history:
            return {}
        
        emotion_counts = {}
        total_detections = len(self.emotion_history)
        
        for entry in self.emotion_history:
            emotion = entry['emotion']
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Convert to percentages
        emotion_stats = {emotion: count/total_detections 
                        for emotion, count in emotion_counts.items()}
        
        return emotion_stats
    
    def run_camera_loop(self):
        """Main camera processing loop"""
        self.is_running = True
        
        while self.is_running:
            if self.cap and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    # Process frame
                    processed_frame, results = self.process_frame(frame)
                    
                    # Convert BGR to RGB for display
                    rgb_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                    
                    # Update the frame in Streamlit
                    self.current_frame = rgb_frame
                    self.current_results = results
                    
                    self.frame_count += 1
                    
                    # Small delay to control frame rate
                    time.sleep(0.03)  # ~30 FPS
                else:
                    st.error("Failed to read frame from camera")
                    break
            else:
                break

def main():
    st.set_page_config(
        page_title="Live FER - Face Emotion Recognition",
        page_icon="😊",
        layout="wide"
    )
    
    st.title("🎭 Live Face Emotion Recognition")
    st.markdown("Real-time emotion detection using your laptop camera")
    
    # Initialize the FER application
    if 'fer_app' not in st.session_state:
        st.session_state.fer_app = LiveCameraFER()
    
    fer_app = st.session_state.fer_app
    
    # Sidebar controls
    st.sidebar.header("🎛️ Controls")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("📹 Start Camera", type="primary"):
            if fer_app.start_camera():
                st.success("Camera started successfully!")
                # Start camera processing in a separate thread
                camera_thread = threading.Thread(target=fer_app.run_camera_loop)
                camera_thread.daemon = True
                camera_thread.start()
                st.session_state.camera_running = True
            else:
                st.error("Failed to start camera!")
    
    with col2:
        if st.button("⏹️ Stop Camera"):
            fer_app.stop_camera()
            st.session_state.camera_running = False
            st.success("Camera stopped!")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📸 Live Camera Feed")
        
        if st.session_state.get('camera_running', False):
            # Create a placeholder for the camera feed
            camera_placeholder = st.empty()
            
            # Display camera feed
            if hasattr(fer_app, 'current_frame') and fer_app.current_frame is not None:
                camera_placeholder.image(fer_app.current_frame, channels="RGB", use_column_width=True)
                
                # Display current emotion results
                if hasattr(fer_app, 'current_results') and fer_app.current_results:
                    st.subheader("🔍 Current Detections")
                    for i, result in enumerate(fer_app.current_results):
                        with st.expander(f"Face {i+1} - {result['dominant_emotion'].upper()}"):
                            # Display emotion probabilities
                            emotions_df = {
                                'Emotion': list(result['emotions'].keys()),
                                'Probability': list(result['emotions'].values())
                            }
                            st.bar_chart(emotions_df)
                            
                            # Display detailed probabilities
                            for emotion, prob in result['emotions'].items():
                                st.metric(emotion.title(), f"{prob:.2%}")
        else:
            st.info("Click 'Start Camera' to begin emotion detection")
    
    with col2:
        st.header("📊 Emotion Statistics")
        
        if fer_app.emotion_history:
            # Get emotion statistics
            emotion_stats = fer_app.get_emotion_statistics()
            
            if emotion_stats:
                # Create pie chart
                fig, ax = plt.subplots(figsize=(8, 6))
                emotions = list(emotion_stats.keys())
                values = list(emotion_stats.values())
                
                # Create color map for emotions
                colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
                
                wedges, texts, autotexts = ax.pie(values, labels=emotions, autopct='%1.1f%%', 
                                                 colors=colors[:len(emotions)])
                ax.set_title('Emotion Distribution')
                
                st.pyplot(fig)
                
                # Display statistics table
                st.subheader("📈 Detailed Stats")
                for emotion, percentage in emotion_stats.items():
                    st.metric(emotion.title(), f"{percentage:.1%}")
                
                # Display total detections
                st.metric("Total Detections", len(fer_app.emotion_history))
        else:
            st.info("No emotion data yet. Start the camera to collect data!")
    
    # Additional features
    st.header("🎯 Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**Real-time Detection**\n\nDetect 7 emotions: Happy, Surprise, Frustration, Anger, Sad, Neutral, Disgust")
    
    with col2:
        st.info("**High Accuracy**\n\nUses latest MediaPipe + DeepFace models for superior performance")
    
    with col3:
        st.info("**Live Statistics**\n\nTrack emotion patterns and confidence levels in real-time")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Built with ❤️ using MediaPipe, DeepFace, and Streamlit</p>
        <p>Supports the FER dataset from <a href='https://www.kaggle.com/datasets/ananthu017/emotion-detection-fer' target='_blank'>Kaggle</a></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
