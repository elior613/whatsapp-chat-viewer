from PIL import Image
from pydub import AudioSegment
import simpleaudio as sa

def load_image(path):
    """Load and return an image object."""
    return Image.open(path)

def play_audio(path):
    """Play an audio file (wav/mp3/ogg/opus)."""
    audio = AudioSegment.from_file(path)
    # Export to WAV bytes in memory
    import io
    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)
    # Play using simpleaudio
    import wave
    with wave.open(wav_io, 'rb') as wf:
        data = wf.readframes(wf.getnframes())
        play_obj = sa.play_buffer(
            data,
            num_channels=wf.getnchannels(),
            bytes_per_sample=wf.getsampwidth(),
            sample_rate=wf.getframerate()
        )
        play_obj.wait_done()
