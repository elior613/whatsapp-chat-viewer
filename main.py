from modules.chat_parser import parse_chat_file
from modules.media_handler import load_image, play_audio
from modules.gui import ChatViewerApp

if __name__ == "__main__":
    app = ChatViewerApp()
    app.run()
