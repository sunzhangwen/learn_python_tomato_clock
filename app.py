"""番茄钟主应用"""

import customtkinter as ctk
from timer_engine import TimerEngine, TimerPhase
from ui_components import CircularTimerDisplay, ControlButton
from notification import Notifier
from theme import (
    COLORS,
    WORK_DURATION,
    SHORT_BREAK_DURATION,
    LONG_BREAK_DURATION,
    SESSIONS_BEFORE_LONG_BREAK,
    get_font,
)


class PomodoroApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self._mode = "light"
        self._drag_x = 0
        self._drag_y = 0

        # 初始化组件
        self._notifier = Notifier()
        self._engine = TimerEngine(self)

        # 窗口设置
        self._setup_window()

        # 构建布局
        self._build_layout()

        # 绑定回调
        self._bind_callbacks()

        # 初始显示
        self._engine.set_phase(TimerPhase.WORK, WORK_DURATION)

    def _setup_window(self):
        """配置窗口外观"""
        self.title("番茄钟")
        self.geometry("360x500")
        self.resizable(False, False)

        # 移除默认标题栏
        self.overrideredirect(True)

        # 设置窗口背景
        ctk.set_appearance_mode("light")
        self.configure(fg_color=COLORS[self._mode]["bg"])

        # 使窗口圆角（Windows）
        try:
            self.after(10, self._apply_rounded_corners)
        except Exception:
            pass

        # 居中显示
        self.update_idletasks()
        w, h = 360, 500
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _apply_rounded_corners(self):
        """Windows 11 圆角窗口"""
        try:
            import pywinstyles
            pywinstyles.apply_style(self, "acrylic")
        except ImportError:
            pass
        except Exception:
            pass

    def _build_layout(self):
        """构建 UI 布局"""
        colors = COLORS[self._mode]

        # ===== 标题栏 =====
        self._titlebar = ctk.CTkFrame(
            self, height=40, fg_color=colors["titlebar_bg"], corner_radius=0
        )
        self._titlebar.pack(fill="x")
        self._titlebar.pack_propagate(False)

        # 交通灯按钮
        dots_frame = ctk.CTkFrame(self._titlebar, fg_color="transparent")
        dots_frame.pack(side="left", padx=15, pady=10)

        self._dot_close = ctk.CTkButton(
            dots_frame,
            text="",
            width=14,
            height=14,
            corner_radius=7,
            fg_color=colors["dot_red"],
            hover_color="#E0444E",
            command=self.destroy,
        )
        self._dot_close.pack(side="left", padx=4)

        self._dot_minimize = ctk.CTkButton(
            dots_frame,
            text="",
            width=14,
            height=14,
            corner_radius=7,
            fg_color=colors["dot_yellow"],
            hover_color="#DEA123",
            command=self.iconify,
        )
        self._dot_minimize.pack(side="left", padx=4)

        # 主题切换按钮
        self._theme_btn = ctk.CTkButton(
            self._titlebar,
            text="☀",
            width=30,
            height=26,
            corner_radius=8,
            fg_color="transparent",
            text_color=colors["fg"],
            hover_color=colors["button_hover"],
            font=("Segoe UI", 14),
            command=self._toggle_theme,
        )
        self._theme_btn.pack(side="right", padx=10, pady=7)

        # 标题栏拖拽
        self._titlebar.bind("<Button-1>", self._on_drag_start)
        self._titlebar.bind("<B1-Motion>", self._on_drag_motion)

        # ===== 计时器显示 =====
        self._timer_display = CircularTimerDisplay(self, size=280)
        self._timer_display.pack(pady=(30, 10))

        # ===== 阶段标签 =====
        self._phase_label = ctk.CTkLabel(
            self,
            text="工作时间",
            font=get_font("phase_label"),
            text_color=colors["fg"],
        )
        self._phase_label.pack(pady=(0, 5))

        # ===== 会话计数 =====
        self._session_label = ctk.CTkLabel(
            self,
            text="第 1 / 4 轮",
            font=get_font("session"),
            text_color=colors["fg"],
        )
        self._session_label.pack(pady=(0, 15))

        # ===== 控制按钮 =====
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(0, 30))

        self._btn_start = ControlButton(
            btn_frame,
            icon="▶",
            label="开始",
            fg_color=colors["accent"],
            hover_color="#E05555",
            text_color="#FFFFFF",
            command=self._on_start,
        )
        self._btn_start.pack(side="left", padx=8)

        self._btn_pause = ControlButton(
            btn_frame,
            icon="⏸",
            label="暂停",
            fg_color=colors["button_fg"],
            hover_color=colors["button_hover"],
            text_color=colors["fg"],
            command=self._on_pause,
        )
        self._btn_pause.pack(side="left", padx=8)

        self._btn_reset = ControlButton(
            btn_frame,
            icon="↺",
            label="重置",
            fg_color=colors["button_fg"],
            hover_color=colors["button_hover"],
            text_color=colors["fg"],
            command=self._on_reset,
        )
        self._btn_reset.pack(side="left", padx=8)

    def _bind_callbacks(self):
        """绑定计时器回调"""
        self._engine.on_tick = self._on_tick
        self._engine.on_complete = self._on_complete

    # ===== 计时器回调 =====

    def _on_tick(self, remaining: int):
        """每秒更新显示"""
        accent = self._get_accent_color()
        self._timer_display.update_display(
            remaining, self._engine.total_seconds, accent
        )

    def _on_complete(self):
        """计时完成"""
        self._notifier.play_alarm()

        if self._engine.phase == TimerPhase.WORK:
            sessions = self._engine.completed_sessions
            self._notifier.show_notification(
                "番茄钟", f"工作时间结束！已完成 {sessions} 轮。休息一下吧。"
            )
            # 自动切换到休息
            if sessions % SESSIONS_BEFORE_LONG_BREAK == 0:
                self._engine.set_phase(TimerPhase.LONG_BREAK, LONG_BREAK_DURATION)
                self._phase_label.configure(text="长休息")
            else:
                self._engine.set_phase(TimerPhase.SHORT_BREAK, SHORT_BREAK_DURATION)
                self._phase_label.configure(text="短休息")
        else:
            self._notifier.show_notification("番茄钟", "休息结束！开始新一轮工作。")
            self._engine.set_phase(TimerPhase.WORK, WORK_DURATION)
            self._phase_label.configure(text="工作时间")

        self._update_session_label()
        self._update_display()

    # ===== 按钮事件 =====

    def _on_start(self):
        self._engine.start()

    def _on_pause(self):
        self._engine.pause()

    def _on_reset(self):
        self._engine.reset()
        self._update_display()

    # ===== 辅助方法 =====

    def _get_accent_color(self) -> str:
        colors = COLORS[self._mode]
        if self._engine.phase == TimerPhase.WORK:
            return colors["accent"]
        return colors["accent_break"]

    def _update_display(self):
        accent = self._get_accent_color()
        self._timer_display.update_display(
            self._engine.remaining_seconds, self._engine.total_seconds, accent
        )

    def _update_session_label(self):
        sessions = self._engine.completed_sessions
        current = (sessions % SESSIONS_BEFORE_LONG_BREAK) + 1
        self._session_label.configure(
            text=f"第 {current} / {SESSIONS_BEFORE_LONG_BREAK} 轮"
        )

    # ===== 窗口拖拽 =====

    def _on_drag_start(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def _on_drag_motion(self, event):
        x = self.winfo_x() + event.x - self._drag_x
        y = self.winfo_y() + event.y - self._drag_y
        self.geometry(f"+{x}+{y}")

    # ===== 主题切换 =====

    def _toggle_theme(self):
        self._mode = "dark" if self._mode == "light" else "light"
        ctk.set_appearance_mode(self._mode)
        self._apply_theme()

    def _apply_theme(self):
        colors = COLORS[self._mode]
        self.configure(fg_color=colors["bg"])
        self._titlebar.configure(fg_color=colors["titlebar_bg"])
        self._dot_close.configure(fg_color=colors["dot_red"])
        self._dot_minimize.configure(fg_color=colors["dot_yellow"])
        self._theme_btn.configure(
            text="🌙" if self._mode == "light" else "☀",
            text_color=colors["fg"],
            hover_color=colors["button_hover"],
        )
        self._phase_label.configure(text_color=colors["fg"])
        self._session_label.configure(text_color=colors["fg"])
        self._btn_start.configure(fg_color=colors["accent"])
        self._btn_pause.configure(
            fg_color=colors["button_fg"],
            hover_color=colors["button_hover"],
            text_color=colors["fg"],
        )
        self._btn_reset.configure(
            fg_color=colors["button_fg"],
            hover_color=colors["button_hover"],
            text_color=colors["fg"],
        )
        self._update_display()
