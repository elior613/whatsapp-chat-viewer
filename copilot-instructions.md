# Copilot Instructions for WhatsApp Chat Desktop Viewer (Python + PySide6)

## 🧠 Project Goal
This is a local desktop application (not web-based) for viewing WhatsApp chat exports with a WhatsApp-style UI.

The app:
- Parses exported WhatsApp `.txt` files
- Displays messages chronologically, in a WhatsApp-like "chat bubble" UI
- Supports text, images, and audio messages
- Runs fully offline (no internet required)

---

## ⚙️ Tech Stack
- **Language**: Python 3.10+
- **GUI Framework**: PySide6 (Qt for Python)
- **File Parsing**: Built-in `re`, `os`, and optionally `chardet`
- **Media Handling**:
  - Images: `Pillow`
  - Audio: `pydub` and `simpleaudio`

---

## 🧑‍💻 Code Style
- Modular Python code (separate parser/UI/modules)
- Use classes for screens/windows
- UI built using Qt Widgets (not QML)
- Functions must include docstrings
- Add comments for logic-heavy sections
- Organize layout using QVBoxLayout, QHBoxLayout, QScrollArea

---

## 🧩 Components
- `MainWindow`: Loads and displays chats
- `ChatParser`: Parses `.txt` files line-by-line
- `MessageBubble`: Custom widget to display message (aligned left/right)
- `MediaHandler`: Handles voice/image rendering
- `ChatListView`: Scrollable chat history

---

## 📝 Chat File Format Example
-04/08/2025, 21:30 - David: What's up?
-04/08/2025, 21:31 - You: Nothing much.
-04/08/2025, 21:32 - David: [Voice message: PTT-20250804-WA0001.opus]


---

## 📦 Dependencies (PyPI)
- `PySide6`
- `pillow`
- `pydub`
- `simpleaudio`
- `chardet` (optional)

---

## 🛠️ Key Features
- [ ] Load `.txt` file via file dialog
- [ ] Parse and format messages by date/sender
- [ ] Align messages based on sender
- [ ] Render voice notes and images
- [ ] Scrollable chat layout


---

