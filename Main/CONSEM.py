import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import os
from tkinter import PhotoImage
from tkinter import messagebox
from PIL import Image





# Preset credentials
admin_USERNAME = ["DIPSHIT", "jose", "benedict", "emmett", "fortniteBattlepassBro", "GarfieldPutmeanA", " "]
admin_PASSWORD = ["MOTHERFUCGGUR", "jose1", "benedict1", "emmett1", "chugJunk", "Please", " "]

# Function to validate login
def validate_login():
    username = entry_username.get()
    password = entry_password.get()
    
    # Check if the username and password are valid
    if username in admin_USERNAME and password in admin_PASSWORD:
        user_index = admin_USERNAME.index(username)
        # Check if the password matches the username by index
        if admin_PASSWORD[user_index] == password:
            open_menu(username)
        else:
            messagebox.showerror("Error", "Invalid username or password")
    else:
        messagebox.showerror("Error", "Invalid username or password")









#window = root = application 
window = tk.Tk()
window.title("CON-SEM v1.0.0.0");
window.iconbitmap("C:/Users/temmy/OneDrive/Desktop/CONSEM/dist/IMG_SRC/ICONIC.ico")
window.attributes('-fullscreen', True)
#window.attributes('-alpha', 0)
#window.attributes('-toolwindow', 1)
#window.attributes('-topmost', FALSE)
window.geometry("+-10+0")
#window.configure("-state", false)

#Close Window
def handle_button_press(event):
    window.destroy()


def handle_admin_button_press(event):
    adminwindow = tk.Tk()
    adminwindow.title("Hello World")










#button.pack(anchor=tk.NW)




DesktopImage = ImageTk.PhotoImage(Image.open("C:/Users/temmy/OneDrive/Desktop/CONSEM/IMG_SRC/102237.jpg"))
panel = Label(window, image = DesktopImage)
panel.pack(side = "bottom", fill = "both", expand = "yes")



twitterIcon = PhotoImage(file = "IMG_SRC/TWIT.png") 
chatIcon = PhotoImage(file = "IMG_SRC/CHAT.png") 
adminToolIcon = PhotoImage(file= "IMG_SRC/TOOL.png")
xbutton = PhotoImage(file="IMG_SRC/x.png")
animatedBackgroundTest = PhotoImage(file ="IMG_SRC/giphy.gif")


#twitter
button = tk.Button(text=" ", image=twitterIcon)
button.bind("<Button-1>", handle_button_press)
button.place(x=50, y=50, width=150, height=150)

#chat box
button = tk.Button(text=" ", image=chatIcon)
button.bind("<Button-1>", handle_button_press)
button.place(x=50, y=250, width=150, height=150)

#admin tools
button = tk.Button(text=" ", image=adminToolIcon)
button.bind("<Button-1>", handle_admin_button_press)
button.place(x=50, y=450, width=150, height=150)


#close window
button = tk.Button(text=" ", image=xbutton)
button.bind("<Button-1>", handle_button_press)
button.place(x=1500, y=0, width=37, height=37)
#button.pack(anchor='ne')





#
#
#
#Display animated Gif
#
#
#



# Function to open the menu screen
def open_menu(username):
    login_window.destroy()  # Close login window
   


    menu_window = tk.Tk()
    menu_window.title("Menu")
    menu_window.iconbitmap("C:/Users/temmy/OneDrive/Desktop/CONSEM/dist/IMG_SRC/ICONIC.ico")
    menu_window.geometry("200x200+500+200")




    tk.Button(menu_window, text="Admin", command=lambda: messagebox.showinfo("Admin", "Admin Page")).pack(pady=10)
    tk.Button(menu_window, text="Twitter", command=lambda: messagebox.showinfo("Twitter", "Twitter Page")).pack(pady=10)
    tk.Button(menu_window, text="Messaging", command=lambda: messagebox.showinfo("Messaging", "Messaging Page")).pack(pady=10)

    menu_window.mainloop()

# Main login screen
login_window = tk.Tk()
login_window.attributes('-topmost', 1)
login_window.resizable(False, False)
login_window.title("Login Screen")

login_window.geometry("500x200+500+100")
login_window.iconbitmap("C:/Users/temmy/OneDrive/Desktop/CONSEM/dist/IMG_SRC/ICONIC.ico")

tk.Label(login_window, text="Username").pack(pady=5)
entry_username = tk.Entry(login_window)
entry_username.pack(pady=5)

tk.Label(login_window, text="Password").pack(pady=5)
entry_password = tk.Entry(login_window, show="*")
entry_password.pack(pady=5)

tk.Button(login_window, text="Login", command=validate_login).pack(pady=20)






























# Start the event loop.
window.mainloop()

