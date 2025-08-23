def start_ffplay(path, from_pos=0):
    """Start ffplay at a given position (in ms), track the process, and return it."""
    global _ffplay_procs
    import subprocess
    ffplay_cmd = [
        'ffplay', '-nodisp', '-autoexit', '-loglevel', 'error'
    ]
    if from_pos > 0:
        ffplay_cmd += ['-ss', str(from_pos/1000.0)]
    ffplay_cmd.append(path)
    try:
        proc = subprocess.Popen(
            ffplay_cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
        )
        _ffplay_procs.append(proc)
        return proc
    except Exception as e:
        print(f"[media_handler] Failed to start ffplay: {e}")
        return None
import subprocess
from PIL import Image
from pydub import AudioSegment
import simpleaudio as sa


# Track all ffplay processes
_ffplay_procs = []

def stop_audio():
    global _ffplay_procs
    for proc in _ffplay_procs:
        try:
            proc.terminate()
            print("[DEBUG media_handler] ffplay process terminated.", flush=True)
        except Exception as e:
            print(f"[DEBUG media_handler] Error terminating ffplay: {e}", flush=True)
    _ffplay_procs.clear()

def load_image(path):
    """Load and return an image object."""
    return Image.open(path)

def play_audio(path):
    """Play an audio file (wav/mp3/ogg/opus) using ffplay as a subprocess."""
    global _ffplay_procs
    print(f"[DEBUG media_handler] TOP of play_audio for: {path}")
    stop_audio()
    print(f"[DEBUG] Playing audio: {path}")
    print(f"[DEBUG media_handler] Before try block in play_audio")
    try:
        print(f"[DEBUG media_handler] About to run ffplay via start_ffplay: {path}")
        proc = start_ffplay(path)
        if proc:
            print(f"[DEBUG media_handler] ffplay process started: {proc.pid}")
        else:
            print(f"[DEBUG media_handler] ffplay failed to start.")
    except Exception as e:
        print(f"[DEBUG media_handler] Exception in play_audio: {e}")
        import traceback
        print(f"[DEBUG media_handler] Error starting ffplay: {e}\n{traceback.format_exc()}")
