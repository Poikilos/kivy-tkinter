#!/usr/bin/env python
import tkinter as tk
from tkinter import ttk
root = tk.Tk()
root.minsize(300, 200)
outerFrame = ttk.Frame(root)
outerFrame.pack(fill=tk.BOTH, expand=True)
widget = ttk.Label(outerFrame, text="This is a very long label.")
widget.grid()


frame = ttk.Frame(outerFrame)
frame.grid()
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

# NOTE: using the variable for the param in the lambda doesn't work--
# it is always B2 when called.

thisId = 'A1'
ids[thisId] = ttk.Button(frame, text=thisId,
                         command=lambda: forget_click('A1'))
ids[thisId].opacity = 1
ids[thisId].grid(row=0, column=0)

thisId = 'A2'
ids[thisId] = ttk.Button(frame, text=thisId,
                         command=lambda: forget_click('A2'))
ids[thisId].opacity = 1
ids[thisId].grid(row=1, column=0)

thisId = 'B1'
ids[thisId] = ttk.Button(frame, text=thisId,
                         command=lambda: forget_click('B1'))
ids[thisId].opacity = 1
ids[thisId].grid(row=0, column=1)

thisId = 'B2'
ids[thisId] = ttk.Button(frame, text=thisId,
                         command=lambda: forget_click('B2'))
ids[thisId].opacity = 1
ids[thisId].grid(row=1, column=1)

root.mainloop()
