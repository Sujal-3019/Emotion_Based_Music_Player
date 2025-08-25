<!-- Animated Emotional Music Banner -->
<p align="center">
  <img src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExY2p0ZGV6bHhrdWppNXRxaWI0M3l0bGJhNmlsNW5mYWJqdGtqeTYydyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/R7QHeNBW4gO1VwAQOI/giphy.gif" width="340" alt="Animated Music Emotions" />
</p>

<h1 align="center">🎶 Emotion-Based Music Player</h1>
<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=24&pause=1300&width=700&lines=Let+your+feelings+choose+your+music!;Real-time+emotion+detection+via+webcam.;AI-powered+playlist+matching.;Enjoy+a+musical+mood+journey..." alt="Typing SVG" />
</p>

---

## ✨ Overview

**Emotion-Based Music Player** is an innovative Python app that uses AI-powered facial emotion detection to select and play songs that match how you feel!  
The app supports both real-time webcam analysis and single-photo capture.  
Each emotion (happy, sad, angry, neutral, surprise, fear, disgust) launches a matching song from the `songs/` folder for a personalized, immersive music experience.

---

## 🚀 Features

- Analyze your facial emotions in real-time using your webcam
- Plays a custom song for each emotion detected (happy, sad, angry, etc.) from your `local storage`
- Smooth and responsive GUI with playback controls (pause, resume, stop, timeline)
- Supports both single image mode and continuous detection mode
- Easy setup: just put your MP3 tracks in the `songs` folder using the given naming convention

---

## 🛠 Technologies

- `Python` | `OpenCV` | `deepface` | `pygame` | `Tkinter`
- AI models (via `deepface`) assist in precise emotion recognition
- GUI theme inspired by modern, minimal dark color palettes

---

## 🌈 How It Works

1. Launch the script (`emotion_music_player.py` for CLI, `emotion_music_player_gui.py` for GUI).
2. Choose a mode: real-time emotion tracking or single image capture.
3. The app detects your current emotion (happy, sad, angry, neutral, surprise, fear, or disgust).
4. A song tailored for your emotion is played from the `songs/` folder.
5. Playback and timeline controls let you pause, resume, or stop music anytime.

---
EmotionMusicPlayer/ <br>
│ <br>
├── emotion_music_player.py # CLI Version <br>
├── emotion_music_player_gui.py # GUI Version <br>
├── requirements.txt # Dependencies <br>
├── songs/ # Folder for all emotion MP3 files  <br>
│ ├── happy.mp3 <br>
│ ├── sad.mp3 <br>
│ ├── angry.mp3 <br>
│ ├── neutral.mp3 <br>
│ ├── fear.mp3 <br>
│ ├── surprise.mp3 <br>
│ ├── disgust.mp3 <br>
│ └── ... (all in the 'songs' folder)


---

## 🎵 Song Mapping

- Ensure **all MP3 files** for emotions are in the `songs/` folder:
  - `songs/happy.mp3`
  - `songs/sad.mp3`
  - `songs/angry.mp3`
  - `songs/neutral.mp3`
  - `songs/fear.mp3`
  - `songs/surprise.mp3`
  - `songs/disgust.mp3`
- If an emotion MP3 is missing, the script will play a fallback (usually `happy.mp3` or `angry.mp3`).

---

## ⚡ Installation & Usage

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Launch the player:
- For CLI:  
  ```
  python emotion_music_player.py
  ```
- For GUI:  
  ```
  python emotion_music_player_gui.py
  ```
3. Make sure your music files are correctly named and stored inside the `songs/` folder.

---

## 🤖 About AI Assistance

This project was built with the creative and technical support of artificial intelligence (AI) tools, including deep learning models for emotion detection, and coding assistants for structure and design.  
Collaborating with AI helped streamline coding, problem-solving, and optimize user experience.

---

## ✨ Credits

- Face emotion detection: [DeepFace](https://github.com/serengil/deepface)
- Music playback: [pygame](https://www.pygame.org/)
- GUI: [Tkinter](https://docs.python.org/3/library/tkinter.html)
- Thanks to open-source and AI communities!

---

## ⭐️ Love this project?

Please star ⭐ the repo, share with friends, and make some music with AI and Python!
