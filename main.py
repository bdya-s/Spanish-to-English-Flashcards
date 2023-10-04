import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
en_translation = ""
pick = None

# If words_to_learn exists, read from it, else read from original list.
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/spanish_words.csv")
    data_dict = original_data.to_dict(orient="records")
else:
    data_dict = data.to_dict(orient="records")

#Show foreign word, wait for 3 secs and display answer
def next_card():
    global en_translation, flip_timer, pick
    window.after_cancel(flip_timer)
    pick = random.choice(data_dict)
    random_es_word = pick["Spanish"]
    en_translation = pick["English"]
    canvas.itemconfig(card_title, text="Spanish", fill="black")
    canvas.itemconfig(card_word, text=random_es_word, fill="black")
    canvas.itemconfig(front, image=card_front)

    flip_timer = window.after(3000, flip_card)

#flip card for answer
def flip_card():
    global en_translation
    canvas.itemconfig(front, image=card_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=en_translation, fill="white")

#If right guess, remove word from the list. Keep remaining words as words to learn.
def known_word():
    data_dict.remove(pick)
    remaining_data = pandas.DataFrame(data_dict)
    remaining_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

# -----------------------------MAIN--------------------------

window = Tk()
window.title("Spanish to English")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)

card_back = PhotoImage(file="images\card_back.png")
card_front = PhotoImage(file="images\card_front.png")

flip_timer = window.after(3000, flip_card)

# Canvas image and texts
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

image_wrong = PhotoImage(file="Images\wrong.png")
image_right = PhotoImage(file="Images\\right.png")

# Buttons
button_wrong = Button(image=image_wrong, highlightthickness=0, command=next_card)
button_wrong.grid(column=0, row=1)
button_right = Button(image=image_right, highlightthickness=0, command=known_word)
button_right.grid(column=1, row=1)

next_card()



window.mainloop()

