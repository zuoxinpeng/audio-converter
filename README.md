# Audio Converter

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

A versatile audio format conversion and clipping tool that supports NCM, MP3, WAV, AAC, FLAC, OGG, and more.

## ✨ Features

- 🎵 **NCM Format Conversion** - Convert NetEase Cloud Music (NCM) files to MP3/FLAC
- ✂️ **Audio Clipping** - Extract audio segments by time range with precision
- 🔄 **Format Conversion** - Convert between MP3, WAV, AAC, FLAC, OGG, OPUS, and more
- 📋 **Metadata Viewing** - View audio file info (duration, bitrate, sample rate)
- 🐍 **Python API** - Use as a Python library in your own projects
- 📦 **Batch Processing** - Convert or clip multiple files efficiently

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/zuoxinpeng/audio-converter.git
cd audio-converter

# Install dependencies
pip install -r requirements.txt
```

### Prerequisites

- **Python 3.10+** (Python 3.10-3.12 recommended)
- **FFmpeg** (for audio processing)

#### Install FFmpeg

| Platform | Command |
|----------|---------|
| Windows | Download from [ffmpeg.org](https://ffmpeg.org/download.html) |
| macOS | `brew install ffmpeg` |
| Linux | `sudo apt install ffmpeg` |

### Usage

```bash
# Convert NCM to MP3
python audio_tool.py convert "song.ncm"

# Clip audio segment (29s to 45s)
python audio_tool.py clip "song.mp3" 29 45

# View audio information
python audio_tool.py info "song.mp3"
```

## 📖 Command Reference

```
python audio_tool.py <command> [arguments]

Commands:
  convert <input> [output]              - Convert NCM to MP3
  clip <input> <start> <end> [output]   - Extract audio segment
  info <file>                            - Show audio file information
```

## 💻 Python API

### NCM to MP3 Conversion

```python
from ncmdump import NeteaseCloudMusicFile

ncm = NeteaseCloudMusicFile("song.ncm")
ncm.decrypt()
ncm.dump_music("song.mp3")
print("Converted: song.mp3")
```

### Batch Conversion

```python
from pathlib import Path
from ncmdump import NeteaseCloudMusicFile

ncm_dir = Path("path/to/ncm/files")
for ncm_file in ncm_dir.glob("*.ncm"):
    ncm = NeteaseCloudMusicFile(str(ncm_file))
    ncm.decrypt()
    output = str(ncm_file).replace('.ncm', '.mp3')
    ncm.dump_music(output)
    print(f"Converted: {ncm_file.name}")
```

### Audio Clipping with FFmpeg

```bash
# Basic clipping
ffmpeg -i input.mp3 -ss 29 -to 45 -c copy output.mp3

# High precision (place -ss before -i)
ffmpeg -ss 00:01:30 -i input.mp3 -to 00:02:45 -c copy output.mp3

# Convert format
ffmpeg -i input.mp3 -c:a aac -b:a 192k output.aac
ffmpeg -i input.flac -c:a libmp3lame -b:a 320k output.mp3
```

## 📊 Supported Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| MP3 | .mp3 | Most widely supported audio format |
| WAV | .wav | Uncompressed PCM audio |
| AAC | .aac, .m4a | Advanced Audio Coding |
| FLAC | .flac | Free Lossless Audio Codec |
| OGG | .ogg | Open source compressed format |
| OPUS | .opus | High-efficiency speech/audio |
| NCM | .ncm | NetEase Cloud Music (encrypted) |

## 🔧 Troubleshooting

### "FFmpeg not found"

Ensure FFmpeg is installed and added to your PATH:

```bash
# Verify FFmpeg installation
ffmpeg -version
```

### "No module named 'imghdr'" (Python 3.13+)

The tool automatically creates a fallback for the removed `imghdr` module. If issues persist, install manually:

```bash
pip install imghdr
```

### Chinese Filenames on Windows

Use the Python API instead of CLI for better Unicode support:

```python
from ncmdump import NeteaseCloudMusicFile
ncm = NeteaseCloudMusicFile("D:/Music/歌曲.ncm")
```

## 📂 Project Structure

```
audio-converter/
├── .github/
│   └── workflows/           # CI/CD workflows
├── docs/
│   └── README.cn.md         # 中文文档
├── scripts/
│   └── audio_tool.py        # Main CLI tool
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── requirements.txt
└── SKILL.md
```

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- [ncmdump-py](https://github.com/zwc404/ncmdump-py) - NCM format decryption
- [mutagen](https://github.com/quodlibet/mutagen) - Audio metadata handling
- [FFmpeg](https://ffmpeg.org/) - Audio processing framework
