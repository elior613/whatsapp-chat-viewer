from PIL import Image
from pydub import AudioSegment
import simpleaudio as sa

def load_image(path):
    """Load and return an image object."""
    return Image.open(path)

def play_audio(path):
    """Play an audio file (wav/mp3/ogg)."""
    audio = AudioSegment.from_file(path)
    play_obj = sa.play_buffer(
        audio.raw_data,
        num_channels=audio.channels,
        bytes_per_sample=audio.sample_width,
        sample_rate=audio.frame_rate
    )
    play_obj.wait_done()
