import json

# Load the JSON data
with open('quiz_data.json', 'r') as file:
    quiz_data = json.load(file)

# Initialize variables
question_number = 0
score = 0

# Function to display a question
def display_question(question):
    print(f"Question {question['question_number']}:\n{question['question_text']}")
    for i, choice in enumerate(question['answer_choices'], start=1):
        print(f"{i}. {choice}")

# Function to check if the answer is correct
def check_answer(question, selected_answers):
    correct_answers = set(question['correct_answers'])
    selected_answers = set(selected_answers)
    return correct_answers == selected_answers

# Main quiz loop
while question_number < len(quiz_data):
    current_question = quiz_data[question_number]
    display_question(current_question)

    selected_answers = []
    while True:
        user_input = input("Select answer(s) (comma-separated, e.g., '1,2'): ")
        try:
            selected_indices = [int(index) for index in user_input.split(',')]
            if all(1 <= index <= len(current_question['answer_choices']) for index in selected_indices):
                selected_answers = [current_question['answer_choices'][index - 1] for index in selected_indices]
                break
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter valid numbers separated by commas.")

    if check_answer(current_question, selected_answers):
        print("Correct!\n")
        score += 1
    else:
        correct_choices = ', '.join(current_question['correct_answers'])
        print(f"Wrong. The correct answer(s) are: {correct_choices}\n")

    question_number += 1

print(f"Quiz complete! Your score is: {score}/{len(quiz_data)}")
