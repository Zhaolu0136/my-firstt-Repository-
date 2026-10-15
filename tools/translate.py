# -*- coding: utf-8 -*-
# 桌面翻译工具 - GUI图形界面版
import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import MyMemoryTranslator

def do_translate():
    text = input_box.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("提示", "请先输入要翻译的文本")
        return
    lang = lang_var.get()
    btn_translate.config(state=tk.DISABLED, text="翻译中...")
    root.update()
    try:
        if lang == "英文→中文":
            result = MyMemoryTranslator(source='en-US', target='zh-CN').translate(text)
        else:
            result = MyMemoryTranslator(source='zh-CN', target='en-US').translate(text)
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, result)
    except Exception as e:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, f"翻译失败：{e}\n请检查网络后重试。")
    finally:
        btn_translate.config(state=tk.NORMAL, text="翻译")

def copy_result():
    res = output_box.get("1.0", tk.END).strip()
    if res:
        root.clipboard_clear()
        root.clipboard_append(res)
        messagebox.showinfo("提示", "翻译结果已复制！")

root = tk.Tk()
root.title("🌐 桌面翻译工具")
root.geometry("560x440")
root.resizable(True, True)

# 方向选择
top_frame = tk.Frame(root)
top_frame.pack(fill=tk.X, padx=10, pady=8)
tk.Label(top_frame, text="翻译方向：").pack(side=tk.LEFT)
lang_var = tk.StringVar(value="英文→中文")
lang_combo = ttk.Combobox(top_frame, textvariable=lang_var, values=["英文→中文", "中文→英文"], state="readonly", width=12)
lang_combo.pack(side=tk.LEFT)

tk.Label(root, text="输入文本：").pack(anchor=tk.W, padx=10)
input_box = tk.Text(root, height=7, width=70, font=("微软雅黑", 11))
input_box.pack(padx=10, fill=tk.BOTH, expand=True)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=8)
btn_translate = ttk.Button(btn_frame, text="翻译", command=do_translate)
btn_translate.pack(side=tk.LEFT, padx=5)
ttk.Button(btn_frame, text="复制结果", command=copy_result).pack(side=tk.LEFT, padx=5)

tk.Label(root, text="翻译结果：").pack(anchor=tk.W, padx=10)
output_box = tk.Text(root, height=7, width=70, font=("微软雅黑", 11), bg="#f5f5f5")
output_box.pack(padx=10, fill=tk.BOTH, expand=True)

root.mainloop()
