import tkinter as tk
from tkinter import messagebox, ttk

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("500x400")

        # Timer settings
        self.work_time = 25 * 60
        self.break_time = 5 * 60
        self.remaining_time = self.work_time
        self.sessions = 0
        self.running = False
        self.is_work_session = True

        # Theme variables
        self.dark_mode = False

        # Colors
        self.light_bg = "#FFFAF0"
        self.light_fg = "#333333"
        self.dark_bg = "#2C2C2C"
        self.dark_fg = "#FFFFFF"
        self.work_color = "#FF6347"  # Tomato
        self.break_color = "#32CD32"  # Lime Green

        # UI Elements
        self.create_widgets()
        self.toggle_theme(initial=True)

    def create_widgets(self):
        # Header
        self.header = tk.Label(self.root, text="Pomodoro Timer", font=("Helvetica", 18))
        self.header.pack(pady=10)

        # Time Display
        self.time_display = tk.Label(self.root, text=self.format_time(self.remaining_time), font=("Helvetica", 48))
        self.time_display.pack(pady=20)

        # Progress Bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

        # Controls
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        self.start_button = tk.Button(control_frame, text="Start", command=self.start_timer, bg="#4CAF50", fg="white", width=10)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = tk.Button(control_frame, text="Stop", command=self.stop_timer, bg="#F44336", fg="white", width=10)
        self.stop_button.grid(row=0, column=1, padx=5)

        self.reset_button = tk.Button(control_frame, text="Reset", command=self.reset_timer, bg="#FFC107", fg="black", width=10)
        self.reset_button.grid(row=0, column=2, padx=5)

        # Settings
        settings_frame = tk.Frame(self.root)
        settings_frame.pack(pady=10)

        tk.Label(settings_frame, text="Work (min):").grid(row=0, column=0, padx=5)
        self.work_entry = tk.Entry(settings_frame, width=5)
        self.work_entry.insert(0, "25")
        self.work_entry.grid(row=0, column=1, padx=5)

        tk.Label(settings_frame, text="Break (min):").grid(row=0, column=2, padx=5)
        self.break_entry = tk.Entry(settings_frame, width=5)
        self.break_entry.insert(0, "5")
        self.break_entry.grid(row=0, column=3, padx=5)

        self.update_button = tk.Button(settings_frame, text="Update", command=self.update_settings, bg="#008CBA", fg="white", width=10)
        self.update_button.grid(row=0, column=4, padx=5)

        # Theme Toggle
        self.theme_button = tk.Button(self.root, text="Toggle Theme", command=self.toggle_theme, bg="#E91E63", fg="white", width=15)
        self.theme_button.pack(pady=10)

        # Session Tracker
        self.session_label = tk.Label(self.root, text=f"Completed Sessions: {self.sessions}", font=("Helvetica", 12))
        self.session_label.pack(pady=10)

    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def update_settings(self):
        try:
            self.work_time = int(self.work_entry.get()) * 60
            self.break_time = int(self.break_entry.get()) * 60
            self.reset_timer()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for work and break times.")

    def toggle_theme(self, initial=False):
        bg_color = self.dark_bg if self.dark_mode else self.light_bg
        fg_color = self.dark_fg if self.dark_mode else self.light_fg
        self.root.configure(bg=bg_color)
        self.header.configure(bg=bg_color, fg=fg_color)
        self.time_display.configure(bg=bg_color, fg=fg_color)
        self.session_label.configure(bg=bg_color, fg=fg_color)
        if not initial:
            self.dark_mode = not self.dark_mode

    def start_timer(self):
        if not self.running:
            self.running = True
            self.update_timer()

    def stop_timer(self):
        self.running = False

    def reset_timer(self):
        self.stop_timer()
        self.remaining_time = self.work_time if self.is_work_session else self.break_time
        self.progress["value"] = 0
        self.time_display.config(text=self.format_time(self.remaining_time))

    def update_timer(self):
        if self.remaining_time > 0 and self.running:
            self.time_display.config(text=self.format_time(self.remaining_time))
            progress_value = ((self.work_time if self.is_work_session else self.break_time) - self.remaining_time) / (
                self.work_time if self.is_work_session else self.break_time
            ) * 100
            self.progress["value"] = progress_value
            self.remaining_time -= 1
            color = self.work_color if self.is_work_session else self.break_color
            self.time_display.config(fg=color)
            self.root.after(1000, self.update_timer)
        elif self.running:
            self.sessions += 1
            self.session_label.config(text=f"Completed Sessions: {self.sessions}")
            self.is_work_session = not self.is_work_session
            self.remaining_time = self.work_time if self.is_work_session else self.break_time
            messagebox.showinfo(
                "Pomodoro Timer",
                "Break Over! Back to work!" if self.is_work_session else "Work session complete! Take a break!",
            )
            self.update_timer()

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()
