import cv2
from deepface import DeepFace
import pygame
import os
import random
import time
import numpy as np

# Define emotion to music file mapping
EMOTION_MUSIC_MAP = {
    'happy': 'musics/happy.mp3',
    'sad': 'musics/sad.mp3',
    'angry': 'musics/anger.mp3',
    'surprise': 'musics/happy.mp3',  # fallback if you don't have a surprise.mp3
    'neutral': 'musics/neutral.mp3',   # now play neutral.mp3 for neutral emotion
    'fear': 'musics/fear.mp3',
    'disgust': 'musics/anger.mp3'    # fallback if you don't have a disgust.mp3
}

def capture_image():
    cap = cv2.VideoCapture(0)
    print("Press SPACE to capture image...")
    while True:
        ret, frame = cap.read()
        cv2.imshow('Capture', frame)
        if cv2.waitKey(1) & 0xFF == ord(' '):
            img_path = 'captured_face.jpg'
            cv2.imwrite(img_path, frame)
            break
    cap.release()
    cv2.destroyAllWindows()
    return img_path

def detect_emotion(img_path):
    try:
        result = DeepFace.analyze(img_path=img_path, actions=['emotion'], enforce_detection=False)
        print(f"DeepFace result: {result}")
        # DeepFace now returns a list of results
        emotion = result[0]['dominant_emotion']
        print(f"Detected emotion: {emotion}")
        return emotion
    except Exception as e:
        print(f"Error detecting emotion: {e}")
        print("Falling back to 'happy' emotion.")
        return 'happy'  # fallback

def play_music_for_emotion(emotion):
    emotion_key = emotion.strip().lower()
    print(f"Emotion key used for lookup: '{emotion_key}'")
    if emotion_key in EMOTION_MUSIC_MAP:
        music_file = EMOTION_MUSIC_MAP[emotion_key]
    else:
        print(f"No mapping for emotion: {emotion_key}, playing happy.mp3 as fallback.")
        music_file = EMOTION_MUSIC_MAP['happy']
    print(f"Music file resolved: {music_file}")
    if not os.path.exists(music_file):
        print(f"No music file for emotion: {emotion_key}")
        return
    print(f"Playing: {music_file}")
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Error playing music: {e}")

def real_time_emotion_music_player():
    cap = cv2.VideoCapture(0)
    last_emotion = None
    last_analysis_time = 0
    analyze_interval_sec = 2  # Analyze every 2 seconds
    print("Press 'q' to quit.")
    faces = []  # Store last detected faces for persistent box
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break
            display_frame = frame.copy()
            now = time.time()
            emotion_key = None
            # Draw last detected faces' boxes and emotions
            for face in faces:
                x, y, w, h = face['region']['x'], face['region']['y'], face['region']['w'], face['region']['h']
                emotion = face['dominant_emotion']
                cv2.rectangle(display_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(display_frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            if now - last_analysis_time > analyze_interval_sec:
                img_path = 'captured_face.jpg'
                cv2.imwrite(img_path, frame)
                try:
                    result = DeepFace.analyze(img_path=img_path, actions=['emotion'], enforce_detection=False)
                    # DeepFace returns a list of dicts, one per face
                    if isinstance(result, list):
                        faces = result
                    else:
                        faces = [result]
                    for face in faces:
                        emotion = face['dominant_emotion']
                        emotion_key = emotion.strip().lower()
                        # Only play music if confidence is high enough
                        emotion_confidence = face['emotion'].get(emotion, 0)
                        print(f"Detected emotion: {emotion_key} (confidence: {emotion_confidence:.2f})")
                        if emotion_key != last_emotion and emotion_confidence > 50:
                            play_music_for_emotion(emotion_key)
                            last_emotion = emotion_key
                            break
                except Exception as e:
                    print(f"Error detecting emotion: {e}")
                last_analysis_time = now
            cv2.imshow('Real-Time Emotion Detection', display_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        pygame.mixer.quit()

def main():
    img_path = capture_image()
    emotion = detect_emotion(img_path)
    play_music_for_emotion(emotion)
    # Wait for the song to finish or until user presses 'q'
    try:
        print("Press the close button on the window or 'q' in the window to quit before the music ends.")
        # Create a small OpenCV window to capture 'q' key
        cv2.namedWindow('Press q to quit')
        blank = 255 * np.ones((50, 300, 3), dtype=np.uint8)
        cv2.imshow('Press q to quit', blank)
        while pygame.mixer.music.get_busy():
            if cv2.waitKey(100) & 0xFF == ord('q'):
                pygame.mixer.music.stop()
                print("Music stopped by user.")
                break
            pygame.time.Clock().tick(10)
        cv2.destroyWindow('Press q to quit')
    except Exception:
        pass

if __name__ == "__main__":
    print("Select mode:")
    print("1. Real-time emotion music player (webcam)")
    print("2. Single image capture and play")
    mode = input("Enter 1 or 2: ").strip()
    if mode == '1':
        real_time_emotion_music_player()
    elif mode == '2':
        main()
    else:
        print("Invalid option. Exiting.")

