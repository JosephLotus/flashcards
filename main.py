from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/spanish_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

# Show next word function


def next_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    card_front.itemconfig(card_word, text=current_card["Spanish"])
    card_front.itemconfig(card_background, image=card_front_img)
    card_front.itemconfig(card_word, fill="black")
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    card_front.itemconfig(card_word, text=current_card["English"], fill="white")
    card_front.itemconfig(card_background, image=card_back_img)


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_word()


# Set up UI
window = Tk()
window.title("Flashcards")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

flip_timer = window.after(3000, func=flip_card)

card_front = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = card_front.create_image(400, 263, image=card_front_img)
card_word = card_front.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
card_front.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_front.grid(column=0, row=0, columnspan=2)

cross_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_img, command=next_word)
unknown_button.config(highlightthickness=0)
unknown_button.grid(column=0, row=1)

check_img = PhotoImage(file="images/right.png")
known_button = Button(image=check_img, command=is_known)
known_button.config(highlightthickness=0)
known_button.grid(column=1, row=1)

next_word()

window.mainloop()
