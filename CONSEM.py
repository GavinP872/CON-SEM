import tkinter as tk
from tkinter import messagebox, PhotoImage
from PIL import ImageTk, Image
from datetime import datetime
from chat_functions import send_message, start_receiving, create_client
from demoMessage import MessagingApp  # Import the MessagingApp class

# Usernames and Passwords
admin_USERNAME = ["gavin", "jose", "benedict", "emmett", " "]
admin_PASSWORD = ["gavin1", "jose1", "benedict1", "emmett1", " "]

# Validate login
def validate_login():
    username = entry_username.get()
    password = entry_password.get()

    if username in admin_USERNAME and password in admin_PASSWORD:
        user_index = admin_USERNAME.index(username)
        if admin_PASSWORD[user_index] == password:
            open_menu(username)
        else:
            messagebox.showerror("Error", "Invalid username or password")
    else:
        messagebox.showerror("Error", "Invalid username or password")

# Function to open the main application menu after successful login
def open_menu(username):
    login_window.destroy()
    window.deiconify()


# Main application window setup (fullscreen)
window = tk.Tk()  
window.title("CON-SEM v1.0.0.0") 
window.iconbitmap("IMG_SRC/ICONIC.ico") 
window.attributes('-fullscreen', True)  
window.withdraw()  # Hide the window initially until login is successful

# Function to handle application close when close button is pressed
def handle_button_press(event):
    window.destroy()  # Close the main window

# Function to open the MessagingApp when admin button is pressed
def handle_admin_button_press(event):
    admin_window = tk.Toplevel(window)
    admin_window.title("Admin Messaging App")
    admin_window.state("zoomed")

    # Initialize the MessagingApp inside the new window
    app = MessagingApp(admin_window)

def open_chat_window():
    # Create a new chat window
    chat_window = tk.Toplevel(window)
    chat_window.title("Chat")
    chat_window.geometry("400x500")

    # Initialize a new client for this chat window
    client = create_client()

    # Chat display
    chat_display = tk.Text(chat_window, state="disabled", wrap="word")
    chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Input message box
    message_entry = tk.Entry(chat_window, width=50)
    message_entry.pack(pady=5, padx=10)

    # Function to update chat display with new messages
    def display_message(message):
        chat_display.config(state="normal")
        chat_display.insert(tk.END, f"{message}\n")
        chat_display.config(state="disabled")
        chat_display.see(tk.END)


    # Function to send a message
    def on_send_click():
        message = message_entry.get().strip()
        if message:
            send_message(client, message)  # Send the message via this user's client
            display_message(f"You: {message}")  # Display sent message in chat
            message_entry.delete(0, tk.END)

    # Send button
    send_button = tk.Button(chat_window, text="Send", command=on_send_click)
    send_button.pack(pady=5)

    # Start receiving messages for this user's client
    start_receiving(client, display_message)



    
