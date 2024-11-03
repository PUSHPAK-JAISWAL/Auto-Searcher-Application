import tkinter as tk
from tkinter import ttk, messagebox
import requests
import time
import random
import subprocess
import pyautogui

# Wikipedia API endpoint for random topic
WIKIPEDIA_RANDOM_API = "https://en.wikipedia.org/api/rest_v1/page/random/summary"

# Function to check internet connectivity
def check_internet():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

# Function to fetch a random search topic from Wikipedia
def get_random_topic():
    try:
        response = requests.get(WIKIPEDIA_RANDOM_API)
        if response.status_code == 200:
            data = response.json()
            return data.get('title', "Random Topic")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get random topic: {e}")
    return "Random Topic"

# Open the selected browser
def open_browser(browser_choice):
    if browser_choice == "Chrome":
        browser_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Update with actual path if different
    elif browser_choice == "Edge":
        browser_path = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"  # Update with actual path if different
    elif browser_choice == "Firefox":
        browser_path = "C:/Program Files/Mozilla Firefox/firefox.exe"  # Update with actual path if different
    else:
        messagebox.showerror("Browser Error", "Unsupported browser selection.")
        return

    subprocess.Popen([browser_path])
    time.sleep(2)  # Give some time for the browser to open

# Type search query into the browser's search bar
def type_search_query(query):
    if typing_active:  # Only type if active
        pyautogui.typewrite(query, interval=random.uniform(0.1, 0.3))  # Type with a slight delay
        pyautogui.press('enter')

# Main function to start search based on user input
def start_search():
    global typing_active
    typing_active = True  # Set flag to indicate typing is active

    if not check_internet():
        messagebox.showerror("Connection Error", "No internet connection. Please connect to the internet and try again.")
        typing_active = False  # Mark typing as inactive
        return

    selected_browser = browser_choice.get()
    if not selected_browser:
        messagebox.showerror("Browser Error", "Please select a browser.")
        typing_active = False  # Mark typing as inactive
        return

    try:
        num_searches = int(search_count.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number of searches.")
        typing_active = False  # Mark typing as inactive
        return

    search_topic = search_topic_input.get() if not randomize_var.get() else None

    if num_searches <= 0 or (not search_topic and not randomize_var.get()):
        messagebox.showerror("Input Error", "Please fill in all required fields.")
        typing_active = False  # Mark typing as inactive
        return

    open_browser(selected_browser)

    # Perform searches without closing the tab
    for _ in range(num_searches):
        if not typing_active:  # Check if typing is still active
            break

        query = search_topic if search_topic else get_random_topic()
        time.sleep(2)  # Wait a moment before typing the query

        # Type the query into the browser's search bar
        type_search_query(query)

        # Wait for a human-like interval to simulate reading time
        time.sleep(random.uniform(8, 12))  # Random delay to simulate reading time

        # To simulate the user preparing for the next search
        if randomize_var.get():
            search_topic_input.delete(0, tk.END)

    typing_active = False  # Mark typing as inactive after completion

# Function to toggle input field based on randomize checkbox
def toggle_search_topic_input():
    if randomize_var.get():
        search_topic_input.config(state='disabled')
    else:
        search_topic_input.config(state='normal')

# Initialize the Tkinter window with styling
app = tk.Tk()
app.title("Auto Searcher")
app.geometry("450x450")
app.configure(bg="#f0f4f8")

# Styling elements
header_font = ("Arial", 16, "bold")
label_font = ("Arial", 12)
button_font = ("Arial", 12, "bold")

# Header Label
header_label = tk.Label(app, text="Auto Searcher", font=header_font, bg="#f0f4f8", fg="#333")
header_label.pack(pady=20)

# Browser selection dropdown
browser_choice_label = tk.Label(app, text="Select Browser:", font=label_font, bg="#f0f4f8")
browser_choice_label.pack(pady=5)
browser_choice = ttk.Combobox(app, values=["Chrome", "Edge", "Firefox"], state="readonly")
browser_choice.pack(pady=5)

# Number of searches input
search_count_label = tk.Label(app, text="Number of Searches:", font=label_font, bg="#f0f4f8")
search_count_label.pack(pady=5)
search_count = tk.Entry(app, font=("Arial", 12), width=20)
search_count.pack(pady=5)

# Randomize checkbox and search topic input
randomize_var = tk.BooleanVar()
randomize_checkbox = tk.Checkbutton(app, text="Randomize Search Topics", variable=randomize_var, command=toggle_search_topic_input, bg="#f0f4f8", font=label_font)
randomize_checkbox.pack(pady=5)

search_topic_label = tk.Label(app, text="Search Topic:", font=label_font, bg="#f0f4f8")
search_topic_label.pack(pady=5)
search_topic_input = tk.Entry(app, font=("Arial", 12), width=30)
search_topic_input.pack(pady=5)

# Start search button
start_button = tk.Button(app, text="Start Search", font=button_font, bg="#007acc", fg="white", relief='raised', bd=3, command=start_search)
start_button.pack(pady=30)  # Adjusting padding to give more space above and below

app.mainloop()
