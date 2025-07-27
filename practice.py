import time
from tkinter import *

gotText = False
i = 0
mistake = 0
sentence = ("In a cozy village nestled among rolling hills, there lived a little girl named Lily. Every day, \n"
            "she would wander into the meadow, where a sparkling stream bubbled merrily. One day, while skipping \n"
            "stones, she spotted a peculiar rock that seemed to shimmer with secrets. Curiosity tugging at her, \n"
            "Lily picked it up, and suddenly, she felt a rush of warmth enveloping her. Colors danced before her \n"
            "eyes, and she understood the language of the birds and the whispers of the trees. With a joyful heart, \n"
            "Lily realized that the world was full of wonders waiting to be discovered, and she skipped back to the \n"
            "village, eager to share her newfound wisdom with her friends and family.\n")


def labelChange():
    label.config(text=sentence)


def sub60():
    global mistake, i
    entry.destroy()
    sen = text.get()
    worL = sen.split()
    senL = sentence.split()
    for x in worL:
        if x != senL[i]:
            mistake += 1
        i += 1
    label.config(text=f"Your typing speed is {len(worL)} wpm with {mistake} mistakes while typing words.")


window = Tk()
window.config(padx=100, pady=100)

text = StringVar()

label = Label(window)
label.grid(row=0, column=0)
labelChange()

entry = Entry(window, textvariable=text)
entry.grid(row=1, column=0)
window.after(63000, sub60)

window.mainloop()