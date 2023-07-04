from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
  letters = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
    'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
    'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
  ]
  numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
  symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

  # Randoms letters between 8 and 10 letters
  password_letters = [choice(letters) for char in range(randint(8, 10))]
  # Randoms symbols between 2 and 4 letters
  password_symbols = [choice(letters) for char in range(randint(2, 4))]
  # Randoms numbers between 2 and 4 letters
  password_numbers = [choice(letters) for char in range(randint(2, 4))]

  # Combines the three aboves lists into one
  password_list = password_letters + password_symbols + password_numbers

  # Shuffles the list in a random order
  shuffle(password_list)

  # Join the elements from the list into a single string
  password = "".join(password_list)

  '''
  Insert the password into the 'password_input' field
  Insert method takes two arguments: index 0 (indicating that the password should be inserted 
  at the beginning of the input field) and the password string (the value to be inserted
  '''
  password_input.insert(0, password)

  '''
  The copy() function from the Pyperclip module is called with the argument password. 
  This will copy the value of the password variable to the clipboard.
  '''
  pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_data():
  '''
  The code website = website_input.get() is used in a Tkinter Python application to retrieve the 
  input from a text entry field and assign it to the variable website (the same goes for email and password)
  '''
  website = website_input.get()
  email = email_input.get()
  password = password_input.get()

  # Add the data to a dictionary
  new_data = {website: {"email": email, "password": password}}

  # If there is no data in the website_input or the password_input show the following error message
  if website_input.get() == "" or password_input.get() == "":
    messagebox.showinfo(title="Oops",
                        message="Please don't leave any field empty!")
  else:
    # If all fields are not empty try the following
    try:
      # The code opens the "data.json" file, reads its contents, and stores the deserialized JSON data in the data_file variable
      with open("data.json", 'r') as data:
        data_file = json.load(data)
    except FileNotFoundError:

      # This code opens the file "data.json" in write mode and writes the JSON representation of the new_data object to the file
      with open("data.json", "w") as data:
        json.dump(new_data, data, indent=4)
    else:
      # The code updates a file (data_file) with new data (new_data) and then saves the updated dictionary to a JSON file ("data.json")
      data_file.update(new_data)
      with open("data.json", "w") as data:
        json.dump(data_file, data, indent=4)
    finally:
      # Deletes the website_input and password_input field for new entry and focuses on the website_input field
      website_input.delete(0, END)
      password_input.delete(0, END)
      website_input.focus()


# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
  '''
  The code website = website_input.get() is used in a Tkinter Python application to retrieve 
  the input from a text entry field and assign it to the variable website.
  '''
  website = website_input.get()
  try:
    # Try to open the file
    with open("data.json") as data:
      data_file = json.load(data)
  except FileNotFoundError:
    # If no file (data) exists, show the following message box
    messagebox.showinfo(title='Error', message='No data file found.')
  else:
    # If there is data and the data contains a website with that name show the following info
    if website in data_file:
      messagebox.showinfo(
        title=website,
        message=
        f"Email: {data_file[website]['email']}\n Password: {data_file[website]['password']}"
      )
    # If there is no website with that name show the following message box
    else:
      messagebox.showinfo(title='Error',
                          message=f'Not details for {website} exists')

  # ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title('Password Manager')
# Add 50px padding in x and y direction
window.config(padx=50, pady=50)

# Create canvas with 200px width and height
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file='logo.png')
# Load image with 100px width and height
canvas.create_image(100, 100, image=logo_img)
# Image position
canvas.grid(row=0, column=1)

### LABELS ###
website_label = Label(text='Website:')
website_label.grid(row=1, column=0)

email_label = Label(text='Email/Username:')
email_label.grid(row=2, column=0)

password_label = Label(text='Password:')
password_label.grid(row=3, column=0)

### INPUTS ###
website_input = Entry(width=21)
website_input.focus()
website_input.grid(row=1, column=1)

email_input = Entry(width=35)
email_input.insert(
  0, 'ENTER YOUR EMAIL SO THAT YOU DO NOT HAVE TO WRITE IT EVERYTIME')
email_input.grid(row=2, column=1, columnspan=2)

password_input = Entry(width=21)
password_input.grid(row=3, column=1)

### BUTTONS ###
# When this button is clicked call password_generator function
generate_password = Button(text='Generate Password',
                           command=password_generator)
generate_password.grid(row=3, column=2)

# When this button is clicked call add_data function
add_password = Button(text='Add', width=35, command=add_data)
add_password.grid(row=4, column=1, columnspan=2)

# When this button is clicked call find_password function
search_password = Button(text="Search", command=find_password, width=13)
search_password.grid(row=1, column=2)

window.mainloop()
