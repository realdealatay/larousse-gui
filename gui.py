import webbrowser
import re
import sys
import os
import  tkinter as tk
import tkinter.messagebox as tk1
import tkinter.filedialog
from pathlib import Path
import requests
import unicodedata
from bs4 import BeautifulSoup 
from tkinter import END, Tk, Canvas, Text

ASSETS_PATH = Path(__file__).resolve().parent / "assets"

# Pour importer les photos et assets dans le code
path = getattr(sys, '_MEIPASS', os.getcwd())
os.chdir(path)

DISABLED = "disabled"

#Pour le fenetre de l'appli
window = Tk()
canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 600,
    width = 900,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    367.0,
    600.0,
    fill="#2F63D9",
    outline="")

#La definition de definition larousse
def get_definitions(word):

    definitions = []

    url = "https://www.larousse.fr/dictionnaires/francais/" + word.lower()
    soup = BeautifulSoup(requests.get(url=url).text, 'html.parser')

    for definition in soup.select('.Definitions .DivisionDefinition:first-child'):
        definitions.append(unicodedata.normalize("NFKD", definition.text))

    aligned_definitions = [definition.ljust(50) for definition in definitions]
    aligned_definitions = [definition[3:] if definition.startswith("1. ") else definition for definition in aligned_definitions]

    return '\n'.join(aligned_definitions)




    
#Boutton instruction
def know_more_clicked(event):
    instructions = (
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    webbrowser.open_new_tab(instructions)


def make_label(master, x, y, h, w, *args, **kwargs):
    f = tk.Frame(master, height=h, width=w)
    f.pack_propagate(0)  # don't shrink
    f.place(x=x, y=y)

    label = tk.Label(f, *args, **kwargs)
    label.pack(fill=tk.BOTH, expand=1)

    return label

#Infos du fenetre
window.geometry("862x519")
window.configure(bg = "#3A7FF6",)
window.title("Larousse App | by atay")

canvas = tk.Canvas(
    window, bg="#3A7FF6", height=519, width=862,
    bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
canvas.create_rectangle(431, 0, 431 + 431, 0 + 519, fill="#FCFCFC", outline="")
canvas.create_rectangle(40, 160, 40 + 60, 160 + 5, fill="#FCFCFC", outline="")

text_box_bg = tk.PhotoImage(file=ASSETS_PATH / "TextBox_Bg.png")
token_entry_img = canvas.create_image(650.5, 167.5, image=text_box_bg)

#Storage du donne entrée dans le "entry"
larous_entry = tk.Entry(bd=0, bg="#F6F7F9",fg="#000716",  highlightthickness=0)
larous_entry.place(x=490.0, y=137+25, width=321.0, height=35)
larous_entry.focus()

#affichage du resultat

result = entry_2 = Text(
    bd=0,
    fg="#515486",
    bg="#F6F7F9",
    highlightthickness=0,
    font=("Arial-BoldMT", 18 * -1),

)


entry_2.place(
    x=480.0,
    y=230.0,
    width=348.0,
    height=112.0
)

#Boutton du "Generate"
def btn_clicked():
    entry_2.delete(1.0, END)
    source = str(larous_entry.get())
    trasnlate = get_definitions(source)
    result.insert(END, trasnlate)
    result.tag_configure('left', justify='left')
    result.tag_add("left", 1.0, "end")

entry_2.bind('<Return>', btn_clicked)


#Les textes dans le code
canvas.create_text(
    490.0, 156.0, text="Word", fill="#515486",
    font=("Arial-BoldMT", int(13.0)), anchor="w")
canvas.create_text(
    646.5, 428.5, text="Generate",
    fill="#FFFFFF", font=("Arial-BoldMT", int(13.0)))
canvas.create_text(
    600.0, 88.0, text="Search for definitions.",
    fill="#515486", font=("Arial-BoldMT", int(22.0)))


title = tk.Label(
    text="Welcome to Larousse App", bg="#3A7FF6",
    fg="white", font=("Arial-BoldMT", int(20.0)))
title.place(x=27.0, y=120.0)

info_text = tk.Label(
    text="Larousse App uses larousse-api\n"
    "to get a definition from the website,\n"
    "then presents to you easily without ads.\n"
    "Enjoy !\n\n"

    "This project is made with\n"
    "<3 by Atay.",
    bg="#3A7FF6", fg="white", justify="left",
    font=("Georgia", int(16.0)))

info_text.place(x=27.0, y=200.0)

know_more = tk.Label(
    text="Click here for instructions",
    bg="#3A7FF6", fg="white", cursor="hand2")
know_more.place(x=27, y=400)
know_more.bind('<Button-1>', know_more_clicked)

generate_btn_img = tk.PhotoImage(file=ASSETS_PATH / "generate.png")
generate_btn = tk.Button(
    image=generate_btn_img, borderwidth=0, highlightthickness=0,
    command=btn_clicked, relief="flat")
generate_btn.place(x=557, y=401, width=180, height=55)

window.resizable(False, False)
window.mainloop()