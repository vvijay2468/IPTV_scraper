import subprocess
import shutil

def play_url(url: str):
    vlc_path = shutil.which("vlc")

    if not vlc_path:
        print("[!] VLC not found in PATH")
        return False, "VLC not installed"

    try:
        proc = subprocess.Popen(
            [vlc_path, url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True, "Player launched"
    except Exception as e:
        return False, str(e)
