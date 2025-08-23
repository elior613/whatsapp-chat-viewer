
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QWidget,
    QScrollArea, QHBoxLayout, QLabel, QSizePolicy, QSlider
)
from PySide6.QtCore import Qt, QTimer
from modules.chat_parser import parse_chat_file
from modules.media_handler import play_audio, stop_audio
import os


# WhatsApp-style audio bubble widget

class AudioBubble(QWidget):
    _current_audio = None  # Class variable to track currently playing audio

    def __init__(self, sender, time, audio_path, duration, is_own=False):
        super().__init__()
        self.audio_path = audio_path
        self.duration = duration
        self.is_playing = False
        self.timer = QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_progress)
        self.progress = 0
        self._seeking = False

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 2, 10, 2)
        layout.setSpacing(8)

        self.play_btn = QPushButton()
        self.play_btn.setText('▶')
        self.play_btn.setFixedSize(32, 32)
        self.play_btn.setStyleSheet('border-radius: 16px; background: #ece5dd; font-size: 18px;')
        self.play_btn.clicked.connect(self.toggle_play)
        layout.addWidget(self.play_btn)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(int(duration * 1000))
        self.slider.setValue(0)
        self.slider.setSingleStep(1000)
        self.slider.setPageStep(5000)
        self.slider.setFixedWidth(180)
        self.slider.setStyleSheet('QSlider::groove:horizontal {height: 6px; background: #ddd; border-radius: 3px;} QSlider::handle:horizontal {background: #25d366; border: 1px solid #25d366; width: 12px; margin: -4px 0; border-radius: 6px;}')
        self.slider.sliderPressed.connect(self.start_seek)
        self.slider.sliderReleased.connect(self.end_seek)
        self.slider.sliderMoved.connect(self.seek_preview)
        layout.addWidget(self.slider)

        self.time_label = QLabel(self.format_time(0) + ' / ' + self.format_time(duration))
        self.time_label.setStyleSheet("font-size: 11px; color: #888;")
        layout.addWidget(self.time_label)

        layout.addStretch()

        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

    def format_time(self, seconds):
        m, s = divmod(int(seconds), 60)
        return f"{m}:{s:02d}"

    def toggle_play(self):
        if self.is_playing:
            self.pause_audio()
        else:
            self.play_audio(from_pos=self.progress)

    def play_audio(self, from_pos=0):
        # Stop any other audio bubble and any previous process for this bubble
        if AudioBubble._current_audio and AudioBubble._current_audio is not self:
            AudioBubble._current_audio.pause_audio()
        AudioBubble._current_audio = self
        # Stop all previous ffplay processes
        from modules.media_handler import stop_audio, start_ffplay
        stop_audio()
        self._proc = start_ffplay(self.audio_path, from_pos=from_pos)
        self.is_playing = True
        self.play_btn.setText('⏸')
        self.timer.start()

    def pause_audio(self):
        # Stop this bubble's process if running
        if hasattr(self, '_proc') and self._proc is not None:
            try:
                self._proc.terminate()
            except Exception:
                pass
            self._proc = None
        stop_audio()
        self.is_playing = False
        self.play_btn.setText('▶')
        self.timer.stop()

    def update_progress(self):
        if self.is_playing and not self._seeking:
            self.progress += 500
            if self.progress >= self.duration * 1000:
                self.progress = self.duration * 1000
                self.pause_audio()
            self.slider.setValue(int(self.progress))
            self.time_label.setText(self.format_time(self.progress/1000) + ' / ' + self.format_time(self.duration))

    def start_seek(self):
        self._seeking = True

    def seek_preview(self, value):
        # Update label while dragging
        self.time_label.setText(self.format_time(value/1000) + ' / ' + self.format_time(self.duration))

    def end_seek(self):
        self.progress = self.slider.value()
        self._seeking = False
        if self.is_playing:
            self.play_audio(from_pos=self.progress)

    def stop(self):
        self.pause_audio()

