# Audio Converter

A versatile audio format conversion and clipping tool that supports NCM, MP3, WAV, AAC, FLAC, OGG, and more.

## Features

- 🎵 **NCM Format Conversion** - Convert NetEase Cloud Music (NCM) files to MP3/FLAC
- ✂️ **Audio Clipping** - Extract audio segments by time range
- 🔄 **Format Conversion** - Convert between MP3, WAV, AAC, FLAC, OGG, and other formats
- 📋 **Metadata Viewing** - View audio file info (duration, bitrate, sample rate)

## Installation

### Prerequisites

- Python 3.10+ (Python 3.10-3.12 recommended)
- FFmpeg (for audio clipping and format conversion)

### Install FFmpeg

**Windows:**
1. Download from https://ffmpeg.org/download.html
2. Extract to a directory (e.g., `C:\ffmpeg`)
3. Add `bin` directory to system PATH
4. Restart your terminal

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg  # Debian/Ubuntu
sudo yum install ffmpeg  # CentOS/RHEL
```

### Install Python Dependencies

```bash
pip install ncmdump-py
```

## Quick Start

### Convert NCM to MP3

```bash
python audio_tool.py convert "song.ncm"
```

### Clip Audio Segment

```bash
# Clip from 29s to 45s
python audio_tool.py clip "song.mp3" 29 45
```

### View Audio Info

```bash
python audio_tool.py info "song.mp3"
```

## Usage

```
python audio_tool.py <command> [arguments]

Commands:
  convert <input> [output]  - Convert NCM to MP3
  clip <input> <start> <end> [output]  - Extract audio segment
  info <file>  - Show audio file information
```

## Python API

### NCM to MP3 Conversion

```python
from ncmdump import NeteaseCloudMusicFile

ncm = NeteaseCloudMusicFile("song.ncm")
ncm.decrypt()
ncm.dump_music("song.mp3")
```

### Audio Clipping

```bash
ffmpeg -i "input.mp3" -ss 29 -to 45 -c copy "output.mp3"
```

### Format Conversion

```bash
# MP3 to WAV
ffmpeg -i input.mp3 output.wav

# MP3 to AAC
ffmpeg -i input.mp3 -c:a aac -b:a 192k output.aac

# FLAC to MP3
ffmpeg -i input.flac -c:a libmp3lame -b:a 320k output.mp3
```

## Supported Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| MP3 | .mp3 | Most common |
| WAV | .wav | Uncompressed |
| AAC | .aac, .m4a | Efficient compression |
| FLAC | .flac | Lossless |
| OGG | .ogg | Open source |
| OPUS | .opus | High efficiency |
| NCM | .ncm | NetEase Cloud Music |

## Batch Processing

### Batch NCM Conversion

```python
from pathlib import Path
from ncmdump import NeteaseCloudMusicFile

ncm_dir = Path("path/to/ncm/files")
for ncm_file in ncm_dir.glob("*.ncm"):
    ncm = NeteaseCloudMusicFile(str(ncm_file))
    ncm.decrypt()
    output = str(ncm_file).replace('.ncm', '.mp3')
    ncm.dump_music(output)
```

### Batch Audio Clipping (Linux/macOS)

```bash
for f in *.mp3; do
    ffmpeg -i "$f" -ss 29 -to 45 -c copy "clip_${f}"
done
```

## Documentation

- [English README](README.md)
- [中文文档 (Chinese Documentation)](docs/README.cn.md)

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