# Open Twitter window
def handle_twitter_button_press(event):
    twitter_window = tk.Toplevel(window)  # Create a new window for Twitter 
    twitter_window.title("Twitter Consem Main Page")  
    twitter_window.state('zoomed')  
    twitter_window.configure(bg="#f5f8fa") 

    # Placeholder data for tweets and friends list
    tweets = [
        {'user': 'Jose', 'handle': '@jose', 'tweet': 'Hello', 'time': '10m'},
        {'user': 'Emmett', 'handle': '@emmett', 'tweet': 'Hey!', 'time': '20m'},
    ]
    friends = ["Friend1", "Friend2", "Friend3"]  # Example friends list

    # Function for buttons with no features yet
    def placeholder_action():
        messagebox.showinfo("Info", "This feature is not yet implemented!")

    # Function to handle posting a new tweet
    def post_tweet():
        tweet = tweet_entry.get()  # Get the text from the tweet entry
        if tweet.strip():  # Ensure the tweet is not empty
            tweets.insert(0, {  # Insert new tweet at the top of the feed
                'handle': '@currentuser', 
                'tweet': tweet.strip(), 
                'time': 'Now',  
            })
            refresh_feed()  # Refresh the feed to show the new tweet
            tweet_entry.delete(0, tk.END)  # Clear the entry field after tweeting
        else:
            messagebox.showwarning("Warning", "Tweet cannot be empty!")  # Show warning for empty tweets

    # Function to refresh the feed with current tweets
    def refresh_feed():
        for widget in feed_content.winfo_children():  # Clear existing widgets in the feed
            widget.destroy()
        
        for tweet in tweets:  # Loop through the tweets to display them
            tweet_frame = tk.Frame(feed_content, bg="#e8f5fd", pady=5, padx=10)  # Create frame for each tweet
            tweet_frame.pack(fill=tk.X, pady=5)

            avatar_label = tk.Label(tweet_frame, image=avatar_image, bg="#e8f5fd")  # Avatar image for tweet
            avatar_label.pack(side=tk.LEFT, padx=5)

            tweet_info_frame = tk.Frame(tweet_frame, bg="#e8f5fd")  # Frame for tweet details
            tweet_info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Username and handle
            user_label = tk.Label(tweet_info_frame, text=f"{tweet['handle']}", font=("Chirp", 12, "bold"), bg="#e8f5fd")
            user_label.pack(anchor="w")

            # Tweet content
            tweet_text = tk.Label(tweet_info_frame, text=tweet['tweet'], font=("Chirp", 12), bg="#e8f5fd", wraplength=400)
            tweet_text.pack(anchor="w")

            # Time and source of the tweet
            time_label = tk.Label(tweet_info_frame, text=f"·{tweet['time']}", font=("Chirp", 10), bg="#e8f5fd", fg="#657786")
            time_label.pack(anchor="w", pady=(0, 5))

            # Interaction buttons (like, reply, retweet, share)
            interaction_frame = tk.Frame(tweet_info_frame, bg="#e8f5fd")
            interaction_frame.pack(anchor="w", pady=5)
            
            tk.Button(interaction_frame, image=like_icon, bg="#e8f5fd", relief="flat", command=placeholder_action).pack(side=tk.LEFT, padx=5)
            tk.Button(interaction_frame, image=reply_icon, bg="#e8f5fd", relief="flat", command=placeholder_action).pack(side=tk.LEFT, padx=5)
            
    # Load images for avatar and interaction buttons
    global avatar_image, like_icon, reply_icon
    try:
        avatar_image = PhotoImage(file="IMG_SRC/profile_icon.png")
        like_icon = PhotoImage(file="IMG_SRC/like_icon.png")
        reply_icon = PhotoImage(file="IMG_SRC/reply_icon.png")
    except tk.TclError as e:
        messagebox.showerror("Image Load Error", f"Failed to load an image: {e}")

    # Top navigation bar with profile, home, and notification buttons
    top_nav = tk.Frame(twitter_window, bg="#1da1f2", height=60)
    top_nav.pack(fill=tk.X)

    profile_button = tk.Button(top_nav, image=profile_icon, bg="#1da1f2", relief="flat", command=placeholder_action)
    profile_button.pack(side=tk.LEFT, padx=10, pady=5)

    home_button = tk.Button(top_nav, image=home_icon, bg="#1da1f2", relief="flat", command=placeholder_action)
    home_button.pack(side=tk.LEFT, padx=10, pady=5)

    notifications_button = tk.Button(top_nav, image=notifications_icon, bg="#1da1f2", relief="flat", command=placeholder_action)
    notifications_button.pack(side=tk.LEFT, padx=10, pady=5)

    title_label = tk.Label(top_nav, image=title_image, bg="#1da1f2")
    title_label.pack(side=tk.TOP, pady=10)

    # Main content area for feed and friends list
    main_content = tk.Frame(twitter_window, bg="#f5f8fa")
    main_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # Feed area setup
    feed_frame = tk.Frame(main_content, bg="white", width=500, height=650)
    feed_frame.pack_propagate(False)
    feed_frame.pack(side=tk.LEFT, padx=20, pady=10, expand=True)

    # Tweet input section
    tweet_input_frame = tk.Frame(feed_frame, bg="white")
    tweet_input_frame.pack(fill=tk.X, padx=10, pady=10)

    tweet_entry = tk.Entry(tweet_input_frame, font=("Chirp", 12), width=40)
    tweet_entry.pack(side=tk.LEFT, padx=5)

    tweet_button = tk.Button(tweet_input_frame, text="Tweet", bg="#1da1f2", fg="white", font=("Chirp", 12), relief="flat", command=post_tweet)
    tweet_button.pack(side=tk.LEFT)

    # Scrollable area for the feed
    feed_canvas = tk.Canvas(feed_frame, bg="white")
    scrollbar = tk.Scrollbar(feed_frame, orient="vertical", command=feed_canvas.yview)
    scrollable_frame = tk.Frame(feed_canvas, bg="white")

    # Bind scrollable frame to canvas
    scrollable_frame.bind(
        "<Configure>",
        lambda e: feed_canvas.configure(
            scrollregion=feed_canvas.bbox("all")
        )
    )

    feed_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    feed_canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    feed_canvas.pack(side="left", fill="both", expand=True)

    feed_content = scrollable_frame  # Frame to contain tweets

    # Friends list on the right side
    friends_frame = tk.Frame(twitter_window, bg="#8eccf5")
    friends_frame.place(relx=0.8, rely=0.1555, relwidth=0.2, relheight=1.0)

    friends_label = tk.Label(friends_frame, text="Friends List", font=("Chirp", 14), bg="#8eccf5")
    friends_label.pack(anchor="w", pady=5, padx=10)

    # Display friends in the friends list
    for friend in friends:
        friend_button = tk.Button(friends_frame, text=friend, bg="#1da1f2", fg="white", font=("Chirp", 10),
                                  relief="flat", command=lambda f=friend: placeholder_action())
        friend_button.pack(fill=tk.X, padx=10, pady=5)

    refresh_feed()  # Initial feed display

