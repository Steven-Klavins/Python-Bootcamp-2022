from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
from pyperclip import copy
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []

    [password_list.append(char) for char in (choice(letters) for num in range(randint(8, 10)))]
    [password_list.append(char) for char in (choice(symbols) for num in range(randint(2, 4)))]
    [password_list.append(char) for char in (choice(numbers) for num in range(randint(2, 4)))]

    shuffle(password_list)

    password = "".join(password_list)
    pass_input.insert(0.0, password)
    copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_password():
    web_address = web_input.get("1.0", "end-1c").strip()
    email_address = email_input.get("1.0", "end-1c").strip()
    password = pass_input.get("1.0", "end-1c").strip()

    # Check if website already exists, if so prompt user to confirm they wish to override

    new_data = {
        web_address: {
            "email": email_address,
            "password": password,
        }
    }

    if web_address == "" or email_address == "" or password == "":
        messagebox.showinfo(title="Validation Error", message="Please ensure all fields are included.")
    else:
        is_ok = messagebox.askokcancel(title=web_address, message="Are you happy with the details entered?\n"
                                                                  f"Website: {web_address}\n"
                                                                  f"Email: {email_address}\n"
                                                                  f"Password: {password}")
        if is_ok:
            try:
                with open('data.json', 'r') as file:
                    # Read Data
                    data = json.load(file)
                    # Update Data
                    data.update(new_data)

            except FileNotFoundError:
                # Dump data into new file
                with open('data.json', 'w') as file:
                    json.dump(new_data, file, indent=4)

            else:
                with open('data.json', 'w') as file:
                    # If file found with try, dump the updated new data
                    json.dump(data, file, indent=4)

            finally:
                # Clear the inputs
                web_input.delete("1.0", "end-1c")
                pass_input.delete("1.0", "end-1c")


# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    try:
        search = web_input.get("1.0", "end-1c").strip()
        with open('data.json', 'r') as file:
            # Read Data
            data = json.load(file)[search]

    except (KeyError, FileNotFoundError) as e:
        # Dump data into new file
        messagebox.showinfo(title="Not found", message=f"No results found for {search}")
    else:
        # Copy data to clipboard
        copy(data['password'])
        messagebox.showinfo(title=search, message=f"Your password for {search} is {data['password']}\n" "Copied to "
                                                  "clipboard!")


# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Canvas
canvas = Canvas(width="200", height="200")

# Image
padlock_logo = PhotoImage(file="./logo.png")
canvas.create_image(100, 100, image=padlock_logo)
canvas.grid(row=0, column=1)

# -------------------------- Website ------------------------------- #

web_label = Label(text="Website:")
web_label.grid(row=1, column=0)

web_input = Text(height=1, width=21)
web_input.grid(row=1, column=1, columnspan=1)
web_input.focus()

# ---------------------------- Email ------------------------------- #

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

email_input = Text(height=1, width=35)
email_input.grid(row=2, column=1, columnspan=2)
email_input.insert(0.0, "email@email.com")

# --------------------------- Password ------------------------------ #

pass_label = Label(text="Password:")
pass_label.grid(row=3, column=0)

pass_input = Text(height=1, width=21)
pass_input.grid(row=3, column=1)

# ---------------------------- Buttons ------------------------------ #

search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(row=1, column=2, columnspan=1)

gen_button = Button(text="Generate Password", width=15, command=generate_password)
gen_button.grid(row=3, column=2)

add_button = Button(text="Add", width=40, command=save_password)
add_button.grid(row=4, column=1, columnspan=3)

window.mainloop()
