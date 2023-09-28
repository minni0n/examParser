import pdfplumber
import re
import json

pdf_path = 'your_pdf_file.pdf'
questions = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()

        # Define a regular expression pattern to find questions and answers
        pattern = r'(Question #(\d+)\s+Topic (\d+)(.*?)\n(Correct Answer: ([A-E]+)|Community vote distribution))'
        matches = re.findall(pattern, text, re.DOTALL)

        for match in matches:
            question_number = int(match[1])
            topic_number = int(match[2])
            question_text = match[3].strip()

            # Initialize variables to store the correct answers as a list
            correct_answers = []

            # Extract the answer choices for the current question
            answer_choices_pattern = r'([A-E])\. (.+?)(?=\n[A-E]\.|Correct Answer:|Community vote distribution|$)'
            answer_choices = re.findall(answer_choices_pattern, match[0], re.DOTALL)

            # Create a list of answer choices with text
            answer_choices_list = [choice[1] for choice in answer_choices]

            # Check if "Community vote distribution" is available
            if "Community vote distribution" in question_text:
                # Extract percentages and corresponding answers
                vote_distribution_pattern = r'([A-E]) \((\d+)%\)'
                vote_distribution = re.findall(vote_distribution_pattern, question_text)

                if vote_distribution:
                    # Find the answer(s) with the highest percentage(s)
                    max_percentage = -1
                    max_percentage_answers = []

                    for answer, percentage in vote_distribution:
                        percentage = int(percentage)

                        if percentage > max_percentage:
                            max_percentage = percentage
                            max_percentage_answers = [answer]
                        elif percentage == max_percentage:
                            max_percentage_answers.append(answer)

                    correct_answers = max_percentage_answers
            else:
                # Split multiple correct answers by their capital letters and remove "Correct Answer:"
                correct_answer = match[4] if match[4] else match[5]
                correct_answers = list(correct_answer.replace("Correct Answer: ", ""))

            # Create a dictionary to represent the question
            question_data = {
                "question_number": question_number,
                "topic_number": topic_number,
                "question_text": question_text,
                "answer_choices": answer_choices_list,
                "correct_answers": correct_answers
            }

            # Append the question to the list
            questions.append(question_data)

# Save the test data to a JSON file
with open('test_data.json', 'w') as f:
    json.dump(questions, f, indent=4)
