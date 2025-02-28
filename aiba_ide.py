import re
import numba
import tensorflow as tf
import torch
import llvmlite.binding as llvm
import tkinter as tk
from tkinter import scrolledtext, Menu, ttk, filedialog
import cv2
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import transformers
from transformers import GPT2LMHeadModel, GPT2Tokenizer, CLIPProcessor, CLIPModel
from diffusers import StableDiffusionPipeline
import pygments
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
import jedi
import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
import psutil
import torch.distributed as dist
import boto3
from numba import jit
import threading

nltk.download('punkt')
nltk.download('vader_lexicon')

# Configurar suporte total a GPU
torch.backends.cudnn.benchmark = True
torch.backends.cudnn.enabled = True

executor = ThreadPoolExecutor()

class AIBAIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("AIBA IDE")
        self.create_menu()
        self.create_text_area()
        self.create_output_area()
        self.update_monitor()

    def create_menu(self):
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Novo", command=self.new_file)
        file_menu.add_command(label="Abrir", command=self.open_file)
        file_menu.add_command(label="Salvar", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)
        menu_bar.add_cascade(label="Arquivo", menu=file_menu)

    def create_text_area(self):
        self.text_area = scrolledtext.ScrolledText(self.root, width=80, height=20, font=("Courier", 12))
        self.text_area.pack()
        self.text_area.bind("<KeyRelease>", self.syntax_highlight)
        self.text_area.bind("<Tab>", self.autocomplete)

    def create_output_area(self):
        self.run_button = tk.Button(self.root, text="Executar", command=self.run_code_async)
        self.run_button.pack()
        self.debug_button = tk.Button(self.root, text="Depurar", command=self.debug_step_by_step)
        self.debug_button.pack()
        self.monitor_label = tk.Label(self.root, text="Monitoramento: CPU 0% | Memória 0%")
        self.monitor_label.pack()
        self.output_label = tk.Label(self.root, text="Saída:")
        self.output_label.pack()
        self.output_text = scrolledtext.ScrolledText(self.root, width=80, height=10, font=("Courier", 12))
        self.output_text.pack()

    def update_monitor(self):
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        self.monitor_label.config(text=f"CPU: {cpu_usage}% | Memória: {memory_usage}%")
        self.root.after(1000, self.update_monitor)

    def syntax_highlight(self, event=None):
        code = self.text_area.get("1.0", tk.END)
        formatted_code = pygments.highlight(code, PythonLexer(), TkFormatter())
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", formatted_code)

    def autocomplete(self, event):
        code = self.text_area.get("1.0", tk.END)
        script = Interpreter(code, globals())
        completions = script.complete()
        if completions:
            self.text_area.insert(tk.INSERT, completions[0].name)
        return "break"

    def run_code_async(self):
        threading.Thread(target=self.run_code, daemon=True).start()

    def run_code(self):
        code = self.text_area.get("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        try:
            exec(code, globals())
        except Exception as e:
            self.output_text.insert("1.0", f"Erro: {str(e)}\n")

    def debug_step_by_step(self):
        code = self.text_area.get("1.0", tk.END).split("\n")
        for line in code:
            try:
                exec(line, globals())
                self.output_text.insert("end", f"Executado: {line}\n")
                self.root.update()
            except Exception as e:
                self.output_text.insert("end", f"Erro em {line}: {str(e)}\n")
                break

    def new_file(self):
        self.text_area.delete("1.0", tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Arquivos AIBA", "*.aiba"), ("Todos os arquivos", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", file.read())

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".aiba", filetypes=[("Arquivos AIBA", "*.aiba"), ("Todos os arquivos", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get("1.0", tk.END))

if __name__ == "__main__":
    root = tk.Tk()
    ide = AIBAIDE(root)
    root.mainloop()