# Load images for main window icons
DesktopImage = ImageTk.PhotoImage(Image.open("IMG_SRC/102237.jpg"))
panel = tk.Label(window, image=DesktopImage)
panel.pack(side="bottom", fill="both", expand="yes")

try:
    twitterIcon = PhotoImage(file="IMG_SRC/TWIT.png")
    chatIcon = PhotoImage(file="IMG_SRC/CHAT.png")
    adminToolIcon = PhotoImage(file="IMG_SRC/TOOL.png")
    xbutton = PhotoImage(file="IMG_SRC/x.png")
    profile_icon = PhotoImage(file="IMG_SRC/profile_icon.png")
    home_icon = PhotoImage(file="IMG_SRC/home_icon.png")
    notifications_icon = PhotoImage(file="IMG_SRC/notifications_icon.png")
    title_image = PhotoImage(file="IMG_SRC/TwConsem_title.png")
except tk.TclError as e:
    messagebox.showerror("Image Load Error", f"Failed to load an image: {e}")

# Twitter button setup
twitter_button = tk.Button(window, text=" ", image=twitterIcon)
twitter_button.bind("<Button-1>", handle_twitter_button_press)
twitter_button.place(x=50, y=50, width=150, height=150)

# Chat button setup
chat_button = tk.Button(window, text=" ", image=chatIcon)
chat_button.bind("<Button-1>", lambda e: open_chat_window())
chat_button.place(x=50, y=250, width=150, height=150)

# Admin tools button setup
admin_button = tk.Button(window, text=" ", image=adminToolIcon)
admin_button.bind("<Button-1>", handle_admin_button_press)
admin_button.place(x=50, y=450, width=150, height=150)

# Close button setup
close_button = tk.Button(window, text=" ", image=xbutton)
close_button.bind("<Button-1>", handle_button_press)
close_button.place(x=1500, y=0, width=37, height=37)

# Main login window setup
login_window = tk.Tk()
login_window.attributes('-topmost', 1)  
login_window.resizable(False, False)  
login_window.title("Login Screen")  

login_window.geometry("500x200+500+100")  # Set size and position of login window
login_window.iconbitmap("IMG_SRC/ICONIC.ico")  # Set icon for login window

# Username input field
tk.Label(login_window, text="Username").pack(pady=5)
entry_username = tk.Entry(login_window)
entry_username.pack(pady=5)

# Password input field
tk.Label(login_window, text="Password").pack(pady=5)
entry_password = tk.Entry(login_window, show="*")  # Use '*' to hide password input
entry_password.pack(pady=5)

# Login button
tk.Button(login_window, text="Login", command=validate_login).pack(pady=20)




# Start the GUI event loop
login_window.mainloop()