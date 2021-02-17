import sys
import tkinter as tk
from tkinter import scrolledtext, Canvas
from tkinter.filedialog import askopenfilename
from tkinter.font import Font
from PIL import ImageTk,Image
import webbrowser
import os


previous_text_starts_at=0


def open_git_page(event):
    webbrowser.open_new(r"https://github.com/sairash/text_game_maker")

def open_file():
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.tgm")]
    )
    if not filepath:
        return
    txt_edit.delete(1.0, tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"Text Game Maker - {filepath}")



def save_file():
    """Save the current file as a new file."""
    with open('game.tgm', "w") as output_file:
        text = txt_edit.get(1.0, tk.END).split("\n")
        text = "\n".join(text[:-1])
        if text != '\r':
            output_file.write(text)
    window.title(f"Text Game Maker")


def run_file():
    os.system('cmd /k "python --version"')


def key_binds(event):
    txt_edit.tag_delete('here')
    global previous_text_starts_at, previous_text_ends_at
    if event.keysym == 'o':
        open_file()
    elif event.keysym == 's':
        save_file()

    for syntax_line in range(int(float(txt_edit.index('end')))):
        print(syntax_line)
        index =  txt_edit.search(r'\[*\]', str(float(syntax_line)), tk.END, regexp=True)
        txt_edit.tag_add("here", str(float(syntax_line)+0.1), index)
    
    txt_edit.tag_config("here", foreground="green")

def make_bold():

    # tk.TclError exception is raised if not text is selecte
    try:
        txt_edit.tag_add("BOLD", "sel.first", "sel.last")
    except tk.TclError:
        pass




window = tk.Tk()
window.title("Text Game Maker")
window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

  
photo = ImageTk.PhotoImage(file = "book_logo_tU5_icon.ico")
window.iconphoto(False, photo)


txt_edit = scrolledtext.ScrolledText(window,  wrap = tk.WORD, font = ("Times New Roman", 15))

fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
canvas = Canvas(fr_buttons, width = 100, height = 124.4, cursor="hand2")

git_sairash = tk.Label( fr_buttons, text='git: @sairash' , cursor="hand2")
btn_new = tk.Button(fr_buttons, text="New", command=save_file, cursor="hand2")
btn_open = tk.Button(fr_buttons, text="Open", command=open_file, cursor="hand2")
btn_save = tk.Button(fr_buttons, text="Save", command=save_file, cursor="hand2")
btn_run = tk.Button(fr_buttons, text="Run", command=run_file, cursor="hand2")

canvas.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_new.grid(row=1, column=0, sticky="ew", padx=5)
btn_open.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=3, column=0, sticky="ew", padx=5)
btn_run.grid(row=4, column=0, sticky="ew", padx=5)
git_sairash.grid(row=5, column=0, sticky="ew", padx=5)

fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")

image = Image.open('book_logo.png')
image = image. resize((100, 124), Image. ANTIALIAS) 
img = ImageTk.PhotoImage(image)
canvas.create_image(5,5, anchor='nw', image=img) 

git_sairash.bind("<Button-1>", open_git_page)
canvas.bind("<Button-1>", open_git_page)
window.bind("<Control-s>", key_binds)
window.bind("<Control-o>", key_binds)
txt_edit.bind("[",key_binds)

txt_edit.focus_set()

window.mainloop()