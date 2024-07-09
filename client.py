import socket
import threading
import random
import time
import tkinter as tk
from tkinter import ttk

class CarClient:
    def __init__(self, host='localhost', port=65432):
        self.host = host
        self.port = port
        self.socket = None

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Car Client")

        # Variables
        self.bridge_state = tk.StringVar()
        self.bridge_state.set('Free')
        self.speed = tk.DoubleVar(value=1.0)
        self.delay = tk.DoubleVar(value=5.0)
        self.direction = tk.StringVar(value="North")

        # GUI Layout
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        # Speed input
        tk.Label(frame, text="Speed:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.speed).grid(row=0, column=1, padx=5, pady=5)

        # Delay input
        tk.Label(frame, text="Delay after crossing:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.delay).grid(row=1, column=1, padx=5, pady=5)

        # Direction input
        tk.Label(frame, text="Initial Direction:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Combobox(frame, textvariable=self.direction, values=["North", "South"]).grid(row=2, column=1, padx=5, pady=5)

        # Bridge state display
        tk.Label(frame, text="Bridge State:").grid(row=3, column=0, padx=5, pady=5)
        tk.Label(frame, textvariable=self.bridge_state).grid(row=3, column=1, padx=5, pady=5)

        # Start button
        tk.Button(frame, text="Start", command=self.start_client).grid(row=4, columnspan=2, pady=10)

        self.root.mainloop()

    def start_client(self):
        threading.Thread(target=self.client_thread).start()

    def client_thread(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            self.socket = s
            threading.Thread(target=self.receive_updates).start()
            while True:
                time.sleep(self.delay.get() * random.uniform(0.5, 1.5))  # Wait before attempti
