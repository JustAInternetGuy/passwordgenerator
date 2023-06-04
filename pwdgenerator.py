import random
import string
import customtkinter as ctk
from customtkinter import CTkToplevel
from customtkinter import filedialog
import zxcvbn
from PIL import Image


# Constants
MAX_LENGTH = 64
MIN_LENGTH = 8

# GUI variables
password_display = None
strength_label = None
strength_canvas = None
checkbox_var = None
window_closed = None
bold_font = ("Arial", 26, "bold")
generic_font = ("Arial", 21)
small_font = ("Arial", 12, "italic")
medium_font = ("Arial", 15)
pil_image = Image.open("paste.png")
copy_icon = ctk.CTkImage(light_image=pil_image)

# Popup_Open Variables
popup_open = None

# Password strength text
strength_text = None

# Others
window_closed_value = False




def update_strength_indicator(strength):
    strength_colors = {
        0: "red",
        1: "orange",
        2: "yellow",
        3: "green",
        4: "blue"
    }
    strength_texts = {
        0: 'Very weak',
        1: 'Weak',
        2: 'Medium',
        3: 'Strong',
        4: 'Very strong'
    }
    strength_canvas.configure(bg=strength_colors[strength])
    strength_label.configure(text=strength_texts[strength])
    

def generate_password_and_update_display_field(length, password_display):
    if not popup_open and window_closed_value != True:
        length = character_length_of_password_field.get()
        generated_password = generate_password(length)
        password_display.configure(state="normal")
        password_display.delete(0, ctk.END)
        password_display.insert(0, generated_password)
        password_display.configure(state="disabled")
        raw_result = zxcvbn.zxcvbn(generated_password)
        strength = raw_result["score"]
        info_label.pack_forget()
        strength_label.pack(pady=5)
        strength_canvas.pack()
        save_button.pack(pady=10)
        window.geometry("450x400")
        update_strength_indicator(strength)


def copy_password(window, password_display):
    password = password_display.get()
    if password != "":
        window.clipboard_clear()
        window.clipboard_append(password)


class CTkMessageBox(ctk.CTk):
    class _NoAnimationButton(ctk.CTkButton):
        def _clicked(self, event):
            self.invoke()

    def __init__(self, parent, title, message):
        ctk.CTk.__init__(self, parent)
        self.iconbitmap("icon.ico")
        self.title(title)
        self.resizable(False, False)

        ctk.CTkLabel(self, text=message).pack(padx=10, pady=10)
        self._NoAnimationButton(self, text="OK", command=self.on_ok).pack(padx=10, pady=10)

    def on_ok(self):
        global popup_open
        popup_open = False
        self.destroy()


def show_popup():
    global popup_open
    if not popup_open:
        popup = CTkMessageBox(None, "Error", f"Password must be a number between {MIN_LENGTH} and {MAX_LENGTH}")
        popup_open = True
        popup.protocol("WM_DELETE_WINDOW", lambda: print(""))
        popup.mainloop()


def save_password(password_display):
    password = password_display.get()
    # Prompt user to choose a file location and filename
    if password != "":
        filename = filedialog.asksaveasfilename(initialfile="password.txt", title="Save Password",
                                                filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))

        # If the user cancels the save dialog, don't save the password
        if not filename:
            return

        # Get the password from the password display field

        # Write the password to the file
        with open(filename, 'w') as f:
            f.write(password)


def generate_password(length):
    global popup_open
    if length.isdigit() and MIN_LENGTH - 1 < int(length) <= MAX_LENGTH:
        password_length = int(length)
    else:
        show_popup()
        return ""

    # Generate a string of random characters of `length` `password_length`
    password = "".join(random.choice(string.ascii_letters + string.digits + string.punctuation)
                       for _ in range(password_length))

    # Shuffle the characters
    password = "".join(random.sample(password, len(password)))

    return password


def show_password():
    if checkbox_var.get():
        password_display.configure(show="")
    


def toggle_password_display():
    if checkbox_var.get():
        password_display.configure(show="")
    else:
        password_display.configure(show="*")


def on_window_closed(password_display, password_length_combobox):
    global window_closed_value
    window_closed_value = True
    password_display.destroy()
    password_length_combobox.destroy()
    window.quit()
    

window = ctk.CTk()
window.bind('<Control-c>', lambda event: copy_password(window, password_display))
window.bind("<Return>", lambda event: generate_password_and_update_display_field(None, password_display))
window.bind("<Control-s>", lambda event: save_password(password_display))
window.protocol("WM_DELETE_WINDOW", window_closed)  # Specify the function to call when the window is closed
window.iconbitmap("icon.ico")
window.title("Password Generator")
window.resizable(False, False)
window.geometry("450x400")  # Specify the function to call when the window is closed

label = ctk.CTkLabel(window, font=bold_font, text="Password Generator")
label.pack(pady=10)

character_limit_label = ctk.CTkLabel(window, font=generic_font, text="Character Limit:")
character_limit_label.pack()

options_of_character_limit = ("8", "16", "32", "64")
string_var_for_char_limit = ctk.StringVar(value=options_of_character_limit[0])

character_length_of_password_field = ctk.CTkComboBox(window, font=generic_font, width=250,
                                                     values=options_of_character_limit, dropdown_font=medium_font)
character_length_of_password_field.pack(pady=10)

run_button = ctk.CTkButton(window, border_width=0, border_color="white", width=250, font=generic_font,
                           text="Generate Password",
                           command=lambda: generate_password_and_update_display_field(
                               character_length_of_password_field.get(), password_display))
run_button.pack(pady=10)

password_label = ctk.CTkLabel(window, font=generic_font, text="Password:")
password_label.pack()

password_display = ctk.CTkEntry(window, font=generic_font, width=250, show="*")
password_display.configure(state="disabled")
password_display.pack(pady=10)

checkbox_var = ctk.BooleanVar()

checkbox_label = ctk.CTkCheckBox(window, border_color="white", border_width=3, variable=checkbox_var, text="",
                                 command=lambda: toggle_password_display())

# Move checkbox to the end of password display field
checkbox_label.place(x=360, y=225)

copy_button = ctk.CTkButton(window, width=30, height=30, image=copy_icon, text="", fg_color="#292929",
                            hover_color="#404040", border_color="white", border_width=2,
                            command=lambda: copy_password(window, password_display))
copy_button.place(x=53, y=222)

save_button = ctk.CTkButton(window, border_width=0, border_color="white", width=250, font=generic_font,
                            text="Save Password",
                            command=lambda: save_password(password_display))
save_button.pack(pady=15)

info_label = ctk.CTkLabel(window, font=small_font,
                          text=f"For information on how to use the program,"
                               f" \n please refer to the README.txt file \n"
                               f" located in the directory of your installation.")
info_label.pack()

strength_label = ctk.CTkLabel(window,  font=generic_font, text="temp")

strength_canvas = ctk.CTkCanvas(window, width=300, height=20)

window.mainloop()