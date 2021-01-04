#!/usr/bin/env python
import tkinter as tk
from tkinter import ttk
# dir(ttk)
root = tk.Tk()
root.minsize(300, 200)
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)
# btn = ttk.Button(frame, text="test")
# btn.pack()
# widget = ttk.Label(frame, text="test")
# widget.pack()
widget = ttk.Entry(frame)
widget.pack()
root.mainloop()
