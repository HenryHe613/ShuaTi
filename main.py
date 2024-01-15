import pandas as pd

def load_questions(filename, start_id):
    questions = pd.read_csv(filename)
    questions['id'] = questions['id'].astype(int)
    return questions[questions['id'] >= start_id].sort_values(by='id')

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

def update_csv(questions, filename):
    questions.to_csv(filename, encoding='utf-8', index=False)

def main():
    filename = "questions.csv"  # 替换为你的CSV文件名
    start_id = int(input("Enter the starting question ID: "))
    questions = load_questions(filename, 0)

    for index, row in questions.iterrows():
        if not ask_question(row):
            questions.at[index, 'wrong_count'] += 1
            update_csv(questions, filename)  # 立即更新CSV文件

    print("\nResults:")
    for index, row in questions.iterrows():
        print(f"Question {row['id']}: Wrong answers - {row['wrong_count']}")

if __name__ == "__main__":
    main()
