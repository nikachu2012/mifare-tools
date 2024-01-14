import dearpygui.dearpygui as dpg
import tkinter
import tkinter.filedialog as filedialog


def saveFile(text: str):
    root = tkinter.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        filetypes=[("Plain text", ".txt"), ("Log file", ".log")],
        defaultextension="bmp",
        initialdir="./"
    )
    root.destroy()

    with open(file_path, 'w', encoding="utf-8") as f:
        f.write(text)
    pass


def saveFileBinary(text: bytes):
    root = tkinter.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        filetypes=[("Binary File", ".bin"), ("Binary Data File", ".dat")],
        defaultextension="bmp",
        initialdir="./"
    )
    root.destroy()

    with open(file_path, 'wb') as f:
        f.write(text)
    pass
