"""自定义 UI 组件：圆形计时器显示、控制按钮"""

import customtkinter as ctk
from theme import COLORS, get_font


class CircularTimerDisplay(ctk.CTkFrame):
    """圆形进度环 + 时间显示"""

    def __init__(self, master, size=280, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._size = size
        self._ring_width = 10
        self._pad = 15

        self.canvas = ctk.CTkCanvas(
            self,
            width=size,
            height=size,
            highlightthickness=0,
            bg=self._get_bg(),
        )
        self.canvas.pack()

        # 初始绘制
        self._time_text_id = None
        self._draw_ring(1.0, "00:00", "#FF6B6B")

    def _get_bg(self) -> str:
        """获取父容器背景色"""
        try:
            return self.master.master.cget("fg_color")
        except Exception:
            return "#F5F5F7"

    def update_display(self, remaining: int, total: int, accent_color: str):
        """更新进度环和时间显示"""
        fraction = remaining / total if total > 0 else 0
        mins = remaining // 60
        secs = remaining % 60
        time_str = f"{mins:02d}:{secs:02d}"
        self._draw_ring(fraction, time_str, accent_color)

    def _draw_ring(self, fraction: float, time_str: str, accent_color: str):
        """绘制进度环和时间文字"""
        self.canvas.delete("all")
        s = self._size
        p = self._pad
        w = self._ring_width

        # 背景环（灰色）
        self.canvas.create_arc(
            p, p, s - p, s - p,
            start=90, extent=-360,
            style="arc", width=w,
            outline="#E5E5EA",
        )

        # 进度环（彩色，从顶部顺时针）
        if fraction > 0:
            extent = fraction * 360
            self.canvas.create_arc(
                p, p, s - p, s - p,
                start=90, extent=-extent,
                style="arc", width=w,
                outline=accent_color,
            )

        # 时间文字
        font = get_font("timer_display")
        self.canvas.create_text(
            s // 2, s // 2,
            text=time_str,
            font=font,
            fill="#1D1D1F",
        )

    def set_theme(self, mode: str):
        """切换主题时更新背景"""
        bg = COLORS[mode]["bg"]
        self.canvas.configure(bg=bg)
        # 重新绘制以更新文字颜色
        fg = COLORS[mode]["timer_text"]
        self.canvas.itemconfig("all", fill=fg)


class ControlButton(ctk.CTkButton):
    """圆角控制按钮"""

    def __init__(self, master, icon: str, label: str, command=None, **kwargs):
        super().__init__(
            master,
            text=f"{icon}\n{label}",
            command=command,
            width=80,
            height=60,
            corner_radius=15,
            font=get_font("button"),
            **kwargs,
        )
