
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QWidget,
    QScrollArea, QHBoxLayout, QLabel, QSizePolicy, QToolButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from modules.chat_parser import parse_chat_file
from modules.media_handler import load_image, play_audio
import os

class ChatBubble(QWidget):
    def __init__(self, sender, text, time, is_own=False, media=None, media_type=None, media_dir=None):
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
        # Media rendering
        if media and media_type:
            media_path = os.path.join(media_dir, media) if media_dir else media
            print(f"[DEBUG] Trying to load media: {media_path} (type: {media_type})", flush=True)
            if media_type == "image":
                try:
                    pixmap = QPixmap(media_path)
                    img_label = QLabel()
                    img_label.setPixmap(pixmap.scaledToWidth(200, Qt.SmoothTransformation))
                    img_label.setStyleSheet("margin-top: 6px; margin-bottom: 6px; border-radius: 8px;")
                    layout.addWidget(img_label)
                except Exception as e:
                    print(f"[ERROR] Failed to load image: {media_path} | {e}", flush=True)
                    err_label = QLabel(f"[Image not found: {media}]")
                    layout.addWidget(err_label)
            elif media_type == "audio":
                import threading
                audio_btn = QToolButton()
                audio_btn.setText("▶️ Play Voice")
                def play():
                    from PySide6.QtWidgets import QMessageBox
                    import traceback
                    def play_in_thread():
                        try:
                            print(f"[DEBUG] Playing audio: {media_path}", flush=True)
                            play_audio(media_path)
                            print(f"[DEBUG] Audio playback finished: {media_path}", flush=True)
                        except Exception as e:
                            tb = traceback.format_exc()
                            print(f"[ERROR] Failed to play audio: {media_path} | {e}\n{tb}", flush=True)
                            def show_error():
                                msg_box = QMessageBox()
                                msg_box.setIcon(QMessageBox.Critical)
                                msg_box.setWindowTitle("Audio Playback Error")
                                msg_box.setText(f"Failed to play audio file:\n{media_path}\n\nError: {e}\n\nTraceback:\n{tb}")
                                msg_box.setDetailedText(tb)
                                msg_box.exec()
                            from PySide6.QtCore import QTimer
                            QTimer.singleShot(0, show_error)
                    threading.Thread(target=play_in_thread, daemon=True).start()
                audio_btn.clicked.connect(play)
                layout.addWidget(audio_btn)
        layout.addWidget(time_label)
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

class ChatViewerApp:
    def __init__(self):
        self.app = QApplication([])
        self.window = QMainWindow()
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
        self.media_dir = None

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self.window, "Open WhatsApp Chat", "", "Text Files (*.txt)")
        if file_path:
            self.media_dir = os.path.dirname(file_path)
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
                    media = msg.get('media')
                    media_type = msg.get('media_type')
                    is_own = (sender.strip() == "אליאור טקאץ'")
                    bubble = ChatBubble(sender, text, time, is_own, media, media_type, self.media_dir)
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
