#!/usr/bin/env python3
"""
Audio conversion and clipping utility.
Usage:
    python audio_tool.py convert <input> [output]
    python audio_tool.py clip <input> <start> <end> [output]
    python audio_tool.py info <file>
"""

import sys
import os
import subprocess
from pathlib import Path

def ensure_imghdr():
    """Create imghdr module for Python 3.13+ if missing."""
    try:
        import imghdr
        return
    except ImportError:
        pass
    
    site_packages = None
    for path in sys.path:
        if 'site-packages' in path and 'Python' in path:
            site_packages = Path(path)
            break
    
    if not site_packages:
        return
    
    imghdr_dir = site_packages / 'imghdr'
    imghdr_dir.mkdir(exist_ok=True)
    
    init_file = imghdr_dir / '__init__.py'
    if not init_file.exists():
        init_file.write_text('''"""imghdr replacement for Python 3.13+"""

def test_jpeg(h, f):
    if h[:3] == b'\\xff\\xd8\\xff':
        return 'jpeg'
    if h[:6] == b'\\xff\\xd8\\xff\\xe0\\x00\\x10':
        return 'jpeg'
    return None

def test_png(h, f):
    if h[:8] == b'\\x89PNG\\r\\n\\x1a\\n':
        return 'png'
    return None

def test_gif(h, f):
    if h[:6] in (b'GIF87a', b'GIF89a'):
        return 'gif'
    return None

def test_bmp(h, f):
    if h[:4] == b'BM':
        return 'bmp'
    return None

tests = [test_jpeg, test_png, test_gif, test_bmp]

def what(file, h=None):
    if h is None:
        with open(file, 'rb') as f:
            h = f.read(32)
    for t in tests:
        try:
            res = t(h, None)
            if res:
                return res
        except Exception:
            pass
    return None
''')


def convert_ncm(input_path, output_path=None):
    """Convert NCM to MP3."""
    ensure_imghdr()
    
    from ncmdump import NeteaseCloudMusicFile
    
    input_path = Path(input_path)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        return False
    
    if output_path is None:
        output_path = input_path.with_suffix('.mp3')
    else:
        output_path = Path(output_path)
    
    try:
        ncm = NeteaseCloudMusicFile(str(input_path))
        ncm.decrypt()
        ncm.dump_music(str(output_path))
        print(f"Converted: {input_path.name} -> {output_path.name}")
        return True
    except Exception as e:
        print(f"Error converting {input_path.name}: {e}")
        return False


def clip_audio(input_path, start_sec, end_sec, output_path=None):
    """Clip audio file from start_sec to end_sec."""
    input_path = Path(input_path)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        return False
    
    if output_path is None:
        output_path = input_path.with_name(
            f"{input_path.stem}_clip_{start_sec}s-{end_sec}s{input_path.suffix}"
        )
    else:
        output_path = Path(output_path)
    
    try:
        cmd = [
            'ffmpeg', '-i', str(input_path),
            '-ss', str(start_sec), '-to', str(end_sec),
            '-c', 'copy', str(output_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Clipped: {output_path.name} ({end_sec - start_sec}s)")
            return True
        else:
            print(f"Error: {result.stderr}")
            return False
    except FileNotFoundError:
        print("Error: FFmpeg not found. Please install FFmpeg.")
        return False


def get_audio_info(file_path):
    """Get audio file information."""
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        return
    
    ext = file_path.suffix.lower()
    
    try:
        if ext == '.mp3':
            from mutagen.mp3 import MP3
            audio = MP3(str(file_path))
            print(f"File: {file_path.name}")
            print(f"Duration: {audio.info.length:.2f}s ({audio.info.length/60:.2f}min)")
            print(f"Bitrate: {audio.info.bitrate // 1000}kbps")
            print(f"Sample rate: {audio.info.sample_rate}Hz")
        elif ext == '.flac':
            from mutagen.flac import FLAC
            audio = FLAC(str(file_path))
            print(f"File: {file_path.name}")
            print(f"Duration: {audio.info.length:.2f}s ({audio.info.length/60:.2f}min)")
            print(f"Channels: {audio.info.channels}")
            print(f"Sample rate: {audio.info.sample_rate}Hz")
        elif ext == '.ncm':
            ensure_imghdr()
            from ncmdump import NeteaseCloudMusicFile
            ncm = NeteaseCloudMusicFile(str(file_path))
            print(f"File: {file_path.name}")
            print(f"Format: NCM (NetEase Cloud Music)")
        else:
            # Use ffprobe
            cmd = ['ffprobe', '-v', 'error', '-show_entries', 
                   'format=duration,bit_rate:stream=sample_rate,channels',
                   '-of', 'default=noprint_wrappers=1', str(file_path)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(result.stdout)
    except Exception as e:
        print(f"Error reading file info: {e}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    
    if cmd == 'convert' and len(sys.argv) >= 3:
        input_path = sys.argv[2]
        output_path = sys.argv[3] if len(sys.argv) >= 4 else None
        success = convert_ncm(input_path, output_path)
        sys.exit(0 if success else 1)
    
    elif cmd == 'clip' and len(sys.argv) >= 5:
        input_path = sys.argv[2]
        start_sec = float(sys.argv[3])
        end_sec = float(sys.argv[4])
        output_path = sys.argv[5] if len(sys.argv) >= 6 else None
        success = clip_audio(input_path, start_sec, end_sec, output_path)
        sys.exit(0 if success else 1)
    
    elif cmd == 'info' and len(sys.argv) >= 3:
        get_audio_info(sys.argv[2])
    
    else:
        print("Usage:")
        print("  python audio_tool.py convert <input.ncm> [output.mp3]")
        print("  python audio_tool.py clip <input.mp3> <start_sec> <end_sec> [output.mp3]")
        print("  python audio_tool.py info <audio_file>")
        sys.exit(1)


if __name__ == '__main__':
    main()
