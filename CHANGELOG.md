# Changelog

All notable changes will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] - 2026-05-07

### Added
- NCM format conversion to MP3/FLAC
- Audio clipping via time range
- Audio format conversion (MP3, WAV, AAC, FLAC, OGG, OPUS)
- Audio metadata viewing (duration, bitrate, sample rate)
- Python 3.13 compatibility (imghdr module fallback)
- Command-line interface
- Chinese documentation
- FFmpeg integration for format conversion

### Features
- `convert` command - NCM to MP3 conversion
- `clip` command - Audio segment extraction
- `info` command - Audio metadata viewing
- Batch processing support
- Metadata preservation (title, artist, album, cover)

### Dependencies
- ncmdump-py (NCM format handling)
- mutagen (audio metadata)
- FFmpeg (external, must be installed separately)
