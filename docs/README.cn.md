# Audio Converter Skill 使用文档

## 目录

1. [技能简介](#技能简介)
2. [安装配置](#安装配置)
3. [快速开始](#快速开始)
4. [功能详解](#功能详解)
5. [命令行工具](#命令行工具)
6. [使用示例](#使用示例)
7. [常见问题](#常见问题)

---

## 技能简介

**Audio Converter** 是一款音视频格式转换和剪辑工具，支持：

- 🎵 **NCM 格式转换** - 网易云音乐 ncm 格式转 MP3/FLAC
- ✂️ **音频截取** - 按时间范围裁剪音频片段
- 🔄 **格式转换** - 支持 MP3、WAV、AAC、FLAC、OGG 等格式互转
- 📋 **信息查看** - 查看音频文件的时长、比特率等元数据

### 系统要求

- Python 3.10+ （推荐 Python 3.10-3.12，3.13 需要额外配置）
- FFmpeg （用于音频截取和格式转换）
- ncmdump-py 库 （用于 NCM 格式转换）

---

## 安装配置

### 1. 安装 FFmpeg

**Windows:**
1. 下载 FFmpeg: https://ffmpeg.org/download.html
2. 解压到任意目录（如 `C:\ffmpeg`）
3. 将 `bin` 目录添加到系统 PATH 环境变量
4. 重启命令行工具使环境变量生效

**验证安装:**
```bash
ffmpeg -version
```

### 2. 安装 Python 依赖

```bash
pip install ncmdump-py
```

> 注意：如果使用 Python 3.13，工具会自动创建缺失的 imghdr 模块，无需手动处理。

### 3. 验证工具

```bash
python audio_tool.py info "任意音频文件.mp3"
```

---

## 快速开始

### 示例 1：转换 NCM 文件

```bash
# 使用命令行工具
python audio_tool.py convert "歌曲.ncm"

# 或直接使用 ncmdump
python -m ncmdump "歌曲.ncm"
```

### 示例 2：截取音频片段

```bash
# 截取 29 秒到 45 秒的片段
python audio_tool.py clip "歌曲.mp3" 29 45

# 使用 FFmpeg 直接截取
ffmpeg -i "歌曲.mp3" -ss 29 -to 45 -c copy "片段.mp3"
```

### 示例 3：查看音频信息

```bash
python audio_tool.py info "歌曲.mp3"
```

输出示例：
```
File: 歌曲.mp3
Duration: 180.50s (3.01min)
Bitrate: 320kbps
Sample rate: 44100Hz
```

---

## 功能详解

### NCM 格式转换

NCM 是网易云音乐的专有格式，经过加密处理。

**转换原理:**
1. 读取 NCM 文件头部，获取加密密钥
2. 使用 AES-ECB 解密音乐数据密钥
3. 使用 AES-CBC 解密原始音频数据
4. 将解密后的音频数据保存为 MP3/FLAC

**支持的输出格式:**
| 格式 | 说明 | 适用场景 |
|------|------|----------|
| MP3 | 最通用格式 | 大多数场景 |
| FLAC | 无损压缩 | 高音质需求 |

**元数据处理:**
- ✅ 保留歌曲标题
- ✅ 保留艺术家信息
- ✅ 保留专辑名称
- ✅ 保留专辑封面
- ✅ 保留音轨编号

### 音频截取

使用 FFmpeg 进行无损截取，不重新编码音频数据。

**时间格式:**
| 格式 | 示例 | 说明 |
|------|------|------|
| 秒数 | `29` | 直接写秒数 |
| HH:MM:SS | `00:00:29` | 标准时间格式 |
| MM:SS | `00:29` | 省略小时 |

**参数说明:**
- `-ss <start>`: 起始时间
- `-to <end>`: 结束时间
- `-c copy`: 流拷贝（快速，无损）

**截取模式:**

```bash
# 从指定时间到指定时间（最常用）
ffmpeg -i input.mp3 -ss 29 -to 45 output.mp3

# 从开头到指定时间
ffmpeg -i input.mp3 -ss 0 -to 60 output.mp3

# 从指定时间到结尾
ffmpeg -i input.mp3 -ss 120 output.mp3

# 指定精确时间点（-ss 放在 -i 前面更准确）
ffmpeg -ss 00:01:30 -i input.mp3 -to 00:02:45 -c copy output.mp3
```

### 格式转换

使用 FFmpeg 进行格式转换，支持多种音频编码器。

**常用转换:**

| 转换类型 | 命令 | 说明 |
|----------|------|------|
| MP3 → WAV | `ffmpeg -i input.mp3 output.wav` | 无损转换 |
| MP3 → AAC | `ffmpeg -i input.mp3 -c:a aac output.aac` | 高效压缩 |
| MP3 → OGG | `ffmpeg -i input.mp3 -c:a libvorbis output.ogg` | 开源格式 |
| FLAC → MP3 | `ffmpeg -i input.flac -c:a libmp3lame output.mp3` | 无损转有损 |
| MP3 → OPUS | `ffmpeg -i input.mp3 -c:a libopus output.opus` | 高效率 |

**指定比特率:**

```bash
# 低比特率（体积小，音质一般）
ffmpeg -i input.mp3 -b:a 128k output.mp3

# 标准比特率（推荐）
ffmpeg -i input.mp3 -b:a 192k output.mp3

# 高比特率（体积大，音质好）
ffmpeg -i input.mp3 -b:a 320k output.mp3
```

### 批量处理

**批量转换 NCM 文件:**

```python
from pathlib import Path
from ncmdump import NeteaseCloudMusicFile

ncm_dir = Path("path/to/ncm/files")
output_dir = Path("path/to/output")
output_dir.mkdir(exist_ok=True)

for ncm_file in ncm_dir.glob("*.ncm"):
    try:
        ncm = NeteaseCloudMusicFile(str(ncm_file))
        ncm.decrypt()
        output_path = output_dir / ncm_file.with_suffix('.mp3').name
        ncm.dump_music(str(output_path))
        print(f"✓ {ncm_file.name}")
    except Exception as e:
        print(f"✗ {ncm_file.name}: {e}")
```

**批量截取音频:**

```bash
# 在 bash 环境下
for f in *.mp3; do
    ffmpeg -i "$f" -ss 29 -to 45 -c copy "clip_${f}"
done
```

---

## 命令行工具

### 工具路径

```
C:\Users\Administrator\.config\opencode\skills\audio-converter\scripts\audio_tool.py
```

### 命令语法

```bash
python audio_tool.py <command> [arguments]

可用命令:
  convert <input> [output]  - 转换 NCM 为 MP3
  clip <input> <start> <end> [output]  - 截取音频片段
  info <file>  - 查看音频文件信息
```

### 命令详解

#### convert - 格式转换

```bash
# 基本用法
python audio_tool.py convert input.ncm

# 指定输出文件
python audio_tool.py convert input.ncm output.mp3

# 批量转换（需配合脚本）
for f in *.ncm; do python audio_tool.py convert "$f"; done
```

#### clip - 音频截取

```bash
# 基本用法（秒为单位）
python audio_tool.py clip input.mp3 29 45

# 指定输出文件
python audio_tool.py clip input.mp3 29 45 output.mp3

# 使用小数（如 29.5 秒）
python audio_tool.py clip input.mp3 29.5 45.5 output.mp3
```

#### info - 查看信息

```bash
# 查看 MP3 文件
python audio_tool.py info song.mp3

# 查看 FLAC 文件
python audio_tool.py info song.flac

# 查看 NCM 文件
python audio_tool.py info song.ncm
```

---

## 使用示例

### 场景 1：转换一首 NCM 歌曲

```
用户: 把 "周杰伦 - 晴天.ncm" 转换成 mp3

操作:
1. 找到文件: D:\Music\周杰伦 - 晴天.ncm
2. 执行转换
3. 输出: D:\Music\周杰伦 - 晴天.mp3
```

### 场景 2：截取副歌部分

```
用户: 把这首歌曲的 1 分 20 秒到 2 分 10 秒截取出来

操作:
1. 计算时间: 80 秒 到 130 秒
2. 执行截取
ffmpeg -i "歌曲.mp3" -ss 80 -to 130 -c copy "歌曲_clip_80s-130s.mp3"
```

### 场景 3：完整工作流

```
用户: 下载了一首 NCM，想截取副歌部分发朋友圈

操作步骤:
1. 转换 NCM 到 MP3
   python -m ncmdump "song.ncm"

2. 查看时长，确定截取位置
   python audio_tool.py info "song.mp3"
   输出: Duration: 240.50s (4.01min)

3. 截取副歌（假设是 1:20-2:10）
   python audio_tool.py clip "song.mp3" 80 130 "highlight.mp3"

4. 分享 highlight.mp3
```

### 场景 4：批量处理

```
用户: 有 50 首 NCM 歌曲要转换

操作:
1. 将所有 NCM 文件放入一个文件夹
2. 使用批量脚本转换
3. 所有 MP3 文件会保存在同一目录
```

---

## 常见问题

### Q1: 提示 "FFmpeg not found"

**原因:** FFmpeg 未安装或未添加到 PATH 环境变量

**解决方法:**
1. 下载 FFmpeg: https://ffmpeg.org/download.html
2. 解压到 `C:\ffmpeg`
3. 将 `C:\ffmpeg\bin` 添加到系统 PATH
4. 重启命令行工具

### Q2: Python 3.13 转换 NCM 报错 "No module named 'imghdr'"

**原因:** Python 3.13 移除了 imghdr 模块

**解决方法:**
工具已内置自动修复功能，会自动创建 imghdr 模块。
如果自动修复失败，可手动创建：

```python
# 创建文件: site-packages/imghdr/__init__.py
# 内容参考工具内置代码
```

### Q3: Windows 命令行无法处理中文文件名

**原因:** Windows 命令行编码问题

**解决方法:**
使用 Python API 而不是命令行：

```python
from ncmdump import NeteaseCloudMusicFile

ncm = NeteaseCloudMusicFile("D:/Music/歌曲.ncm")
ncm.decrypt()
ncm.dump_music("D:/Music/歌曲.mp3")
```

### Q4: 截取后文件时长不对

**原因:** 使用了不准确的截取方式

**解决方法:**
将 `-ss` 参数放在 `-i` 前面：

```bash
# 不准确（可能差几帧）
ffmpeg -i input.mp3 -ss 29 -to 45 -c copy output.mp3

# 准确（推荐）
ffmpeg -ss 29 -i input.mp3 -to 45 -c copy output.mp3
```

### Q5: 如何保留原有音质？

**转换 NCM:**
默认输出为 320kbps MP3，已经是最高音质

**格式转换:**
- 避免多次转码（每次都会有损失）
- 使用 `-c:a copy` 进行流拷贝（最快且无损）
- 指定高比特率: `-b:a 320k`

### Q6: 批量处理时如何跳过已转换的文件？

```python
from pathlib import Path

ncm_dir = Path("input")
output_dir = Path("output")

for ncm_file in ncm_dir.glob("*.ncm"):
    mp3_file = output_dir / ncm_file.with_suffix('.mp3').name
    if mp3_file.exists():
        print(f"跳过（已存在）: {ncm_file.name}")
        continue
    
    # 转换...
```

---

## 附录

### FFmpeg 常用参数

| 参数 | 说明 |
|------|------|
| `-i` | 输入文件 |
| `-ss` | 起始时间 |
| `-to` | 结束时间 |
| `-c copy` | 流拷贝（快速） |
| `-c:a <codec>` | 音频编码器 |
| `-b:a <bitrate>` | 音频比特率 |
| `-ar <rate>` | 采样率 |
| `-ac <channels>` | 声道数 |

### 音频格式编码器

| 格式 | 编码器 | 命令示例 |
|------|--------|----------|
| MP3 | libmp3lame | `-c:a libmp3lame -b:a 320k` |
| AAC | aac | `-c:a aac -b:a 192k` |
| FLAC | flac | `-c:a flac` |
| WAV | pcm_s16le | `-c:a pcm_s16le` |
| OGG | libvorbis | `-c:a libvorbis -q:a 4` |
| OPUS | libopus | `-c:a libopus -b:a 128k` |

### Mutagen 库（元数据处理）

```python
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.id3 import ID3

# 读取 MP3 信息
audio = MP3("song.mp3")
print(f"时长: {audio.info.length}秒")
print(f"比特率: {audio.info.bitrate}")

# 读取标签
tags = ID3("song.mp3")
print(f"标题: {tags.get('TIT2')}")
print(f"艺术家: {tags.get('TPE1')}")
print(f"专辑: {tags.get('TALB')}")
```

---

*文档版本: 1.0*
*最后更新: 2026-05-07*
