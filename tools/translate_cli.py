# -*- coding: utf-8 -*-
# 命令行版翻译工具 - 国内可用接口
from deep_translator import MyMemoryTranslator

def translate(text):
    # 简单判断：包含中文就翻成英文，否则翻成中文
    has_chinese = any('\u4e00' <= ch <= '\u9fff' for ch in text)
    if has_chinese:
        result = MyMemoryTranslator(source='zh-CN', target='en-US').translate(text)
        return f"中译英：{result}"
    else:
        result = MyMemoryTranslator(source='en-US', target='zh-CN').translate(text)
        return f"英译中：{result}"

print("=" * 40)
print("  命令行翻译工具（国内可用版）")
print("  英文->中文，中文->英文，自动判断")
print("  输入 q 退出")
print("=" * 40)

while True:
    text = input("\n请输入要翻译的文字：").strip()
    if text.lower() == "q":
        print("再见！")
        break
    if not text:
        continue
    try:
        print(translate(text))
    except Exception as e:
        print(f"翻译失败：{e}")
