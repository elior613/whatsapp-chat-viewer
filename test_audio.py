from pydub import AudioSegment
import simpleaudio as sa
import sys
import os

# Usage: python test_audio.py <audiofile>
if len(sys.argv) < 2:
    print("Usage: python test_audio.py <audiofile>")
    sys.exit(1)

path = sys.argv[1]
if not os.path.exists(path):
    print(f"File not found: {path}")
    sys.exit(1)

print(f"[DEBUG] Loading audio: {path}")
audio = AudioSegment.from_file(path)
import io
wav_io = io.BytesIO()
audio.export(wav_io, format="wav")
wav_io.seek(0)
import wave
with wave.open(wav_io, 'rb') as wf:
    data = wf.readframes(wf.getnframes())
    print(f"[DEBUG] Playing audio...")
    play_obj = sa.play_buffer(
        data,
        num_channels=wf.getnchannels(),
        bytes_per_sample=wf.getsampwidth(),
        sample_rate=wf.getframerate()
    )
    play_obj.wait_done()
    print(f"[DEBUG] Playback finished.")
