---
name: audio-converter
description: Audio format conversion and clipping skill. Use when user wants to convert audio between formats (ncm to mp3/flac, mp3 to wav/aac/ogg, etc.) or clip/cut a segment from an audio file (e.g., "截取 29s-45s", "cut from 1:00 to 2:30"). Triggers on: ncm转换, 音频转换, 格式转换, 截取音频, 剪辑音频, audio convert, audio clip, cut audio, trim audio, extract audio segment. Also triggers when user provides an audio file path and mentions time ranges or format conversion.
---

# Audio Converter Skill

Convert audio formats and clip audio segments using FFmpeg and ncmdump.

## Supported Operations

### 1. NCM to MP3/FLAC Conversion

NCM is NetEase Cloud Music's proprietary format. Conversion requires the `ncmdump-py` library.

**Dependencies:**
- `pip install ncmdump-py` (includes mutagen for metadata handling)
- `imghdr` module (for Python 3.13+, create manually if missing)

**Conversion via Python API (handles Chinese filenames):**
```python
from ncmdump import NeteaseCloudMusicFile
from pathlib import Path

ncm_path = Path("path/to/file.ncm")
ncm = NeteaseCloudMusicFile(str(ncm_path))
ncm.decrypt()
output_path = str(ncm_path).replace('.ncm', '.mp3')
ncm.dump_music(output_path)
print(f"Converted: {output_path}")
```

**For Python 3.13+ (imghdr missing):** Create the imghdr module at:
`site-packages/imghdr/__init__.py` with image type detection functions.

### 2. Audio Clipping with FFmpeg

Extract a segment from any audio file using FFmpeg.

**Basic clip (29s to 45s):**
```bash
ffmpeg -i "input.mp3" -ss 29 -to 45 -c copy "output_clip.mp3"
```

**Clip with time format (HH:MM:SS):**
```bash
ffmpeg -i "input.mp3" -ss 00:01:30 -to 00:02:45 -c copy "output_clip.mp3"
```

**Clip from start to specific time:**
```bash
ffmpeg -i "input.mp3" -ss 0 -to 60 -c copy "output_first_60s.mp3"
```

**Clip from specific time to end:**
```bash
ffmpeg -i "input.mp3" -ss 120 -c copy "output_after_2min.mp3"
```

**Parameters:**
- `-ss <start>`: Start time (seconds or HH:MM:SS)
- `-to <end>`: End time (seconds or HH:MM:SS)
- `-c copy`: Stream copy (fast, no re-encoding)

### 3. Audio Format Conversion with FFmpeg

Convert between common audio formats.

**MP3 to WAV:**
```bash
ffmpeg -i "input.mp3" "output.wav"
```

**MP3 to AAC:**
```bash
ffmpeg -i "input.mp3" -c:a aac -b:a 192k "output.aac"
```

**MP3 to OGG:**
```bash
ffmpeg -i "input.mp3" -c:a libvorbis -q:a 4 "output.ogg"
```

**FLAC to MP3:**
```bash
ffmpeg -i "input.flac" -c:a libmp3lame -b:a 320k "output.mp3"
```

**Convert with specific bitrate:**
```bash
ffmpeg -i "input.mp3" -b:a 192k "output_192k.mp3"
```

**Preserve metadata:**
```bash
ffmpeg -i "input.mp3" -c copy "output.mp3"
```

### 4. Batch Conversion

Convert multiple files in a directory.

**All NCM files in directory:**
```python
from pathlib import Path
from ncmdump import NeteaseCloudMusicFile

ncm_dir = Path("path/to/ncm/files")
for ncm_file in ncm_dir.glob("*.ncm"):
    try:
        ncm = NeteaseCloudMusicFile(str(ncm_file))
        ncm.decrypt()
        output = str(ncm_file).replace('.ncm', '.mp3')
        ncm.dump_music(output)
        print(f"Converted: {ncm_file.name}")
    except Exception as e:
        print(f"Failed: {ncm_file.name} - {e}")
```

**All files of one type to MP3:**
```bash
for f in *.wav; do ffmpeg -i "$f" "${f%.wav}.mp3"; done
```

## Common Audio Formats and Codecs

| Format | Codec Option | Typical Extension |
|--------|-------------|-------------------|
| MP3 | `-c:a libmp3lame` | .mp3 |
| AAC | `-c:a aac` or `-c:a libfdk_aac` | .aac, .m4a |
| FLAC | `-c:a flac` | .flac |
| WAV | `-c:a pcm_s16le` | .wav |
| OGG | `-c:a libvorbis` | .ogg |
| OPUS | `-c:a libopus` | .opus |

## Workflows

### NCM → MP3 → Clip Segment

```python
# Step 1: Convert NCM to MP3
from ncmdump import NeteaseCloudMusicFile
from pathlib import Path
import subprocess

ncm_path = Path("song.ncm")
ncm = NeteaseCloudMusicFile(str(ncm_path))
ncm.decrypt()
mp3_path = str(ncm_path).replace('.ncm', '.mp3')
ncm.dump_music(mp3_path)

# Step 2: Clip the segment (29s-45s)
output_clip = mp3_path.replace('.mp3', '_clip_29s-45s.mp3')
subprocess.run([
    'ffmpeg', '-i', mp3_path,
    '-ss', '29', '-to', '45',
    '-c', 'copy', output_clip
])
print(f"Clipped: {output_clip}")
```

### Get Audio Info

```python
from mutagen.mp3 import MP3
from mutagen.flac import FLAC

# For MP3
audio = MP3("file.mp3")
print(f"Duration: {audio.info.length:.2f}s")
print(f"Bitrate: {audio.info.bitrate // 1000}kbps")
print(f"Sample rate: {audio.info.sample_rate}Hz")

# For FLAC
audio = FLAC("file.flac")
print(f"Duration: {audio.info.length:.2f}s")
print(f"Channels: {audio.info.channels}")
```

## Error Handling

**File not found (Chinese filenames on Windows):**
```python
from pathlib import Path

# Use glob to find file by pattern
ncm_dir = Path("path/to/dir")
files = list(ncm_dir.glob("*.ncm"))
target = next((f for f in files if 'keyword' in f.name), None)
```

**FFmpeg not found:**
```python
import shutil
if not shutil.which('ffmpeg'):
    print("FFmpeg not found. Please install FFmpeg and add to PATH.")
```

**Invalid time format:**
- Use seconds (29) or HH:MM:SS (00:00:29)
- FFmpeg accepts both

## Output Conventions

- Converted file: Same directory as original, same name with new extension
- Clipped file: Original name + `_clip_HHMMSS-HHMMSS` suffix
- Batch output: Same directory as originals (or specify `--output-dir`)

## Quick Reference

| Task | Command |
|------|---------|
| NCM → MP3 | `python -m ncmdump file.ncm` |
| Clip 29s-45s | `ffmpeg -i in.mp3 -ss 29 -to 45 -c copy out.mp3` |
| MP3 → WAV | `ffmpeg -i in.mp3 out.wav` |
| Get info | `ffprobe -v error -show_entries format=duration,bit_rate -of default=noprint_wrappers=1:nokey=1 in.mp3` |