class ChatBubble(QWidget):
    def __init__(self, sender, text, time, is_own=False):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 2, 10, 2)
        layout.setSpacing(2)
        sender_label = QLabel(sender)
        sender_label.setStyleSheet("font-weight: bold; color: #388e3c;" if is_own else "font-weight: bold; color: #1976d2;")
        text_label = QLabel(text)
        text_label.setWordWrap(True)
        text_label.setStyleSheet(f"background: {'#dcf8c6' if is_own else '#f7f7f7'}; border-radius: 12px; padding: 8px; font-size: 14px; border: 1px solid #ddd;")
        time_label = QLabel(time)
        time_label.setStyleSheet("font-size: 10px; color: #888;")
        time_label.setAlignment(Qt.AlignRight)
        layout.addWidget(sender_label)
        layout.addWidget(text_label)
        layout.addWidget(time_label)
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

class ChatViewerMainWindow(QMainWindow):
    def closeEvent(self, event):
        from modules.media_handler import stop_audio
        stop_audio()
        super().closeEvent(event)

class ChatViewerApp:
    def __init__(self):
        self.app = QApplication([])
        self.window = ChatViewerMainWindow()
        self.window.setWindowTitle("WhatsApp Chat Viewer")
        # Set chat background color (light gray)
        self.window.setStyleSheet("background-color: #ece5dd;")
        self.open_btn = QPushButton("Open Chat File")
        self.open_btn.clicked.connect(self.open_file)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_container.setLayout(self.chat_layout)
        self.scroll_area.setWidget(self.chat_container)
        layout = QVBoxLayout()
        layout.addWidget(self.open_btn)
        layout.addWidget(self.scroll_area)
        container = QWidget()
        container.setLayout(layout)
        self.window.setCentralWidget(container)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self.window, "Open WhatsApp Chat", "", "Text Files (*.txt)")
        if file_path:
            messages = parse_chat_file(file_path)
            # Clear previous chat
            for i in reversed(range(self.chat_layout.count())):
                widget = self.chat_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
            if messages:
                for msg in messages:
                    sender = msg.get('sender', 'Unknown')
                    time = msg.get('time', '')
                    text = msg.get('text', '')
                    is_own = (sender.strip() == "אליאור טקאץ'")

                    # Show audio bubble if media_type is audio
                    if msg.get('media_type') == 'audio' and msg.get('media'):
                        audio_path = msg['media']
                        if not os.path.isabs(audio_path):
                            audio_path = os.path.join(os.path.dirname(file_path), audio_path)
                        duration = 20
                        try:
                            from pydub.utils import mediainfo
                            info = mediainfo(audio_path)
                            duration = float(info['duration'])
                        except Exception:
                            pass
                        bubble = AudioBubble(sender, time, audio_path, duration, is_own)
                    # Show image if media_type is image
                    elif msg.get('media_type') == 'image' and msg.get('media'):
                        from modules.media_handler import load_image
                        image_path = msg['media']
                        if not os.path.isabs(image_path):
                            image_path = os.path.join(os.path.dirname(file_path), image_path)
                        image_widget = QLabel()
                        try:
                            from PySide6.QtGui import QPixmap
                            img = load_image(image_path)
                            qimg = QPixmap(image_path)
                            # Optionally scale for chat bubble size
                            qimg = qimg.scaledToWidth(200, Qt.SmoothTransformation)
                            image_widget.setPixmap(qimg)
                        except Exception as e:
                            image_widget.setText(f"[Image not found: {os.path.basename(image_path)}]")
                        # Compose a bubble with image and text
                        bubble = ChatBubble(sender, text, time, is_own)
                        # Insert image above text
                        bubble.layout().insertWidget(1, image_widget)
                    else:
                        bubble = ChatBubble(sender, text, time, is_own)

                    row = QHBoxLayout()
                    row.setContentsMargins(0, 0, 0, 0)
                    if is_own:
                        row.addWidget(bubble)
                        row.addStretch()
                    else:
                        row.addStretch()
                        row.addWidget(bubble)
                    row_widget = QWidget()
                    row_widget.setLayout(row)
                    self.chat_layout.addWidget(row_widget)
            else:
                label = QLabel("No messages found or failed to parse file.")
                self.chat_layout.addWidget(label)

    def run(self):
        self.window.show()
        self.app.exec()
