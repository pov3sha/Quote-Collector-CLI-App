import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import requests
import re

def fetch_quotes():
    try:
        url = 'https://www.goodreads.com/quotes'
        response = requests.get(url)

        if response.status_code == 200:
            html = response.text
            pattern = r'<span class="text" itemprop="text">(.+?)</span>.*?<small class="author" itemprop="author">(.+?)</small>'
            matches = re.findall(pattern, html, re.DOTALL)

            if not matches:
                quote_text.set("No quotes found!")
            else:
                global all_quotes
                all_quotes = matches
                display_quotes(matches)
        else:
            quote_text.set(f"Failed to connect. Status code: {response.status_code}")
    except Exception as e:
        quote_text.set(f"Error: {e}")

def display_quotes(quotes):
    text = "\n\n".join([f'"{q}"\n— {a}' for q, a in quotes])
    quote_text.set(text)

def search_author():
    if not all_quotes:
        messagebox.showinfo("Info", "No quotes loaded yet. Click 'Get Quotes' first.")
        return
    
    author = simpledialog.askstring("Search Author", "Enter author name:").strip().lower()
    if not author:
        return

    found = [(q, a) for q, a in all_quotes if author in a.lower()]
    if found:
        display_quotes(found)
        save = messagebox.askyesno("Save Quotes", f"Save {len(found)} quotes by {author.title()} to file?")
        if save:
            with open("quotes.txt", "w") as f:
                for q, a in found:
                    f.write(f'"{q}" — {a}\n')
            messagebox.showinfo("Saved", "Quotes saved to quotes.txt")
    else:
        quote_text.set(f"No quotes found for author: {author.title()}")

# App Window
app = tk.Tk()
app.title("Quote Collector")
app.geometry("800x600")
app.configure(bg="#2c2f33")

style = ttk.Style(app)
style.theme_use('clam')
style.configure("TButton", font=("Segoe UI", 12), padding=10, background="#7289da", foreground="white")
style.map("TButton", background=[("active", "#5b6eae")])

# Buttons
button_frame = tk.Frame(app, bg="#2c2f33")
button_frame.pack(pady=20)

ttk.Button(button_frame, text="Get Quotes", command=fetch_quotes).pack(side="left", padx=10)
ttk.Button(button_frame, text="Search by Author", command=search_author).pack(side="left", padx=10)

# Scrollable Text Area
text_frame = tk.Frame(app, bg="#2c2f33")
text_frame.pack(padx=20, pady=10, fill="both", expand=True)

scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side="right", fill="y")

quote_text = tk.StringVar()
quote_display = tk.Label(
    text_frame,
    textvariable=quote_text,
    wraplength=760,
    justify="left",
    font=("Segoe UI", 12),
    bg="#23272a",
    fg="#ffffff",
    anchor="nw"
)
quote_display.pack(fill="both", expand=True)
quote_display.config(padx=20, pady=20)
quote_display.bind("<Configure>", lambda e: quote_display.config(wraplength=e.width - 40))

scrollbar.config(command=lambda *args: quote_display.yview(*args))

# Data storage
all_quotes = []

app.mainloop()
