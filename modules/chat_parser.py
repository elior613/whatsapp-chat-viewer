import re
from typing import List, Dict

def parse_chat_file(file_path: str) -> List[Dict]:
    """
    Parse WhatsApp exported .txt file and return a list of messages.
    Each message is a dict with keys: sender, time, text, media (optional), media_type (optional)
    Media files are detected by filename patterns in the message text.
    """
    messages = []
    # WhatsApp export line example:
    # 25.5.2025, 19:57 - שם: הודעה
    msg_pattern = re.compile(r"^(\d{1,2}\.\d{1,2}\.\d{4}), (\d{1,2}:\d{2}) - (.*?): (.*)$")
    # Pattern for media: FILENAME.EXT (קובץ מצורף)
    attached_pattern = re.compile(r"([\w\-]+\.(?:jpg|jpeg|png|gif|bmp|opus|ogg|mp3|wav|m4a)) \(קובץ מצורף\)", re.IGNORECASE)
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            match = msg_pattern.match(line)
            if match:
                date, time, sender, text = match.groups()
                msg = {
                    'sender': sender,
                    'time': f"{date} {time}",
                    'text': text
                }
                # Detect media (Hebrew export)
                attached_match = attached_pattern.search(text)
                if attached_match:
                    filename = attached_match.group(1)
                    msg['media'] = filename
                    ext = filename.lower().split('.')[-1]
                    if ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                        msg['media_type'] = 'image'  # Used by media_handler.load_image
                    elif ext in ['opus', 'ogg', 'mp3', 'wav', 'm4a']:
                        msg['media_type'] = 'audio'  # Used by media_handler.play_audio
                messages.append(msg)
                print(msg,  flush=True )
            elif messages and line:
                # Multiline message: append to last
                messages[-1]['text'] += '\n' + line
    return messages
