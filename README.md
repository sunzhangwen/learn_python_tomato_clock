# 番茄钟 (Pomodoro Timer)

一款 macOS 风格的桌面番茄钟工具，基于 Python + customtkinter 实现。

## 项目结构

```
├── main.py              # 入口文件
├── app.py               # 主应用类（窗口、布局、事件绑定）
├── timer_engine.py      # 计时引擎（倒计时状态机）
├── ui_components.py     # UI 组件（圆形进度环、控制按钮）
├── theme.py             # 主题配置（颜色、字体、时长设置）
├── notification.py      # 通知模块（提示音、弹窗）
├── requirements.txt     # Python 依赖
└── assets/
    └── alarm.wav        # 计时结束提示音
```

## 功能特性

- **番茄工作法**：25 分钟工作 → 5 分钟短休息 → 循环 4 轮后 15 分钟长休息
- **圆形进度环**：实时显示倒计时进度
- **macOS 风格 UI**：交通灯按钮（关闭/最小化）、圆角窗口、简洁配色
- **明暗主题**：一键切换浅色/深色模式
- **窗口拖拽**：自定义标题栏，可自由拖动窗口位置
- **自动提醒**：时间到播放提示音 + 弹窗通知，自动切换工作/休息阶段
- **会话计数**：显示当前轮次进度

## 安装依赖

```bash
pip install -r requirements.txt
```

依赖列表：
- `customtkinter>=5.2.0` — 现代化 tkinter UI 组件
- `Pillow>=10.0` — 图像处理（customtkinter 依赖）

## 运行

```bash
python main.py
```

## 自定义配置

编辑 `theme.py` 可修改以下配置：

```python
WORK_DURATION = 25 * 60          # 工作时长（秒）
SHORT_BREAK_DURATION = 5 * 60    # 短休息时长（秒）
LONG_BREAK_DURATION = 15 * 60    # 长休息时长（秒）
SESSIONS_BEFORE_LONG_BREAK = 4   # 几轮后进入长休息
```

## 系统要求

- Python 3.8+
- Windows 10/11（推荐）
