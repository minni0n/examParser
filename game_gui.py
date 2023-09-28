import tkinter as tk
from tkinter import messagebox
import json

# Load the JSON data
with open('quiz_data.json', 'r') as file:
    quiz_data = json.load(file)

# Initialize variables
question_number = 0
score = 0

def display_question():
    global question_number
    question_label.config(text=quiz_data[question_number]['question_text'])

def check_answer():
    global question_number, score
    question_number += 1
    if question_number < len(quiz_data):
        display_question()
    else:
        messagebox.showinfo("Quiz Complete", f"Your score is: {score}/{len(quiz_data)}")
        window.quit()

# Create the main window
window = tk.Tk()
window.title("Quiz Game")

# Create widgets
question_label = tk.Label(window, text="", wraplength=400, padx=20, pady=10)
question_label.pack()

next_button = tk.Button(window, text="Next", command=check_answer, bg="blue", fg="white")
next_button.pack()

# Start the quiz
display_question()

# Run the GUI main loop
window.mainloop()
