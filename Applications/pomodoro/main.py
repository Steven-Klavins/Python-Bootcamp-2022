from tkinter import *
import math
import time
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

reps = 0
checks = ""
timer = None

# ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    global checks
    global reps
    global timer
    window.after_cancel(timer)
    checks = ""
    reps = 0
    check_box.config(text="")
    title_label.config(text="Timer")
    canvas.itemconfig(timer_text, text="00:00")

# ---------------------------- TIMER MECHANISM ------------------------------- #

def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break = SHORT_BREAK_MIN * 60
    long_break = LONG_BREAK_MIN * 60

    if reps == 8:
        title_label.config(text="Break", fg=RED)
        count_down(long_break)
    elif reps % 2 == 0:
        count_down(short_break)
        title_label.config(text="Break", fg=PINK)
    else:
        count_down(work_sec)
        title_label.config(text="Work", fg=GREEN)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def count_down(count):
    mins = math.floor(count/60)
    seconds = count % 60

    if seconds < 10:
        seconds = f"0{seconds}"

    canvas.itemconfig(timer_text, text=str(f"{mins}:{seconds}"))
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        if reps % 2 == 0:
            global checks
            checks = checks + " ✓"
            check_box.config(text=checks)


# ---------------------------- UI ------------------------------- #


# Window
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

# Title
title_label = Label(text="Timer", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 35, "bold"))
title_label.grid(row=0, column=1)

# Canvas
canvas = Canvas(width="200", height="224", bg=YELLOW, highlightthickness=0)

# Image
tomato_image = PhotoImage(file="./tomato.png")
canvas.create_image(100, 112, image=tomato_image)

# Timer
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

# Button Left
button_left = Button(text="Start", command=start_timer)
button_left.grid(row=2, column=0)

# Check
check_box = Label(font=(FONT_NAME, 16, "bold"), bg=YELLOW, fg=GREEN)
check_box.grid(row=3, column=1)

# Button Right
button_right = Button(text="Reset", command=reset_timer)
button_right.grid(row=2, column=2)

window.mainloop()
