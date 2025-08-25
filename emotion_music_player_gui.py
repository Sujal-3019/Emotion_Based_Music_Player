import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
from deepface import DeepFace
import pygame
import threading
import os
import numpy as np
import time

EMOTION_MUSIC_MAP = {
    'happy': 'musics/happy.mp3',
    'sad': 'musics/sad.mp3',
    'angry': 'musics/anger.mp3',
    'surprise': 'musics/happy.mp3',
    'neutral': 'musics/neutral.mp3',
    'fear': 'musics/fear.mp3',
    'disgust': 'musics/anger.mp3'
}

class EmotionMusicPlayerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Emotion Based Music Player")
        self.root.geometry("600x550")
        self.root.configure(bg="#393E46")
        self.webcam_on = False
        self.captured_image = None
        self.emotion_icon = None
        self.music_playing = False
        self.music_paused = False
        self.music_length = 0
        self.music_update_job = None
        self.setup_ui()
        pygame.mixer.init()

    def setup_ui(self):
        self.title_label = tk.Label(self.root, text="Emotion Based Music Player", font=("Arial", 22, "bold"), fg="#FFD369", bg="#393E46", bd=2, relief="groove")
        self.title_label.pack(pady=20, ipadx=10, ipady=5)

        self.mode_frame = tk.Frame(self.root, bg="#393E46")
        self.mode_frame.pack(pady=10)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 12, 'bold'), foreground='#222831', background='#FFD369', borderwidth=2, focusthickness=3, focuscolor='none')
        style.map('TButton', background=[('active', '#FFB347')], foreground=[('active', '#222831')])
        style.configure('TScale', background='#393E46', troughcolor='#FFD369', sliderthickness=20)

        self.btn_realtime = ttk.Button(self.mode_frame, text="🎥 Real-time Mode", command=self.start_realtime_mode)
        self.btn_realtime.grid(row=0, column=0, padx=15, ipadx=10, ipady=5)
        self.btn_single = ttk.Button(self.mode_frame, text="📸 Single Image Mode", command=self.start_single_mode)
        self.btn_single.grid(row=0, column=1, padx=15, ipadx=10, ipady=5)

        self.canvas = tk.Canvas(self.root, width=320, height=240, bg="#FFD369", highlightthickness=4, highlightbackground="#222831")
        self.canvas.pack(pady=20)

        self.capture_btn = ttk.Button(self.root, text="📷 Capture Image", command=self.capture_image)
        self.capture_btn.pack(pady=5, ipadx=10, ipady=5)
        self.capture_btn.config(state=tk.DISABLED)

        self.emotion_label = tk.Label(self.root, text="", font=("Arial", 16, "bold"), fg="#393E46", bg="#FFD369", bd=2, relief="ridge")
        self.emotion_label.pack(pady=10, ipadx=10, ipady=5)

        self.progress = ttk.Progressbar(self.root, mode='indeterminate', style='TProgressbar')
        self.progress.pack(pady=5)
        self.progress.pack_forget()

        btn_frame = tk.Frame(self.root, bg="#393E46")
        btn_frame.pack(pady=5)
        self.stop_btn = ttk.Button(btn_frame, text="⏹ Stop", command=self.stop_music)
        self.stop_btn.grid(row=0, column=0, padx=8, ipadx=10, ipady=5)
        self.stop_btn.config(state=tk.DISABLED)

        self.pause_btn = ttk.Button(btn_frame, text="⏸ Pause", command=self.pause_music)
        self.pause_btn.grid(row=0, column=1, padx=8, ipadx=10, ipady=5)
        self.pause_btn.config(state=tk.DISABLED)

        self.resume_btn = ttk.Button(btn_frame, text="▶️ Resume", command=self.resume_music)
        self.resume_btn.grid(row=0, column=2, padx=8, ipadx=10, ipady=5)
        self.resume_btn.config(state=tk.DISABLED)

        self.timeline = ttk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, length=400, state=tk.DISABLED, style='TScale')
        self.timeline.pack(pady=10)

        self.timeline_label = tk.Label(self.root, text="00:00 / 00:00", font=("Arial", 10, "bold"), fg="#FFD369", bg="#393E46")
        self.timeline_label.pack()

        self.root.configure(bg="#393E46")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def start_realtime_mode(self):
        self.webcam_on = True
        self.capture_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.resume_btn.config(state=tk.DISABLED)
        self.timeline.config(state=tk.DISABLED)
        self.emotion_label.config(text="")
        self.progress.pack_forget()
        self._realtime_loop()

    def start_single_mode(self):
        self.webcam_on = True
        self.capture_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.resume_btn.config(state=tk.DISABLED)
        self.timeline.config(state=tk.DISABLED)
        self.emotion_label.config(text="")
        self.progress.pack_forget()
        self._webcam_preview_loop()

    def _webcam_preview_loop(self):
        def update():
            if not self.webcam_on:
                return
            if not hasattr(self, 'cap') or self.cap is None:
                self.cap = cv2.VideoCapture(0)
            ret, frame = self.cap.read()
            if ret:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb)
                imgtk = ImageTk.PhotoImage(image=img.resize((320, 240)))
                self.canvas.imgtk = imgtk
                self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
                self.captured_image = frame
            self.root.after(30, update)
        update()

    def _realtime_loop(self):
        # Smooth webcam preview, analyze every 2 seconds in a background thread
        if not hasattr(self, 'cap') or self.cap is None:
            self.cap = cv2.VideoCapture(0)
        self._last_analysis_time = 0
        self._analyzing = False
        self._last_frame = None
        def update():
            if not self.webcam_on:
                if hasattr(self, 'cap') and self.cap:
                    self.cap.release()
                    self.cap = None
                return
            ret, frame = self.cap.read()
            if ret:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb)
                imgtk = ImageTk.PhotoImage(image=img.resize((320, 240)))
                self.canvas.imgtk = imgtk
                self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
                self._last_frame = frame
                now = time.time()
                # Only analyze every 2 seconds and if not already analyzing
                if now - self._last_analysis_time > 2 and not self._analyzing:
                    self._analyzing = True
                    img_path = 'captured_face.jpg'
                    cv2.imwrite(img_path, frame)
                    def detect():
                        try:
                            result = DeepFace.analyze(img_path=img_path, actions=['emotion'], enforce_detection=False)
                            emotion = result[0]['dominant_emotion']
                            if not hasattr(self, 'last_emotion') or emotion != self.last_emotion:
                                self.root.after(0, lambda: self.show_emotion(emotion))
                                self.root.after(0, lambda: self.play_music_for_emotion(emotion))
                                self.last_emotion = emotion
                        except Exception as e:
                            self.root.after(0, lambda: self.emotion_label.config(text=f"Error: {e}"))
                        finally:
                            self._analyzing = False
                            self._last_analysis_time = time.time()
                    threading.Thread(target=detect, daemon=True).start()
            self.root.after(30, update)
        update()

    def capture_image(self):
        if self.captured_image is not None:
            img_path = 'captured_face.jpg'
            cv2.imwrite(img_path, self.captured_image)
            self.progress.pack()
            self.progress.start()
            threading.Thread(target=self.detect_and_play, args=(img_path,), daemon=True).start()

    def detect_and_play(self, img_path):
        try:
            result = DeepFace.analyze(img_path=img_path, actions=['emotion'], enforce_detection=False)
            emotion = result[0]['dominant_emotion']
            self.show_emotion(emotion)
            self.play_music_for_emotion(emotion)
        except Exception as e:
            self.emotion_label.config(text=f"Error: {e}")
        finally:
            self.progress.stop()
            self.progress.pack_forget()

    def show_emotion(self, emotion):
        icon_path = f"icons/{emotion}.png"
        if os.path.exists(icon_path):
            img = Image.open(icon_path).resize((64, 64))
            self.emotion_icon = ImageTk.PhotoImage(img)
            self.canvas.create_image(160, 120, image=self.emotion_icon)
        self.emotion_label.config(text=f"Detected Emotion: {emotion.title()}")

    def play_music_for_emotion(self, emotion):
        emotion_key = emotion.strip().lower()
        music_file = EMOTION_MUSIC_MAP.get(emotion_key, EMOTION_MUSIC_MAP['happy'])
        if not os.path.exists(music_file):
            self.emotion_label.config(text=f"No music file for emotion: {emotion_key}")
            return
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play()
            self.music_playing = True
            self.music_paused = False
            self.stop_btn.config(state=tk.NORMAL)
            self.pause_btn.config(state=tk.NORMAL)
            self.resume_btn.config(state=tk.DISABLED)
            self.timeline.config(state=tk.NORMAL)
            self.music_length = self.get_music_length(music_file)
            self.timeline.config(to=self.music_length)
            self.update_timeline()
        except Exception as e:
            self.emotion_label.config(text=f"Error playing music: {e}")

    def get_music_length(self, music_file):
        try:
            import mutagen
            from mutagen.mp3 import MP3
            audio = MP3(music_file)
            return int(audio.info.length)
        except Exception:
            return 100

    def update_timeline(self):
        if not self.music_playing:
            self.timeline.set(0)
            self.timeline_label.config(text="00:00 / 00:00")
            return
        pos = pygame.mixer.music.get_pos() // 1000
        total = self.music_length
        self.timeline.set(pos)
        self.timeline_label.config(text=f"{self.format_time(pos)} / {self.format_time(total)}")
        if pygame.mixer.music.get_busy() and not self.music_paused:
            self.music_update_job = self.root.after(500, self.update_timeline)
        else:
            self.music_update_job = None

    def format_time(self, seconds):
        m, s = divmod(int(seconds), 60)
        return f"{m:02}:{s:02}"

    def pause_music(self):
        if self.music_playing and not self.music_paused:
            pygame.mixer.music.pause()
            self.music_paused = True
            self.pause_btn.config(state=tk.DISABLED)
            self.resume_btn.config(state=tk.NORMAL)

    def resume_music(self):
        if self.music_playing and self.music_paused:
            pygame.mixer.music.unpause()
            self.music_paused = False
            self.pause_btn.config(state=tk.NORMAL)
            self.resume_btn.config(state=tk.DISABLED)
            self.update_timeline()

    def stop_music(self):
        pygame.mixer.music.stop()
        self.music_playing = False
        self.music_paused = False
        self.webcam_on = False
        self.capture_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.DISABLED)
        self.resume_btn.config(state=tk.DISABLED)
        self.timeline.config(state=tk.DISABLED)
        if self.music_update_job:
            self.root.after_cancel(self.music_update_job)
            self.music_update_job = None
        self.timeline.set(0)
        self.timeline_label.config(text="00:00 / 00:00")
        if hasattr(self, 'cap') and self.cap:
            self.cap.release()
            self.cap = None

    def on_close(self):
        self.webcam_on = False
        pygame.mixer.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = EmotionMusicPlayerGUI(root)
    root.mainloop()
