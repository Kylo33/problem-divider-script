import pandas as pd
import dataframe_image as dfi
import random
import sys
from PIL import Image

def main():

    if len(sys.argv) != 5:
        print(
            "Syntax: python3 script.py <group member file> <question count> <required version count> <output file path>"
        )
        return 1

    group_members = []
    with open(sys.argv[1]) as group_member_file:
        for line in group_member_file:
            group_members.append(line.strip())

    random.shuffle(group_members)

    question_count = int(sys.argv[2])
    version_count = int(sys.argv[3])

    output_file_path = sys.argv[4]

    questions = {
        question_number: set() for question_number in range(1, question_count + 1)
    }

    group_member_index = 0
    while any([len(questions[question]) < version_count for question in questions]):
        group_member = group_members[group_member_index % len(group_members)]

        open_questions = [
            question
            for question in questions
            if len(questions[question]) < version_count
            and group_member not in questions[question]
        ]
        if open_questions:
            questions[random.choice(open_questions)].add(group_member)

        group_member_index += 1

    assignments = {
        group_member: sorted(
            [str(question) for question in questions if group_member in questions[question]]
        )
        for group_member in group_members
    }

    data_frame = pd.DataFrame.from_dict(
        assignments,
        orient="index"
    )
    data_frame.sort_index(inplace=True) 
    data_frame.fillna("", inplace=True)
    dfi.export(data_frame, output_file_path)
    with Image.open(output_file_path) as image:
        width, height = image.size;
        image.crop((0, 32, width, height)).save(output_file_path)

if __name__ == "__main__":
    main()
