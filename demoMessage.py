from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk, ImageDraw
import textwrap
import os


class MessagingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Messaging App")
        self.root.state("zoomed")  # Open in fullscreen mode
        self.light_mode = True  # Theme state
        self.bg_light = "#FFF9E6"
        self.bg_dark = "#2C2C2C"
        self.text_light = "#000000"
        self.text_dark = "#FFFFFF"
        self.primary_light = "#FFC629"
        self.primary_dark = "#FFD369"
        self.secondary_light = "#C9C9C9"
        self.secondary_dark = "#404040"
        self.update_theme_colors()

        # Data and state
        self.messages_data = {}
        self.current_friend = None

        # Load icons
        self.profile_icon = self.load_image("IMG_SRC/profile_icon.png", (30, 30))
        self.send_icon = self.load_image("IMG_SRC/send_icon.png", (45, 45))
        self.theme_icon = self.load_image("IMG_SRC/dark_mode.png", (30, 30))
        self.emoji_icon = self.load_image("IMG_SRC/emoji_icon.png", (50, 50))
        self.attachment_icon = self.load_image("IMG_SRC/attachment_icon.png", (50, 50))

        # Setup UI components
        self.setup_ui()

    def update_theme_colors(self):
        """Update theme colors dynamically based on light_mode state."""
        self.bg_color = self.bg_light if self.light_mode else self.bg_dark
        self.text_color = self.text_light if self.light_mode else self.text_dark
        self.primary_color = self.primary_light if self.light_mode else self.primary_dark
        self.secondary_color = self.secondary_light if self.light_mode else self.secondary_dark

    def load_image(self, path, size):
        try:
            image = Image.open(path).resize(size)
            return ImageTk.PhotoImage(image)
        except FileNotFoundError:
            print(f"Error: {path} not found.")
            return None

    def setup_ui(self):
        """Reinitialize the UI for theme toggling."""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Friends list frame
        self.setup_friends_frame()

        # Chat area frame
        self.setup_chat_frame()

        # Input area
        self.setup_input_frame()

    def setup_friends_frame(self):
        self.friends_frame = tk.Frame(self.root, bg=self.primary_color, width=300, height=600)
        self.friends_frame.pack_propagate(False)
        self.friends_frame.pack(side="left", fill="y")

        friends_label = tk.Label(
            self.friends_frame,
            text="C-Messages",
            bg=self.primary_color,
            font=("Segoe UI", 18, "bold"),
            fg=self.bg_color,
        )
        friends_label.pack(pady=20)

        # Add friends dynamically
        friends_list = ["Jose", "Gavin", "Emmett"]
        for friend in friends_list:
            button = tk.Button(
                self.friends_frame,
                text=f"  {friend}",
                image=self.profile_icon,
                compound="left",
                font=("Segoe UI", 14),
                bg="#FFD369",
                fg="#000000",
                activebackground="#FFC629",
                activeforeground="#FFF9E6",
                relief="flat",
                bd=0,
                padx=10,
                command=lambda f=friend: self.select_friend(f),
            )
            button.pack(fill="x", pady=10, padx=20)
            self.messages_data[friend] = []

        # Add a dark mode toggle button
        theme_button = tk.Button(
            self.friends_frame,
            image=self.theme_icon,
            bg=self.primary_color,
            activebackground=self.primary_color,
            command=self.toggle_theme,
            relief="flat",
            bd=0,
        )
        theme_button.pack(pady=10)

    def toggle_theme(self):
        """Toggle between light and dark modes."""
        self.light_mode = not self.light_mode
        self.update_theme_colors()
        self.update_theme_for_existing_ui()

    def update_theme_for_existing_ui(self):
        """Update theme colors for the existing UI components."""
        self.friends_frame.config(bg=self.primary_color)
        for widget in self.friends_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg=self.primary_color, activebackground=self.primary_color)
            elif isinstance(widget, tk.Label):
                widget.config(bg=self.primary_color, fg=self.bg_color)

        self.chat_frame.config(bg=self.bg_color)
        self.header_frame.config(bg=self.primary_color)
        self.header_label.config(bg=self.primary_color, fg="#FFFFFF")
        self.chat_area_frame.config(bg=self.bg_color)
        self.chat_log_canvas.config(bg=self.bg_color)
        self.chat_log_inner.config(bg=self.bg_color)
        self.input_frame.config(bg=self.bg_color)
        self.EntryBox.config(bg=self.secondary_color, fg=self.text_color)

        # Update message bubbles
        for widget in self.chat_log_inner.winfo_children():
            if isinstance(widget, tk.Frame):
                for bubble in widget.winfo_children():
                    if isinstance(bubble, tk.Label):
                        sent_by_user = widget.pack_info()["anchor"] == "e"
                        bubble_text = bubble.cget("text")
                        bubble.config(
                            bg=self.bg_color,
                            fg=self.text_color,
                            image=self.create_dynamic_bubble(bubble_text, sent_by_user),
                        )

    def setup_chat_frame(self):
        self.chat_frame = tk.Frame(self.root, bg=self.bg_color)
        self.chat_frame.pack(side="right", fill="both", expand=True)

        # Header
        self.header_frame = tk.Frame(self.chat_frame, bg=self.primary_color, height=50)
        self.header_frame.pack(fill="x")
        self.header_label = tk.Label(
            self.header_frame,
            text="Welcome!",
            bg=self.primary_color,
            font=("Segoe UI", 16, "bold"),
            fg="#FFFFFF",
        )
        self.header_label.pack(pady=10)

        # Chat area
        self.chat_area_frame = tk.Frame(self.chat_frame, bg=self.bg_color)
        self.chat_area_frame.pack(fill="both", expand=True, padx=10, pady=(10, 0))

        # Chat log
        self.chat_log_canvas = tk.Canvas(self.chat_area_frame, bg=self.bg_color, highlightthickness=0)
        self.chat_log_inner = tk.Frame(self.chat_log_canvas, bg=self.bg_color)
        self.chat_scroll = ttk.Scrollbar(
            self.chat_area_frame, orient="vertical", command=self.chat_log_canvas.yview
        )
        self.chat_log_canvas.configure(yscrollcommand=self.chat_scroll.set)

        # Attach chat log inner frame to canvas
        self.chat_log_window = self.chat_log_canvas.create_window(
            (0, 0), window=self.chat_log_inner, anchor="nw"
        )
        self.chat_log_inner.bind(
            "<Configure>",
            lambda e: self.chat_log_canvas.configure(
                scrollregion=self.chat_log_canvas.bbox("all")
            ),
        )

        self.chat_log_canvas.bind(
            "<Configure>",
            lambda e: self.chat_log_canvas.itemconfig(
                self.chat_log_window, width=e.width
            ),
        )

        self.chat_log_canvas.pack(side="left", fill="both", expand=True)
        self.chat_scroll.pack(side="right", fill="y")

    def setup_input_frame(self):
        self.input_frame = tk.Frame(self.chat_frame, bg=self.bg_color, height=50)
        self.input_frame.pack(fill="x", side="bottom", padx=10, pady=10)

        # Input box
        self.EntryBox = tk.Text(
            self.input_frame,
            font=("Segoe UI", 13),
            width=60,
            height=3,
            wrap="word",
            bg=self.secondary_color,
            fg=self.text_color,
            bd=2,
        )
        self.EntryBox.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=5)
        self.EntryBox.insert("1.0", "Type your message here...")

        # Bind Enter key to send message
        self.EntryBox.bind("<FocusIn>", lambda event: self.clear_placeholder())
        self.EntryBox.bind("<FocusOut>", lambda event: self.add_placeholder())
        self.EntryBox.bind("<Return>", lambda event: (self.send_message(), "break"))

        # Emoji picker button
        emoji_button = tk.Button(
            self.input_frame,
            image=self.emoji_icon,
            bg=self.bg_color,
            relief="flat",
            command=self.pick_emoji,
        )
        emoji_button.pack(side="right", padx=(10, 0))

        # Attachment button
        attachment_button = tk.Button(
            self.input_frame,
            image=self.attachment_icon,
            bg=self.bg_color,
            relief="flat",
            command=self.attach_file,
        )
        attachment_button.pack(side="right", padx=(10, 0))

        # Send button
        self.SendButton = tk.Button(
            self.input_frame,
            image=self.send_icon,
            bg=self.bg_color,
            activebackground=self.primary_color,
            relief="flat",
            command=self.send_message,
        )
        self.SendButton.pack(side="right", padx=(10, 0), pady=5)

    def clear_placeholder(self):
        if self.EntryBox.get("1.0", tk.END).strip() == "Type your message here...":
            self.EntryBox.delete("1.0", tk.END)

    def add_placeholder(self):
        if not self.EntryBox.get("1.0", tk.END).strip():
            self.EntryBox.insert("1.0", "Type your message here...")

    def create_dynamic_bubble(self, text, sent_by_user=True):
        wrapped_text = textwrap.fill(text, width=50)
        lines = len(wrapped_text.split("\n"))

        text_width = max(len(max(wrapped_text.split("\n"), key=len)), 5)
        bubble_width = max(5, text_width * 10 + 20)
        bubble_height = max(55, lines * 20 + 20)

        bubble_color = self.primary_color if sent_by_user else self.secondary_color

        image = Image.new("RGBA", (bubble_width, bubble_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle(
            [(0, 0), (bubble_width, bubble_height)],
            radius=20,
            fill=bubble_color,
        )
        return ImageTk.PhotoImage(image)

    def pick_emoji(self):
        """Open a pop-up emoji picker window."""
        emoji_window = tk.Toplevel(self.root)
        emoji_window.title("Pick an Emoji")
        emoji_window.geometry("300x200")
        emoji_window.resizable(False, False)
        emoji_window.transient(self.root)  # Keep it on top of the main window

        emojis = [
            "😊", "😂", "😍", "😭", "😒",
            "👍", "🙏", "❤️", "🎉", "🔥",
            "🤔", "😎", "🥳", "😢", "💪",
        ]

        def insert_emoji(emoji):
            """Insert selected emoji into the EntryBox without triggering placeholder logic."""
            # Temporarily disable the placeholder logic
            self.EntryBox.unbind("<FocusOut>")
            self.EntryBox.insert("insert", emoji)
            # Re-enable the placeholder logic
            self.EntryBox.bind("<FocusOut>", lambda event: self.add_placeholder())
            emoji_window.destroy()  # Close the emoji picker

        # Create a grid of emoji buttons
        for idx, emoji in enumerate(emojis):
            button = tk.Button(
                emoji_window,
                text=emoji,
                font=("Segoe UI", 16),
                command=lambda e=emoji: insert_emoji(e),
                relief="flat",
                bg=self.secondary_color,
                activebackground=self.primary_color,
            )
            button.grid(row=idx // 5, column=idx % 5, padx=10, pady=10)

        # Center the emoji picker relative to the main window
        self.center_window(emoji_window)


    def center_window(self, window):
        """Center a window relative to the main application."""
        window.update_idletasks()
        main_width = self.root.winfo_width()
        main_height = self.root.winfo_height()
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()

        win_width = window.winfo_width()
        win_height = window.winfo_height()

        pos_x = main_x + (main_width // 2) - (win_width // 2)
        pos_y = main_y + (main_height // 2) - (win_height // 2)
        window.geometry(f"+{pos_x}+{pos_y}")

    def attach_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            file_ext = os.path.splitext(file_path)[-1].lower()
            if file_ext in [".png", ".jpg", ".jpeg", ".gif"]:
                self.display_image(file_path)
            else:
                file_name = os.path.basename(file_path)
                self.display_message(f"Sent a file: {file_name}", sent_by_user=True)

    def send_message(self):
        message = self.EntryBox.get("1.0", "end-1c").strip()
        self.EntryBox.delete("1.0", tk.END)
        if message and self.current_friend:
            self.messages_data[self.current_friend].append((message, True))
            self.display_message(message, sent_by_user=True)
            response = "This is a reply."
            self.messages_data[self.current_friend].append((response, False))
            self.display_message(response, sent_by_user=False)

    def select_friend(self, friend):
        self.current_friend = friend
        self.header_label.config(text=self.current_friend)
        self.load_messages()

    def display_message(self, text, sent_by_user=True):
        bubble_frame = tk.Frame(self.chat_log_inner, bg=self.bg_color)
        bubble_frame.pack(fill="x", pady=5, padx=10, anchor="e" if sent_by_user else "w")

        bubble_image = self.create_dynamic_bubble(text, sent_by_user=sent_by_user)
        bubble = tk.Label(
            bubble_frame,
            image=bubble_image,
            text=textwrap.fill(text, 40),
            font=("Segoe UI", 13),
            bg=self.bg_color,
            fg=self.text_color,
            padx=10,
            pady=10,
            compound="center",
            bd=0,
        )
        bubble.image = bubble_image
        bubble.pack(anchor="e" if sent_by_user else "w")
        self.chat_log_canvas.update_idletasks()
        self.chat_log_canvas.yview_moveto(1.0)

    def display_image(self, file_path):
        image = Image.open(file_path)
        image.thumbnail((300, 300))
        img = ImageTk.PhotoImage(image)

        bubble_frame = tk.Frame(self.chat_log_inner, bg=self.bg_color)
        bubble_frame.pack(fill="x", pady=5, padx=10, anchor="e")

        label = tk.Label(bubble_frame, image=img, bg=self.bg_color)
        label.image = img  # Keep a reference to avoid garbage collection
        label.pack(anchor="e")

    def load_messages(self):
        if self.current_friend in self.messages_data:
            for widget in self.chat_log_inner.winfo_children():
                widget.destroy()
            for msg, sent_by_user in self.messages_data[self.current_friend]:
                if isinstance(msg, str):
                    self.display_message(msg, sent_by_user=sent_by_user)
                elif isinstance(msg, ImageTk.PhotoImage):
                    self.display_image(msg)


# Run the app
# Run the app only if this file is executed directly, not when imported
if __name__ == "__main__":
    root = tk.Tk()
    app = MessagingApp(root)
    root.mainloop()
