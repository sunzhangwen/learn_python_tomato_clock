"""通知模块：声音播放 + 系统弹窗"""

import os
import sys


class Notifier:
    def __init__(self, assets_dir: str = "assets"):
        self._assets_dir = assets_dir
        self._use_winsound = sys.platform == "win32"

    def play_alarm(self):
        """播放提示音"""
        alarm_path = os.path.join(self._assets_dir, "alarm.wav")

        if self._use_winsound:
            import winsound
            if os.path.exists(alarm_path):
                winsound.PlaySound(
                    alarm_path,
                    winsound.SND_FILENAME | winsound.SND_ASYNC,
                )
            else:
                # 无音频文件时使用系统蜂鸣
                winsound.Beep(800, 500)
        else:
            # 非 Windows 平台的简单 fallback
            print("\a", end="", flush=True)

    def show_notification(self, title: str, message: str):
        """显示系统通知"""
        try:
            from tkinter import messagebox
            messagebox.showinfo(title, message)
        except Exception:
            print(f"[通知] {title}: {message}")
