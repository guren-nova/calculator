import tkinter as tk
import webbrowser
from math import sqrt
import re

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("ノヴァの万能電卓")
        self.root.geometry("400x600")
        
        self.result_var = tk.StringVar()
        self.history = []

        self.display = tk.Entry(root, textvariable=self.result_var, font=("Arial", 24), bd=10, relief="sunken", justify="right")
        self.display.grid(row=0, column=0, columnspan=4)

        buttons = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
            ("C", 5, 0), ("√", 5, 1), ("History", 5, 2), ("Exit", 5, 3)
        ]

        for (text, row, col) in buttons:
            button = tk.Button(root, text=text, font=("Arial", 18), width=5, height=2, command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col)

        self.github_button = tk.Button(root, text="GitHub", font=("Arial", 14), fg="blue", command=self.open_github)
        self.github_button.grid(row=6, column=0, columnspan=4)

    def on_button_click(self, text):
        if text == "=":
            try:
                expression = self.result_var.get()
                if self.is_safe_expression(expression):
                    result = self.safe_eval(expression)
                    self.result_var.set(result)
                    self.history.append(f"{expression} = {result}")
                else:
                    self.result_var.set("Error: Unsafe expression")
            except Exception as e:
                self.result_var.set("Error")
        elif text == "C":
            self.result_var.set("")
        elif text == "√":
            try:
                value = float(self.result_var.get())
                self.result_var.set(sqrt(value))
            except Exception as e:
                self.result_var.set("Error")
        elif text == "History":
            self.show_history()
        elif text == "Exit":
            self.root.quit()
        else:
            current_text = self.result_var.get()
            self.result_var.set(current_text + text)

    def is_safe_expression(self, expression):
        allowed_chars = re.match("^[0-9+\-*/().^ ]*$", expression)
        return bool(allowed_chars)

    def safe_eval(self, expression):
        safe_operators = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y if y != 0 else "Error: Division by zero",
            "^": lambda x, y: x ** y
        }
        
        tokens = re.split(r'(\+|\-|\*|/|\^|\(|\)|\.)', expression)
        result = float(tokens[0])

        i = 1
        while i < len(tokens):
            operator = tokens[i]
            if operator in safe_operators:
                num = float(tokens[i + 1])
                result = safe_operators[operator](result, num)
                i += 2
            else:
                i += 1

        return result

    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("履歴")
        history_list = "\n".join(self.history)
        history_label = tk.Label(history_window, text=history_list, font=("Arial", 14), justify="left")
        history_label.pack()

    def open_github(self):
        webbrowser.open("https://github.com/guren-nova")

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
