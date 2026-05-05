import subprocess
import re
import sys
import os
from utils import createFolder, checkFileExists


def getInfo(url, courseName, className):
    """
    Downloads a video using ffmpeg directly from the HLS/M3U8 URL.
    ffmpeg handles all segment downloads internally with proper headers,
    avoiding 403 errors and manual segment management.
    """
    folderPath = f"videos/{courseName}/{className}"
    outputFile = f"{folderPath}/{className}.mp4"
    createFolder("\\" + folderPath)

    if checkFileExists(f"\\videos\\{courseName}\\{className}\\{className}.mp4"):
        print(f"The file {className} already exists")
        return None

    print(f"\nStarted downloading: {className}")

    headers_str = (
        "Referer: https://platzi.com/\r\n"
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
    )

    command = [
        "ffmpeg", "-y",
        "-headers", headers_str,
        "-protocol_whitelist", "file,tls,tcp,https,crypto",
        "-i", url,
        "-c:v", "copy",
        "-c:a", "aac",
        "-bsf:a", "aac_adtstoasc",
        "-movflags", "+faststart",
        outputFile,
    ]

    process = subprocess.Popen(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )

    duration = None
    duration_pattern = re.compile(r"Duration: (\d{2}):(\d{2}):(\d{2})\.(\d{2})")
    progress_pattern = re.compile(r"time=(\d{2}):(\d{2}):(\d{2})\.(\d{2})")

    for line in iter(process.stderr.readline, b""):
        line = line.decode("utf-8", errors="replace")
        dm = duration_pattern.search(line)
        if dm:
            h, m, s, ms = map(int, dm.groups())
            duration = h * 3600 + m * 60 + s + ms / 100
        pm = progress_pattern.search(line)
        if pm and duration:
            h, m, s, ms = map(int, pm.groups())
            current = h * 3600 + m * 60 + s + ms / 100
            pct = min((current / duration) * 100, 100)
            bar_len = 50
            filled = int(pct * bar_len // 100)
            bar = "█" * filled + "░" * (bar_len - filled)
            sys.stdout.write(f"\r[{bar}] {pct:.1f}%")
            sys.stdout.flush()

    process.stderr.close()
    process.wait()
    sys.stdout.write("\n")
    sys.stdout.flush()

    if process.returncode != 0:
        print(f"ERROR downloading {className}")
        if os.path.exists(outputFile):
            os.remove(outputFile)
        return className

    return None
