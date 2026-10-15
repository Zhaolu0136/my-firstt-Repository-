# -*- coding: utf-8 -*-
# 桌面截图翻译工具
# 点击按钮框选屏幕区域，自动识别英文并翻译成中文
import tkinter as tk
from PIL import ImageGrab
from rapidocr_onnxruntime import RapidOCR
from deep_translator import MyMemoryTranslator
import threading
import numpy as np

print("正在加载OCR模型，请稍候...")
ocr = RapidOCR()
print("模型加载完成！")

class ScreenCapture:
    def __init__(self, root):
        self.root = root
        self.root.title("截图翻译工具")
        self.root.geometry("320x180")
        self.root.attributes("-topmost", True)

        tk.Label(root, text="📷 截图翻译工具", font=("微软雅黑", 14)).pack(pady=10)

        self.btn = tk.Button(root, text="📸 开始截图翻译", font=("微软雅黑", 12),
                             bg="#4a90d9", fg="white", relief=tk.FLAT,
                             width=16, height=2, command=self.start_capture)
        self.btn.pack(pady=5)

        self.status = tk.Label(root, text="状态：就绪", font=("微软雅黑", 10), fg="green")
        self.status.pack(pady=5)

    def start_capture(self):
        self.status.config(text="状态：框选中...", fg="orange")
        self.btn.config(state=tk.DISABLED)
        # 创建全屏遮罩窗口
        self.overlay = tk.Toplevel(self.root)
        self.overlay.attributes("-fullscreen", True)
        self.overlay.attributes("-alpha", 0.3)
        self.overlay.attributes("-topmost", True)
        self.overlay.configure(bg="black")
        self.overlay.config(cursor="cross")

        self.canvas = tk.Canvas(self.overlay, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.overlay.bind("<Escape>", lambda e: self.cancel_capture())

    def cancel_capture(self):
        self.overlay.destroy()
        self.btn.config(state=tk.NORMAL)
        self.status.config(text="状态：就绪", fg="green")

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2)

    def on_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event):
        end_x = event.x
        end_y = event.y
        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)
        self.overlay.destroy()
        self.btn.config(state=tk.NORMAL)

        if x2 - x1 < 5 or y2 - y1 < 5:
            self.status.config(text="状态：就绪", fg="green")
            return

        self.status.config(text="状态：识别翻译中...", fg="orange")
        threading.Thread(target=self.process, args=(x1, y1, x2, y2), daemon=True).start()

    def process(self, x1, y1, x2, y2):
        try:
            img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            img_array = np.array(img)
            result, _ = ocr(img_array)
            if not result:
                self.root.after(0, lambda: self.show_result("（未识别到文字）", ""))
                return
            text = "\n".join([line[1] for line in result])
            # 分段翻译（MyMemory有长度限制，按行分段）
            lines = text.split("\n")
            translated_lines = []
            for line in lines:
                line = line.strip()
                if not line:
                    translated_lines.append("")
                    continue
                try:
                    t = MyMemoryTranslator(source='en-US', target='zh-CN').translate(line)
                    translated_lines.append(t)
                except:
                    translated_lines.append(line)
            translated = "\n".join(translated_lines)
            self.root.after(0, lambda: self.show_result(text, translated))
        except Exception as e:
            self.root.after(0, lambda: self.show_result("识别失败", str(e)))

    def show_result(self, original, translated):
        self.status.config(text="状态：就绪", fg="green")
        win = tk.Toplevel(self.root)
        win.title("翻译结果")
        win.geometry("500x400")
        win.attributes("-topmost", True)

        tk.Label(win, text="📝 识别到的英文：", font=("微软雅黑", 11)).pack(anchor=tk.W, padx=10, pady=5)
        orig_text = tk.Text(win, height=8, width=60, font=("微软雅黑", 10))
        orig_text.pack(padx=10, fill=tk.BOTH, expand=True)
        orig_text.insert(tk.END, original)

        tk.Label(win, text="🌐 中文翻译：", font=("微软雅黑", 11), fg="blue").pack(anchor=tk.W, padx=10, pady=5)
        trans_text = tk.Text(win, height=8, width=60, font=("微软雅黑", 10), bg="#f0f7ff")
        trans_text.pack(padx=10, fill=tk.BOTH, expand=True)
        trans_text.insert(tk.END, translated)

        tk.Button(win, text="复制翻译结果", command=lambda: (win.clipboard_clear(), win.clipboard_append(translated))).pack(pady=5)

root = tk.Tk()
app = ScreenCapture(root)
root.mainloop()
