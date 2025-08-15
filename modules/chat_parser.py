import re
from typing import List, Dict

def parse_chat_file(file_path: str) -> List[Dict]:
    """
    Parse WhatsApp exported .txt file and return a list of messages.
    Each message is a dict with keys: sender, time, text, media (optional)
    """
    messages = []
    # WhatsApp export line example:
    # 25.5.2025, 19:57 - שם: הודעה
    msg_pattern = re.compile(r"^(\d{1,2}\.\d{1,2}\.\d{4}), (\d{1,2}:\d{2}) - (.*?): (.*)$")
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            match = msg_pattern.match(line)
            if match:
                date, time, sender, text = match.groups()
                messages.append({
                    'sender': sender,
                    'time': f"{date} {time}",
                    'text': text
                })
            elif messages and line:
                # Multiline message: append to last
                messages[-1]['text'] += '\n' + line
    return messages
