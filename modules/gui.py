from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QWidget,
    QScrollArea, QHBoxLayout, QLabel, QSizePolicy
)
from PySide6.QtCore import Qt
from modules.chat_parser import parse_chat_file

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
