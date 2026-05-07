# Audio Converter

一款功能强大的音频格式转换和剪辑工具，支持 NCM、MP3、WAV、AAC、FLAC、OGG 等格式。

## 功能特点

- NCM 格式转换 - 网易云音乐 NCM 格式转换为 MP3/FLAC
- 音频剪辑 - 按时间范围精确提取音频片段
- 格式转换 - 支持 MP3、WAV、AAC、FLAC、OGG、OPUS 等格式互转
- 元数据查看 - 查看音频时长、比特率、采样率等信息
- Python API - 可作为 Python 库在项目中使用
- 批量处理 - 高效转换或剪辑多个文件

## 快速开始

### 安装依赖

`Bash
pip install -r requirements.txt
`

### FFmpeg 安装

- Windows: 从 ffmpeg.org 下载
- macOS: brew install ffmpeg
- Linux: sudo apt install ffmpeg

### 使用方法

`Bash
# NCM 转换为 MP3
python audio_tool.py convert 歌曲.ncm

# 剪辑音频片段
python audio_tool.py clip 歌曲.mp3 29 45

# 查看音频信息
python audio_tool.py info 歌曲.mp3
`

## 命令说明

- convert 输入文件 [输出文件] - 将 NCM 转换为 MP3
- clip 输入文件 起始秒 结束秒 [输出文件] - 提取音频片段
- info 文件 - 显示音频文件信息

## 支持的格式

MP3、WAV、AAC、FLAC、OGG、OPUS、NCM

## 开源协议

MIT License
