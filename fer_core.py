import cv2
import numpy as np
import mediapipe as mp
from deepface import DeepFace
import tensorflow as tf
from typing import Tuple, Dict, List
import logging

class FEREngine:
    """
    Advanced Face Emotion Recognition Engine using latest models
    Supports: happy, surprise, frustration, anger, sad, neutral, disgust
    """
    
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1,  # 0 for short-range, 1 for full-range
            min_detection_confidence=0.5
        )
        
        # Initialize emotion models
        self.emotion_models = ['emotion', 'age', 'gender', 'race']
        self.emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        
        # Map emotions to our target categories
        self.emotion_mapping = {
            'angry': 'anger',
            'disgust': 'disgust',
            'fear': 'frustration',  # Map fear to frustration
            'happy': 'happy',
            'sad': 'sad',
            'surprise': 'surprise',
            'neutral': 'neutral'
        }
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def detect_faces(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in the frame using MediaPipe
        Returns: List of (x, y, width, height) bounding boxes
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_frame)
        
        face_boxes = []
        if results.detections:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                h, w, _ = frame.shape
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)
                face_boxes.append((x, y, width, height))
        
        return face_boxes
    
    def analyze_emotion(self, face_img: np.ndarray) -> Dict[str, float]:
        """
        Analyze emotion in the face image using DeepFace
        Returns: Dictionary with emotion probabilities
        """
        try:
            # Ensure image is in correct format
            if len(face_img.shape) == 3:
                face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
            
            # Analyze emotions using DeepFace
            result = DeepFace.analyze(
                face_img,
                actions=['emotion'],
                enforce_detection=False,
                detector_backend='opencv'
            )
            
            if isinstance(result, list):
                result = result[0]
            
            emotions = result.get('emotion', {})
            
            # Map emotions to our target categories
            mapped_emotions = {}
            for emotion, prob in emotions.items():
                mapped_emotion = self.emotion_mapping.get(emotion, emotion)
                if mapped_emotion in mapped_emotions:
                    mapped_emotions[mapped_emotion] += prob
                else:
                    mapped_emotions[mapped_emotion] = prob
            
            # Normalize probabilities
            total_prob = sum(mapped_emotions.values())
            if total_prob > 0:
                mapped_emotions = {k: v/total_prob for k, v in mapped_emotions.items()}
            
            return mapped_emotions
            
        except Exception as e:
            self.logger.error(f"Error analyzing emotion: {str(e)}")
            return {}
    
    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, List[Dict]]:
        """
        Process a single frame: detect faces and analyze emotions
        Returns: Processed frame and list of emotion results
        """
        results = []
        
        # Detect faces
        face_boxes = self.detect_faces(frame)
        
        for (x, y, w, h) in face_boxes:
            # Extract face region
            face_roi = frame[y:y+h, x:x+w]
            
            # Analyze emotion
            emotions = self.analyze_emotion(face_roi)
            
            # Store results
            result = {
                'bbox': (x, y, w, h),
                'emotions': emotions,
                'dominant_emotion': max(emotions.items(), key=lambda x: x[1])[0] if emotions else 'neutral'
            }
            results.append(result)
            
            # Draw bounding box and emotion
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Display dominant emotion
            emotion_text = result['dominant_emotion'].upper()
            cv2.putText(frame, emotion_text, (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            # Display emotion probabilities
            y_offset = y + h + 20
            for emotion, prob in emotions.items():
                text = f"{emotion}: {prob:.2f}"
                cv2.putText(frame, text, (x, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                y_offset += 20
        
        return frame, results
    
    def get_emotion_statistics(self, results: List[Dict]) -> Dict[str, float]:
        """
        Calculate emotion statistics across multiple detections
        """
        emotion_counts = {}
        total_detections = len(results)
        
        if total_detections == 0:
            return {}
        
        for result in results:
            dominant = result['dominant_emotion']
            emotion_counts[dominant] = emotion_counts.get(dominant, 0) + 1
        
        # Convert to percentages
        emotion_stats = {emotion: count/total_detections 
                        for emotion, count in emotion_counts.items()}
        
        return emotion_stats

if __name__ == "__main__":
    # Test the FER engine
    engine = FEREngine()
    print("FER Engine initialized successfully!")
    print(f"Supported emotions: {list(engine.emotion_mapping.values())}")
