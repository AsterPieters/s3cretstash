#s3cretstash.py
import tkinter as tk
from tkinter import ttk, messagebox

from modules.encryption import encrypt_secret, decrypt_secret
from modules.authentication import authenticate_user

def login():
    master_secret = master_secret_textbox.get()
    if not master_secret:
        messagebox.showwarning("Login Failed", "Please provide your master secret.")
        return

    else:
        if authenticate_user(master_secret):
            pass
        else:
            messagebox.showerror("Login Failed", "Wrong master secret.")
            return


    try:
        print(master_secret)
    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed: {e}")



def login_screen():
    # Login textbox
    ttk.Label(root, text="Master Secret:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    master_secret_textbox = ttk.Entry(root, show="*", width=40)
    master_secret_textbox.grid(row=0, column=1, padx=10, pady=5)

    # Login button
    encrypt_button = ttk.Button(root, text="Login", command=login)
    encrypt_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

# Create the main application window
root = tk.Tk()
root.title("S3cretstash")

login_screen()

# Start the main loop
root.mainloop()
