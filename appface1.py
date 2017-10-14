from pediatric_general import pediatric_general
import tkinter as tk
from tkinter import filedialog





root = tk.Tk()
root.withdraw()
file_paths = filedialog.askopenfilename()

createstuff = pediatric_general(file_paths)
createstuff.sort()

