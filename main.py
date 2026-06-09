"""番茄钟入口"""

from app import PomodoroApp


def main():
    app = PomodoroApp()
    app.mainloop()


if __name__ == "__main__":
    main()
