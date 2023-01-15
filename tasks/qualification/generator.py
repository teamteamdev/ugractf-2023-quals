#!/usr/bin/env python3
import shutil
import sys
import json
import random
import hashlib
import tempfile
import string
import os

salt = "ugractf_salt_lol_kek_rozetkin"
app_home = "/home/rozetkin/ugra_quest_backend"
server_url = "https://qualification.q.2023.ugractf.ru"


def generate_xml(user):
    """
    Generate xml file with questions and answers for given user
    user: user
    """

    random.seed(user)

    xml = {"CommandName": None, "CommandKey": None, "qTotal": None, "questions": None}

    question_template = """
    <string-array name="question_{QUESTION_NUM}">
        <item name="question_{QUESTION_NUM}">{QUESTION}</item>
        <item name="{QUESTION_NUM}_1a{ANSWER_1_IS_RIGHT}">{ANSWER_1}</item>
        <item name="{QUESTION_NUM}_2a{ANSWER_2_IS_RIGHT}">{ANSWER_2}</item>
        <item name="{QUESTION_NUM}_3a{ANSWER_3_IS_RIGHT}">{ANSWER_3}</item>
        <item name="{QUESTION_NUM}_right_ans">{ANSWER_RIGHT_NUM}</item>
    </string-array>
    """

    with open('questions.json', 'r') as f:
        all_questions = json.load(f)
    
    q_total = 15
    all_questions = all_questions['questions']
    # print(len(all_questions))

    # random pick 15 question from questions array
    questions = []
    for _ in range(q_total):
        questions.append(all_questions.pop(all_questions.index(random.choice(all_questions))))
    
    
    # pick random right answer for each question
    for question in questions:
        question['right_index'] = random.randint(1, 3)
        # pick 3 random answers from question['answers']
        try:
            question['answers'] = random.sample(question['answers'], 3)
        except ValueError:
            # print(question['answers'])
            raise
    
    # generate xml file
    questions_xml = ""
    for i, question in enumerate(questions):
        questions_xml += question_template.format(
            QUESTION_NUM=i+1,
            QUESTION=question['question'],
            ANSWER_1=question['answers'][0],
            ANSWER_1_IS_RIGHT=1 if question['right_index'] == 1 else 0,
            ANSWER_2=question['answers'][1],
            ANSWER_2_IS_RIGHT=1 if question['right_index'] == 2 else 0,
            ANSWER_3=question['answers'][2],
            ANSWER_3_IS_RIGHT=1 if question['right_index'] == 3 else 0,
            ANSWER_RIGHT_NUM=question['right_index']
        )
    
    # generate state
    state = ""
    for question in questions:
        state += str(question['right_index'])
    
    # generate key from user by hashing with salt 

    key = hashlib.sha256((user + salt).encode()).hexdigest()


    xml["CommandKey"]   = key
    xml["CommandName"]  = user
    xml["qTotal"]       = q_total
    xml["questions"]    = questions_xml
    

    # print(state)
    return key, state, xml

def generate_app(user, workdir):
    """
    #Build apk from sources with generated questions, which saved in xml file 
    Unpack apk, replace xml file, repack apk and sign it
    """

    task = os.getcwd()

    with tempfile.TemporaryDirectory(dir=workdir) as tempdir:
        shutil.copytree(task, os.path.join(tempdir, "task"))
        os.chdir(os.path.join(tempdir, "task"))

        # generate xml file with questions
        key, state, xml = generate_xml(user)

        # unpack apk
        os.system(f"java -jar apktool.jar d app-release.apk -f 1>/dev/null")

        # replace xml file
        with open(f'app-release/res/values/integers.xml', 'r') as f:
            integers = f.read()
        
        integers = integers.replace("9999", str(xml["qTotal"]))

        with open(f'app-release/res/values/integers.xml', 'w') as f:
            f.write(integers)

        with open(f'app-release/res/values/strings.xml', 'r') as f:
            strings = f.read()
        
        strings = strings.replace("{USER}", xml["CommandName"])
        strings = strings.replace("{KEY}", xml["CommandKey"])
        # print(xml["CommandKey"], xml["CommandName"])

        with open(f'app-release/res/values/strings.xml', 'w') as f:
            f.write(strings)

        with open(f'app-release/res/values/arrays.xml', 'w') as f:
            f.write("<resources>\n" + xml["questions"] + "\n</resources>")
        
        # replace server url

        with open(f'app-release/smali/com/rozetkin/ugraquest/QuestionFragment.smali', 'r') as f:
            smali = f.read()
        
        smali = smali.replace("http://10.0.2.2", server_url)

        with open(f'app-release/smali/com/rozetkin/ugraquest/QuestionFragment.smali', 'w') as f:
            f.write(smali)


        
        # arrays = arrays.replace("{QUESTIONS}", xml["questions"])

            
        
        # repack apk via aaapt2
        os.system(f"java -jar apktool.jar b app-release -f  --use-aapt2 -o app.apk 1>/dev/null")

        # sign apk via uber-apk-signer
        os.system(f"java -jar uber-apk-signer.jar --apks app.apk --out . --ks ./rozetkin_ugra.jks --ksAlias key0 --ksKeyPass 'ugractf_keys' --ksPass 'ugractf_keys' --debug 1>/dev/null")

        os.rename(
            'app-aligned-signed.apk',
            os.path.join(workdir, 'attachments', 'Qualification.apk')
        )

        return key, state


leetspeak_dict = {
    "a": ["4"],
    "b": ["8"],
    "e": ["3"],
    "g": ["6", "9"],
    "i": ["1"],
    "l": ["1", "7"],
    "o": ["0"],
    "s": ["5"],
    "t": ["7"],
    "z": ["2"]
}

def gen_flag(key):
    random.seed(key)
    flag_prefix = "ugra_"
    flag_body = "android_reverse_not_so_easy_but_it_is_cool"
    salt_length = 8

    # replace up to random 10 letters with leetspeak
    for _ in range(10):
        letter_index = random.randint(0, len(flag_body) - 1)
        letter = flag_body[letter_index]
        if letter in leetspeak_dict:
            flag_body = flag_body[:letter_index] + random.choice(leetspeak_dict[letter]) + flag_body[letter_index + 1:]
        
    flag_hash = ''.join(random.choice('0123456789abcdef') for _ in range(salt_length))
    flag = flag_prefix + flag_body + '_' + flag_hash
    return flag




def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir", file=sys.stderr)
        sys.exit(1)
    
    user_id = sys.argv[1]
    workdir = sys.argv[2]
    os.makedirs(os.path.join(workdir, "attachments"), exist_ok=True)
    
    key, state = generate_app(user_id, workdir)

    json.dump({
        "flags": [gen_flag(key)]
    }, sys.stdout)

# ./generate.py <task name> <user_uuid> <folder_for_attachments>
if __name__ == "__main__":
    generate()
