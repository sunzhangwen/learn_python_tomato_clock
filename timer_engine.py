"""番茄钟计时引擎，纯逻辑，无 UI 依赖"""

from enum import Enum
from typing import Callable, Optional


class TimerState(Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"


class TimerPhase(Enum):
    WORK = "work"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"


class TimerEngine:
    def __init__(self, root):
        self._root = root
        self._tick_id: Optional[str] = None

        self.total_seconds: int = 0
        self.remaining_seconds: int = 0
        self.state: TimerState = TimerState.IDLE
        self.phase: TimerPhase = TimerPhase.WORK
        self.completed_sessions: int = 0

        self.on_tick: Optional[Callable[[int], None]] = None
        self.on_complete: Optional[Callable[[], None]] = None

    def set_phase(self, phase: TimerPhase, duration_seconds: int):
        """切换阶段并设置时长"""
        self._cancel_tick()
        self.phase = phase
        self.total_seconds = duration_seconds
        self.remaining_seconds = duration_seconds
        self.state = TimerState.IDLE
        if self.on_tick:
            self.on_tick(self.remaining_seconds)

    def start(self):
        """开始或恢复计时"""
        if self.state == TimerState.RUNNING:
            return
        self.state = TimerState.RUNNING
        self._tick()

    def pause(self):
        """暂停计时"""
        if self.state != TimerState.RUNNING:
            return
        self._cancel_tick()
        self.state = TimerState.PAUSED

    def reset(self):
        """重置当前阶段"""
        self._cancel_tick()
        self.remaining_seconds = self.total_seconds
        self.state = TimerState.IDLE
        if self.on_tick:
            self.on_tick(self.remaining_seconds)

    def _tick(self):
        """每秒倒计时"""
        if self.state != TimerState.RUNNING:
            return

        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            if self.on_tick:
                self.on_tick(self.remaining_seconds)
            self._tick_id = self._root.after(1000, self._tick)
        else:
            self.state = TimerState.IDLE
            if self.phase == TimerPhase.WORK:
                self.completed_sessions += 1
            if self.on_complete:
                self.on_complete()

    def _cancel_tick(self):
        """取消待执行的 tick"""
        if self._tick_id:
            self._root.after_cancel(self._tick_id)
            self._tick_id = None

    def format_time(self, seconds: Optional[int] = None) -> str:
        """格式化时间为 MM:SS"""
        s = seconds if seconds is not None else self.remaining_seconds
        mins = s // 60
        secs = s % 60
        return f"{mins:02d}:{secs:02d}"
