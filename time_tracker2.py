import tkinter as tk
from tkinter import ttk
import csv
import os
from datetime import datetime, timedelta

class TimeTracker:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Work Time Tracker")
        
        # Styling
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#ccc")
        style.configure("TLabel", padding=6, font=("Arial", 10))
        style.configure("Timer.TLabel", font=("Arial", 16, "bold"), foreground="blue")
        
        # Variables
        self.task_var = tk.StringVar()
        self.project_var = tk.StringVar()
        self.timer_var = tk.StringVar()
        self.start_time = None
        self.total_paused_time = timedelta()  # Total time that the timer has been paused
        
        # UI Elements
        ttk.Label(self.root, text="Task:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self.root, textvariable=self.task_var, width=30).grid(row=0, column=1, padx=10, pady=5, columnspan=3)
        
        ttk.Label(self.root, text="Project:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self.root, textvariable=self.project_var, width=30).grid(row=1, column=1, padx=10, pady=5, columnspan=3)
        
        self.start_btn = ttk.Button(self.root, text="Start", command=self.start_timer)
        self.start_btn.grid(row=2, column=0, padx=10, pady=10)
        
        self.stop_btn = ttk.Button(self.root, text="Stop", command=self.stop_timer, state=tk.DISABLED)
        self.stop_btn.grid(row=2, column=1, padx=10, pady=10)
        
        self.pause_btn = ttk.Button(self.root, text="Pause", command=self.pause_timer, state=tk.DISABLED)
        self.pause_btn.grid(row=2, column=2, padx=10, pady=10)
        
        self.resume_btn = ttk.Button(self.root, text="Resume", command=self.resume_timer, state=tk.DISABLED)
        self.resume_btn.grid(row=2, column=3, padx=10, pady=10)
        
        ttk.Label(self.root, text="Elapsed Time:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(self.root, textvariable=self.timer_var, style="Timer.TLabel").grid(row=3, column=1, padx=10, pady=5, columnspan=3)
        
        # Initialize timer var
        self.timer_var.set("")
        
    def start_timer(self):
        self.start_time = datetime.now()
        self.start_btn['state'] = tk.DISABLED
        self.stop_btn['state'] = tk.NORMAL
        self.pause_btn['state'] = tk.NORMAL
        self.update_timer()
        
    def stop_timer(self):
        end_time = datetime.now()
        elapsed_time = end_time - self.start_time + self.total_paused_time
        hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        duration = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        
        self.start_btn['state'] = tk.NORMAL
        self.stop_btn['state'] = tk.DISABLED
        self.pause_btn['state'] = tk.DISABLED
        self.resume_btn['state'] = tk.DISABLED
        
        # Save to CSV
        self.save_to_csv(duration)
        
        # Reset task and project entries and the timer
        self.task_var.set("")
        self.project_var.set("")
        self.timer_var.set("")
        self.start_time = None  # Reset the start time
        self.total_paused_time = timedelta()  # Reset the total paused time
        
    def pause_timer(self):
        self.total_paused_time += datetime.now() - self.start_time
        self.start_time = None  # Reset the start time
        self.pause_btn['state'] = tk.DISABLED
        self.resume_btn['state'] = tk.NORMAL
        
    def resume_timer(self):
        self.start_time = datetime.now()
        self.pause_btn['state'] = tk.NORMAL
        self.resume_btn['state'] = tk.DISABLED
        self.update_timer()
        
    def update_timer(self):
        if self.start_time:
            elapsed_time = datetime.now() - self.start_time + self.total_paused_time
            hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            self.timer_var.set(f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}")
            self.root.after(1000, self.update_timer)  # Update every second
            
    def save_to_csv(self, duration):
        if not os.path.exists("work_log.csv"):
            with open("work_log.csv", "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Task', 'Project', 'Start Time', 'End Time', 'Duration'])
        with open("work_log.csv", "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.task_var.get(), self.project_var.get(), self.start_time.strftime('%Y-%m-%d %H:%M:%S'), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), duration])
        
root = tk.Tk()
app = TimeTracker(root)
root.mainloop()
