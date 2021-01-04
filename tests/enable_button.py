#!/usr/bin/env python
import tkinter as tk
from tkinter import ttk
root = tk.Tk()
root.minsize(300, 200)
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)
# btn = ttk.Button(frame, text="test")
# btn.pack()
# widget = ttk.Label(frame, text="test")
# widget.pack()

ids = {}

def forget_click(senderId):
    print("clicked {}".format(senderId))
    for k,v in ids.items():
        if k == senderId:
            v.grid_remove()
            # ^ remembers position in grid (grid_forget does not)
        else:
            v.grid()

def enable_A1():
    thisId = 'A1'
    ids[thisId].configure(command=lambda: forget_click('A1'))

def enable_B1():
    thisId = 'B1'
    ids[thisId].configure(state=tk.NORMAL)

# NOTE: using the variable for the param in the lambda doesn't work--
# it is always B2 when called.

thisId = 'A1'
ids[thisId] = ttk.Button(frame, text=thisId)
ids[thisId].opacity = 1
ids[thisId].grid(row=0, column=0)

thisId = 'A2'
ids[thisId] = ttk.Button(frame, text="Add Command to A1",
                         command=enable_A1)
ids[thisId].opacity = 1
ids[thisId].grid(row=1, column=0)

thisId = 'B1'
ids[thisId] = ttk.Button(frame, text=thisId,
                         command=lambda: forget_click('B1'),
                         state=tk.DISABLED)
ids[thisId].opacity = 1
ids[thisId].grid(row=0, column=1)

thisId = 'B2'
ids[thisId] = ttk.Button(frame, text="Enable B1",
                         command=enable_B1)
ids[thisId].opacity = 1
ids[thisId].grid(row=1, column=1)

root.mainloop()
