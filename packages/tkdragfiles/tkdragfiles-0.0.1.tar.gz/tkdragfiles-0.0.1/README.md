<div align="center">
    
[![PyPI](https://img.shields.io/pypi/v/tkdragfiles)](https://pypi.org/project/tkdragfiles/)

</div>

# Easy Drag Files and Drop to Tkinter

Only for windows

## Installation
```shell
pip3 install tkdragfiles
pip3 install async_tkinter_loop #if u need asyncio
```
## Easy to use 
```python
#for normal tk
import tkinter as tk
from tkdragfiles import start_dragfiles_event

root = tk.Tk()
root.geometry("600x200")
lb = tk.Listbox(root, height=500, width=500, selectmode=tk.SINGLE)
lb.pack()

def callback(file_paths):
    for file_path in file_paths:
        lb.insert("end", file_path)

start_dragfiles_event(root,callback)
root.mainloop()
```
```python
#for asyncio tk
import tkinter as tk
from tkdragfiles import start_dragfiles_event

root = tk.Tk()
root.geometry("600x200")
lb = tk.Listbox(root, height=500, width=500, selectmode=tk.SINGLE)
lb.pack()

def callback(file_paths):
    for file_path in file_paths:
        lb.insert("end", file_path)

start_dragfiles_event(root,callback)
root.mainloop()
```

## References
