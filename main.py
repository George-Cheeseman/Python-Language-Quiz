import tkinter as tk
from tkinter import messagebox
import pandas as pd
import random
from PIL import Image
from PIL import ImageTk


class QuizApp:
    def __init__(self, root, accent_colour="#008EFE"):

        # Configuring the root window
        self.root = root
        self.root.title("Language Quiz App")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.accent_colour = accent_colour

        self.selection_window()

    def selection_window(self):
        self.language = None
        self.category = None

        # Dictionary of the languages and the file path to the flag image
        self.languages = {
            "German": ImageTk.PhotoImage(
                Image.open("img/flag_germany.jpg").resize((100, 67))
            ),
            "French": ImageTk.PhotoImage(
                Image.open("img/flag_france.jpg").resize((100, 67))
            ),
            "Spanish": ImageTk.PhotoImage(
                Image.open("img/flag_spain.jpg").resize((100, 67))
            ),            
        }

        # Dictionary of the categories and the file path to the CSV file
        self.categories = {
            "Animals": pd.read_csv("data/animals.csv"),
            "Food & Drink": pd.read_csv("data/food_drink.csv"),
            "Colours": pd.read_csv("data/colours.csv"),
            "Numbers": pd.read_csv("data/numbers.csv"),
            "Hobbies": pd.read_csv("data/hobbies.csv"),
        }

        main_heading = tk.Label(
            root, text="LANGUAGES EXAM PRACTICE", font=("Bebas Neue", 32)
        )
        main_heading.pack(pady=20)

        self.selection_frame = tk.Frame(root)
        self.selection_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Language selection buttons
        self.quiz_language_label = tk.Label(
            self.selection_frame,
            text="Select Quiz Language:",
            font=("Helvetica Neue LT", 16),
        )
        self.quiz_language_label.pack(pady=5)

        self.flag_frame = tk.Frame(self.selection_frame)

        self.german_button = tk.Button(
            self.flag_frame,
            image=self.languages["German"],
            command=lambda: self.select_language("German"),
            borderwidth=0,
            relief=tk.FLAT,
        )
        self.french_button = tk.Button(
            self.flag_frame,
            image=self.languages["French"],
            command=lambda: self.select_language("French"),
            borderwidth=0,
            relief=tk.FLAT,
        )
        self.spanish_button = tk.Button(
            self.flag_frame,
            image=self.languages["Spanish"],
            command=lambda: self.select_language("Spanish"),
            borderwidth=0,
            relief=tk.FLAT,
        )

        self.flag_frame.columnconfigure(0, weight=1)
        self.flag_frame.columnconfigure(1, weight=1)
        self.flag_frame.columnconfigure(2, weight=1)
        self.flag_frame.rowconfigure(0, weight=1)

        self.german_button.grid(row=0, column=0, padx=10, pady=10)
        self.french_button.grid(row=0, column=1, padx=10, pady=10)
        self.spanish_button.grid(row=0, column=2, padx=10, pady=10)

        self.flag_frame.pack(pady=5)

        self.selected_language = tk.Label(
            self.selection_frame,
            text="Select Quiz Language: None",
            font=("Helvetica Neue LT", 12),
        )
        self.selected_language.pack(pady=5)

        # Category selection dropdown
        self.category_label = tk.Label(
            self.selection_frame,
            text="Select Category:",
            font=("Helvetica Neue LT", 16),
        )
        self.category_label.pack(pady=(25, 5))

        self.selected_category = tk.StringVar()
        self.selected_category.set(list(self.categories.keys())[0])
        self.category_dropdown = tk.OptionMenu(
            self.selection_frame,
            self.selected_category,
            *self.categories.keys(),
        )
        self.category_dropdown.pack(pady=5)

        # Start and exit buttons
        self.start_button = tk.Button(
            self.selection_frame,
            text="Start Quiz",
            command=lambda: self.start_quiz(),
            bg=self.accent_colour,
            fg="#fff",
            font=("Helvetica Neue LT", 12),
            relief=tk.FLAT,
        )
        self.start_button.pack(pady=20, side=tk.RIGHT)

        self.exit_button = tk.Button(
            self.selection_frame,
            text="Exit",
            command=root.quit,
            bg=self.accent_colour,
            fg="#fff",
            font=("Helvetica Neue LT", 12),
            relief=tk.FLAT,
        )
        self.exit_button.pack(pady=20, side=tk.LEFT)

        self.exeter_logo = ImageTk.PhotoImage(
            Image.open("img/exeter_college.png").resize((250, 100))
        )
        self.logo_label = tk.Label(root, image=self.exeter_logo)
        self.logo_label.place(relx=0.99, rely=0.99, anchor=tk.SE)

    # Stores the selected language and updates the label
    def select_language(self, language):
        self.language = language
        self.selected_language.config(
            text=f"Selected Quiz Language: {self.language}"
        )

    # Returns the selected category
    def get_category(self):
        return self.selected_category.get()

    # Creates the quiz window and widgets
    def start_quiz(self):
        if not self.language:
            messagebox.showerror("Error", "Please select a language")
            return

        self.score = 0
        self.question_index = 0
        self.questions = self.generate_questions()
        self.selected_answer = None
        self.incorrect_answers = []

        self.quiz_window = tk.Toplevel(self.root)
        self.quiz_window.title("Language Quiz")
        self.quiz_window.geometry("600x400")
        self.quiz_window.resizable(False, False)

        self.quiz_frame = tk.Frame(self.quiz_window)
        self.quiz_frame.pack(expand=True)

        self.question_label = tk.Label(
            self.quiz_frame,
            text="",
            wraplength=500,
            font=("Helvetica Neue", 16),
        )
        self.question_label.pack(pady=20)

        self.option_buttons = []

        for i in range(4):
            btn = tk.Button(
                self.quiz_frame,
                text="",
                command=lambda i=i: self.select_answer(i),
                bg="#CCCCCC",
                fg="#303030",
                font=("Helvetica Neue", 12),
                relief=tk.FLAT,
                width=20,
            )
            btn.pack(pady=10)
            self.option_buttons.append(btn)

        self.next_button = tk.Button(
            self.quiz_frame,
            text="Next",
            command=self.next_question,
            bg=self.accent_colour,
            fg="#FFFFFF",
            font=("Helvetica Neue", 12),
            relief=tk.FLAT,
        )
        self.next_button.pack(pady=20)

        self.load_question()

    # Returns a 2D array of random questions and answers from the category and language selected
    def generate_questions(self):
        category = self.get_category()
        language = self.language

        questions = []
        used_indices = set()

        while len(questions) < 10:
            random_index = random.randint(
                0, len(self.categories[category]) - 1
            )
            if random_index not in used_indices:
                used_indices.add(random_index)
                question = self.categories[category]["English"].iloc[
                    random_index
                ]
                answer = self.categories[category][language].iloc[random_index]
                questions.append((question, answer))

        return questions

    # Configures the quiz window to display the next question
    def load_question(self):
        english_word = self.questions[self.question_index][0]
        quiz_word = self.questions[self.question_index][1]
        category = self.get_category()

        options = [quiz_word] + random.sample(
            [
                word
                for word in self.categories[category][self.language]
                if word != quiz_word
            ],
            3,
        )
        random.shuffle(options)

        self.question_label.config(
            text=f'What is "{english_word}" in {self.language}?'
        )

        for i in range(4):
            self.option_buttons[i].config(text=options[i])
            for btn in self.option_buttons:
                btn.config(bg="#CCCCCC", fg="#303030")

    # Configures the button colours and assigns the selected answer to class variable
    def select_answer(self, i):
        selected_button = i

        self.selected_answer = self.option_buttons[selected_button]["text"]

        for btn in self.option_buttons:
            btn.config(bg="#CCCCCC", fg="#303030")

        self.option_buttons[i].config(bg=self.accent_colour, fg="#FFFFFF")

    # Checks if the answer is correct and loads the next question
    def next_question(self):

        if self.selected_answer == self.questions[self.question_index][1]:
            self.score += 1
        else:
            self.incorrect_answers.append(
                (
                    self.questions[self.question_index][0],
                    self.questions[self.question_index][1],
                    self.selected_answer,
                )
            )

        if self.question_index < len(self.questions) - 1:
            self.question_index += 1
            self.selected_answer = None
            self.load_question()
        else:
            self.quiz_window.destroy()
            self.show_result()

    # Displays the user's score and any incorrect answers
    def show_result(self):
        result = f"Your score is {self.score}/10\n"

        if self.incorrect_answers:
            result += "\nIncorrect Answers:\n\n"
            for (
                question,
                correct_answer,
                given_answer,
            ) in self.incorrect_answers:
                result += f"Question: {question} - Answer: {correct_answer} - Your Guess: {given_answer}\n\n"

        messagebox.showinfo("Quiz Complete", result)
        self.quiz_window.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()