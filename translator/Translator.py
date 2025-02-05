import tkinter as tk
from tkinter import messagebox
import asyncio
import aiohttp
import os
import ctypes

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Translator")
        self.root.configure(bg='black')
        self.root.geometry("450x600")  # Set the window size to 450x600
        self.history = []

        self.input_label = tk.Label(root, text="Word:", fg='white', bg='black')
        self.input_label.grid(row=0, column=0, padx=10, pady=10)

        self.input_entry = tk.Entry(root, width=30)
        self.input_entry.grid(row=0, column=1, padx=10, pady=10)
        self.input_entry.bind("<Return>", self.translate_word)  # Bind Enter key to translate_word

        self.translate_button = tk.Button(root, text="Translate", command=self.translate_word)
        self.translate_button.grid(row=0, column=2, padx=10, pady=10)

        self.save_button = tk.Button(root, text="Save to File", command=self.save_to_file)
        self.save_button.grid(row=0, column=3, padx=10, pady=10)

        self.output_label = tk.Label(root, text="", fg='white', bg='black')
        self.output_label.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        self.history_listbox = tk.Listbox(root, width=50, height=10, bg='black', fg='white')
        self.history_listbox.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

        self.set_keyboard_language_to_english()

    async def translate_word_async(self, english_word):
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=ru&dt=t&q={english_word}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                result = await response.json()
                return result[0][0][0]

    def translate_word(self, event=None):
        english_word = self.input_entry.get()
        if english_word:
            translated_word = asyncio.run(self.translate_word_async(english_word))
            print(translated_word)
            self.output_label.config(text=f"{english_word} - {translated_word}")
            self.history.append(f"{english_word} - {translated_word}")
            self.history_listbox.insert(tk.END, f"{english_word} - {translated_word}")
            self.input_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a word to translate.")

    def save_to_file(self):
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads", "translations.txt")
        with open(downloads_path, "a", encoding="utf-8") as file:  # Open the file in append mode
            for entry in self.history:
                file.write(entry + "\n")
        messagebox.showinfo("Save Successful", f"Translations saved to {downloads_path}")

    def set_keyboard_language_to_english(self):
        user32 = ctypes.WinDLL('user32', use_last_error=True)
        user32.LoadKeyboardLayoutW('00000409', 1)

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()
