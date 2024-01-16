import pandas as pd

def load_questions(filename):
    return pd.read_csv(filename)

def color_text(text:str, color_code:int):
    return f"\033[{color_code}m{text}\033[0m"

def ask_question(row):
    question_type = color_text("Multiple Choice", 34) if len(row['rightanswer']) > 1 else color_text("Single Choice",33)
    print(f"\nQuestion {row['id']} ({question_type}): {row['descriptions']}")  # 蓝色
    print(f"A: {row['A']}")
    print(f"B: {row['B']}")
    if isinstance(row['C'],str):
        print(f"C: {row['C']}")
    if isinstance(row['D'],str):
        print(f"D: {row['D']}")
    if row["wrong_count"]>0:
        print(color_text(f"本题你已经做错了:{row['wrong_count']}次",31))
    answer:str
    if len(row['rightanswer']) > 1:
        answer = input("Enter your answer (e.g. AB/AC/BCD/ABCD): ").strip().upper()
    else:
        answer = input("Enter your answer (e.g. A/B/C/D): ").strip().upper()
    is_correct = answer == row['rightanswer']
    if not is_correct:
        input(color_text(f"Wrong answer. The correct answer is: {row['rightanswer']}", 31))  # 红色
    else:
        print(color_text(("Accepted!"),32))
    return is_correct

def main():
    filename = "questions.csv"
    questions = load_questions(filename)

    ac_cnt=len(questions[questions["wrong_count"] < 0])
    wa_cnt=len(questions[questions["wrong_count"] > 0])
    un_cnt=len(questions[questions["wrong_count"] == 0])
    input(f"目前已经刷了{747-un_cnt}道题\nAC:{ac_cnt}\nWA:{wa_cnt}\n按回车开始继续刷题")

    questions_filtered = questions[questions["wrong_count"]>=0].sample(frac=1)

    for index, row in questions_filtered.iterrows():
        if not ask_question(row):   #Wrong Answer!
            questions.loc[questions['id'] == row['id'], 'wrong_count'] += 1
        else:                       #Accepted!
            questions.loc[questions['id'] == row['id'], 'wrong_count'] = -1
        questions.to_csv(filename, encoding="UTF-8", index=False)

    print("\nResults:")
    for _, row in questions_filtered.iterrows():
        print(f"Question {row['id']}: Wrong answers - {row[questions['id'] == row['id']]['wrong_count'].iloc[0]}")

if __name__ == "__main__":
    main()
