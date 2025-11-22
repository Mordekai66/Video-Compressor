# Video-Compressor
![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-Video_Processing-007808?logo=ffmpeg&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-306998?logo=python&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-Image_Processing-40A5E6?logo=pillow&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-Compatible-0078D6?logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-4DA51F?logo=opensourceinitiative&logoColor=white)

Video-Compressor is a Python application with Tkinter GUI that compresses videos while maintaining quality using FFmpeg.

## Features
- Drag & drop video files
- Real-time compression preview
- Adjustable video and audio settings for full control.
- Presets for quick optimization
- Clean, user-friendly interface

## How It Works
1. Import video file (drag or browse)
2. Adjust audio and video compression settings
3. Set output destination
4. Click "Run" to process
5. Get optimized video file in specified path

## Usage
1. Run the application (main_window.py)
2. Import video (drag and drop or browse)
3. Configure audio/video compression settings
4. Select output folder
5. Click on "Run" to start processing

## Future Plans
- Output size prediction
- Batch video processing
- Expanded codec support

## Requirements
- `Python 3.8+`
- `FFmpeg system installation`

### Packages:
  - `opencv-python`
  - `pillow`
  - `tkinterdnd2`
    
  ```python
  pip install opencv-python pillow tkinterdnd2
  ```
or 
```python
pip install -r requirements.txt
```

## Repository Structure
```bash
Video-Compressor/
├── main_window.py        # Main interface
├── compressing_window.py # Compression settings  
├── get_video_info.py     # Video analysis
├── run.py                # FFmpeg processor
├── LICENSE
└── requirements.txt
```

## Troubleshooting
- Ensure FFmpeg is installed
- Check file permissions
- Verify supported formats
- Monitor system resources
- Video file names should not contain spaces.

## License
MIT License - see `LICENSE`

## Contribution
- Contributions welcome! Fork and submit PRs for:
  - New features
  - Bug fixes
  - UI improvements
  - Documentation
