from tkinter import *
from tkinter import filedialog
import os
import logic

directorio = os.getcwd()
archivo = None

def openFile():
    global archivo
    archivo = filedialog.askopenfilename(   initialdir=directorio,
                                            title="Abrir archivo",
                                            filetypes= (("excel","*.xlsx"),
                                            ("todos los archivos","*.*")))

window = Tk()
abrir = Button(text="Abrir",command=openFile)
abrir.pack()
computar = Button(text="Computar", command=lambda: logic.computar(archivo))
computar.pack()
window.mainloop()