import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os


class SimpleGreenTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple Green Tracker")
        self.root.geometry("1200x800")
        self.root.configure(bg="#e8f5e9")

        # Daily tips (moved before create_interface)
        self.daily_tips = [
            "Try walking or cycling to work today!",
            "Remember to turn off lights when leaving a room",
            "Use a reusable water bottle",
            "Take shorter showers to save water",
            "Recycle your paper waste",
            "Use public transportation",
            "Plant a tree or care for existing plants",
            "Use energy-efficient LED bulbs",
            "Compost your food waste",
            "Use reusable shopping bags"
        ]

        # Initialize data storage
        self.data_file = "green_data.json"
        self.load_data()

        # Create main interface
        self.create_interface()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                'actions': [],
                'total_points': 0,
                'daily_goals': 5
            }

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f)

    def create_interface(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Daily Tip Section
        tip_frame = ttk.LabelFrame(main_frame, text="Today's Green Tip", padding="10")
        tip_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        self.tip_label = ttk.Label(tip_frame, text=self.get_daily_tip(), wraplength=400)
        self.tip_label.grid(row=0, column=0, pady=5)

        ttk.Button(tip_frame, text="New Tip", command=self.update_tip).grid(row=1, column=0, pady=5)

        # Quick Actions Section
        actions_frame = ttk.LabelFrame(main_frame, text="Quick Actions", padding="10")
        actions_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        self.create_quick_actions(actions_frame)

        # Progress Section
        progress_frame = ttk.LabelFrame(main_frame, text="Your Progress", padding="10")
        progress_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        self.points_label = ttk.Label(progress_frame, text=f"Total Green Points: {self.data['total_points']}")
        self.points_label.grid(row=0, column=0, pady=5)

        self.goal_label = ttk.Label(progress_frame, text=f"Daily Goal: {self.data['daily_goals']} actions")
        self.goal_label.grid(row=1, column=0, pady=5)

        # Recent Actions Section
        recent_frame = ttk.LabelFrame(main_frame, text="Recent Actions", padding="10")
        recent_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        self.recent_text = tk.Text(recent_frame, height=8, width=50)
        self.recent_text.grid(row=0, column=0, pady=5)
        self.update_recent_actions()

        # Settings Section
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(settings_frame, text="Daily Goal:").grid(row=0, column=0, padx=5)
        self.goal_var = tk.StringVar(value=str(self.data['daily_goals']))
        ttk.Entry(settings_frame, textvariable=self.goal_var, width=10).grid(row=0, column=1, padx=5)

        ttk.Button(settings_frame, text="Update Goal", command=self.update_goal).grid(row=0, column=2, padx=5)

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

    def create_quick_actions(self, parent):
        actions = [
            ("Walk/Cycle", 10),
            ("Public Transport", 8),
            ("Turn Off Lights", 3),
            ("Recycle", 5),
            ("Save Water", 3),
            ("Plant Care", 5),
            ("LED Bulbs", 5),
            ("Compost", 8)
        ]

        for i, (action, points) in enumerate(actions):
            row = i // 2
            col = i % 2
            btn = ttk.Button(
                parent,
                text=f"{action} (+{points})",
                command=lambda a=action, p=points: self.record_action(a, p)
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky=(tk.W, tk.E))

    def get_daily_tip(self):
        today = datetime.now().day
        return self.daily_tips[today % len(self.daily_tips)]

    def update_tip(self):
        self.tip_label.config(text=self.get_daily_tip())

    def record_action(self, action, points):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.data['actions'].append({
            'action': action,
            'points': points,
            'timestamp': timestamp
        })
        self.data['total_points'] += points

        # Keep only last 10 actions
        if len(self.data['actions']) > 10:
            self.data['actions'] = self.data['actions'][-10:]

        self.save_data()
        self.update_recent_actions()
        self.points_label.config(text=f"Total Green Points: {self.data['total_points']}")

        messagebox.showinfo("Success", f"Recorded: {action} (+{points} points)")

    def update_recent_actions(self):
        self.recent_text.delete(1.0, tk.END)
        for action in reversed(self.data['actions']):
            self.recent_text.insert(tk.END,
                                    f"{action['timestamp']}: {action['action']} (+{action['points']} points)\n")

    def update_goal(self):
        try:
            new_goal = int(self.goal_var.get())
            if new_goal > 0:
                self.data['daily_goals'] = new_goal
                self.save_data()
                self.goal_label.config(text=f"Daily Goal: {new_goal} actions")
                messagebox.showinfo("Success", "Daily goal updated!")
            else:
                messagebox.showerror("Error", "Goal must be positive")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = SimpleGreenTracker()
    app.run()