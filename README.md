# 我的工具合集

个人开发的小工具集合。

## 工具列表

### 1. 翻译工具
- `tools/translate.py` — 图形界面翻译器（Python tkinter）
- `tools/translate_cli.py` — 命令行版翻译器
- `tools/翻译工具.html` — 网页版翻译器（浏览器直接打开）

### 2. 截图翻译工具
- `tools/截图翻译.py` — 框选屏幕区域，自动识别英文并翻译成中文

## 使用说明

### 环境要求
- Python 3.13+
- 依赖库：`pip install deep-translator pillow rapidocr-onnxruntime`

### 快速开始
```bash
# 网页版翻译器（最简单，双击即可）
打开 tools/翻译工具.html

# 图形界面翻译器
python tools/translate.py

# 截图翻译工具
python tools/截图翻译.py
```

## 备注
- 翻译接口使用 MyMemory API，国内可访问
- OCR识别使用 RapidOCR，本地运行无需联网识别
