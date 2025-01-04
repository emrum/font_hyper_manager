# dialogs.py

import tkinter as tk
from tkinter import ttk

class ScrollableDialog:
    def __init__(self, parent, width=400, height=300):
        self.parent = parent  # Store parent reference
        self.window = tk.Toplevel(parent)
        self.window.title("Scrollable Dialog")
        self.window.geometry(f"{width}x{height}")
        self.window.protocol("WM_DELETE_WINDOW", self.close)  # Handle window close button
        self.window.withdraw()  # hide window

    def show(self, title, text):
        self.window.title(title)

        # Make the dialog stay on top
        self.window.attributes("-topmost", True)

        # Create a frame for the Text and Scrollbar
        frame = ttk.Frame(self.window)
        frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        # Create a Scrollbar
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Create a Text widget
        self.text = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        self.text.grid(row=0, column=0, sticky="nsew")

        # Configure the scrollbar
        scrollbar.config(command=self.text.yview)

        # Insert text
        self.text.delete('1.0', tk.END)
        self.text.insert(tk.END, text)

        # Create a Close button
        close_button = ttk.Button(self.window, text="Close", command=self.close)
        close_button.grid(row=1, column=0, pady=10)

        # Configure column and row weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        # Center the window on parent
        self.window.transient(self.parent)  # Make window modal
        self.window.grab_set()  # Make window modal
        
        self.window.deiconify()  # show the dialog window
        
        # focus to close button
        close_button.focus_set()

    def close(self):
        self.window.grab_release()  # Release modal state
        self.window.destroy()
        self.window = None  # Clear the reference
#
