try:
    import threading
    import time
    import os
    import sys
    import ctypes
    import customtkinter as ctk
    from pynput import keyboard
    from pynput.keyboard import Key
except ModuleNotFoundError as em:
    print(f"Module missing: {em.name}")
    exit()

kbd = keyboard.Controller()
ctk.set_appearance_mode("dark")

class App:
    def __init__(self, main):
        self.main = main

    def safe_type(self, text):
        for char in text:
            if self.main.stop_event.is_set():
                return
            kbd.press(char)
            kbd.release(char)
            time.sleep(0.005)

    def troll_start(self):
        time.sleep(5)
        for word in self.main.words:
            if self.main.stop_event.is_set():
                break
            self.safe_type(word)
            if self.main.stop_event.is_set():
                break
            kbd.press(Key.enter)
            kbd.release(Key.enter)
            time.sleep(0.5)
        print("Скрипт остановлен")

    def troll_start_thread(self):
        if self.main.switch_var.get() == "on":
            self.main.stop_event.clear()

            try:
                with open("text.txt", "r", encoding="utf-8") as f:
                    self.main.words = f.read().splitlines()
            except Exception as e:
                ctypes.windll.user32.MessageBoxW(
                    0,
                    f"text.txt не найден\n{e}",
                    "Ошибка",
                    0x10
                )
                return

            if self.main.thread_instance and self.main.thread_instance.is_alive():
                return

            self.main.thread_instance = threading.Thread(target=self.troll_start)
            self.main.thread_instance.start()

        else:
            self.main.stop_event.set()

class Main:
    def __init__(self, master):
        self.root = master
        self.root.title("troll")

        self.app = App(self)

        self.stop_event = threading.Event()
        self.thread_instance = None
        self.words = []

        self._widgets()

        self.esc_listener = keyboard.Listener(on_press=self.emergency_stop)
        self.esc_listener.start()

    def _widgets(self):
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(padx=20, pady=20)

        self.label = ctk.CTkLabel(self.root, text="Скрипт начнёт работать через 5 секунд\nESC - экстренная остановка").pack(pady=10)

        self.switch_var = ctk.StringVar(value="off")

        self.switch = ctk.CTkSwitch(self.main_frame, text="on", command=self.app.troll_start_thread, variable=self.switch_var, onvalue="on", offvalue="off").pack(side="left", padx=10)

        self.exit_btn = ctk.CTkButton(self.main_frame, text="exit", command=self.troll_stop).pack(side="left")

    @staticmethod
    def emergency_stop(key):
        if key == Key.esc:
            # noinspection PyProtectedMember
            os._exit(0)

    def troll_stop(self):
        self.stop_event.set()
        # noinspection PyProtectedMember
        os._exit(0)

if __name__ == '__main__':
    root = ctk.CTk()
    mainapp = Main(root)
    root.mainloop()