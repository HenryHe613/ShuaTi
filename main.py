import pandas as pd

def load_questions(filename):
    return pd.read_csv(filename)

def color_text(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def ask_question(row):
    question_type = color_text("Multiple Choice", 31) if len(row['rightanswer']) > 1 else "Single Choice"
    print(f"\nQuestion {row['id']} ({question_type}): {row['descriptions']}")
    print(f"A: {row['A']}")
    print(f"B: {row['B']}")
    print(f"C: {row['C']}")
    print(f"D: {row['D']}")
    answer = input("Enter your answer (e.g., A/B/C/D or AB/AC/BCD): ").strip().upper()
    is_correct = answer == row['rightanswer']
    if not is_correct:
        input(color_text(f"Wrong answer. The correct answer is: {row['rightanswer']}", 31))  # 红色
    return is_correct

def main():
    filename = "questions.csv"
    questions = load_questions(filename)
    start_id = int(input("Enter the starting question ID: "))
    questions_filtered = questions[questions['id'] >= start_id].sort_values(by='id')

    for index, row in questions_filtered.iterrows():
        if not ask_question(row):
            questions.loc[questions['id'] == row['id'], 'wrong_count'] += 1
            questions.to_csv(filename, encoding="UTF-8", index=False) 

    print("\nResults:")
    for _, row in questions_filtered.iterrows():
        print(f"Question {row['id']}: Wrong answers - {row[questions['id'] == row['id']]['wrong_count'].iloc[0]}")

if __name__ == "__main__":
    main()
