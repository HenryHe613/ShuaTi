import os
import platform
import pandas as pd

def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def load_questions(filename):
    return pd.read_csv(filename)

def color_text(text:str, color_code:int):
    return f"\033[{color_code}m{text}\033[0m"

def ask_question(row):
    question_type = color_text("Multiple Choice", 34) if len(row['rightanswer']) > 1 else color_text("Single Choice",33)
    print(f"\nQuestion {row['id']} ({question_type}): {row['descriptions']}")
    print(f"A: {row['A']}")
    print(f"B: {row['B']}")
    CDexist = isinstance(row['C'],str) and isinstance(row['D'],str)
    if CDexist:
        print(f"C: {row['C']}")
        print(f"D: {row['D']}")
    if row["wrong_count"]>0:
        print(color_text(f"You have already done this question wrong: {row['wrong_count']}次",31))
    answer:str
    if len(row['rightanswer']) > 1:
        answer = input("Enter your answer (e.g. AB/AC/BCD/ABCD): ").strip().upper()
    elif(CDexist):
        answer = input("Enter your answer (e.g. A/B/C/D): ").strip().upper()
    else:
        answer = input("Enter your answer (e.g. A/B): ").strip().upper()
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
    mode=input(f"目前已经刷了{747-un_cnt}道题\nAC:{ac_cnt}\nWA:{wa_cnt}\n输入1开始顺序刷题,输入2随机刷题")

    print("Do you want to clear terminal before each questions? (yes/no) ")
    ifclear_str=input().upper()
    ifclear=True if ifclear_str=="Y" or ifclear=="YES" else False

    if(mode=='1'):
        start_id = int(input("Enter the starting question ID: "))
        questions_filtered = questions[questions['id'] >= start_id].sort_values(by='id')
    elif(mode=='2'):
        questions_filtered = questions[questions["wrong_count"]>=0].sample(frac=1)
    else:
        input("Invalid input. PRESS ENTER to exit. ")
        return

    for index, row in questions_filtered.iterrows():
        if not ask_question(row):   #Wrong Answer!
            questions.loc[questions['id'] == row['id'], 'wrong_count'] += 1
        else:                       #Accepted!
            questions.loc[questions['id'] == row['id'], 'wrong_count'] = -1
        questions.to_csv(filename, encoding="UTF-8-sig", index=False)
        if(ifclear):
            clear_screen()

    print("\nResults:")
    for _, row in questions_filtered.iterrows():
        print(f"Question {row['id']}: Wrong answers - {row[questions['id'] == row['id']]['wrong_count'].iloc[0]}")

if __name__ == "__main__":
    main()
