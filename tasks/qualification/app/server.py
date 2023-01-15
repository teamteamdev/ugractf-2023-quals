#flask backend for android app

from flask import Flask, jsonify
import json
import random
import base64
import hashlib
import string

# Pillow
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

salt = "ugractf_salt_lol_kek_rozetkin"

   

def generate_flag_certificate(username, flag, failed=True):
    """Generate certificate with flag
    
    Хедер - Федеральное государственное бюджетное учреждение высшего образования «Исследовательский институт изучения информационных искусств (ФГБУ ВО ИИИИИ)»
    
    Текст - Данное удостоверение подтверждает, что участник {user} {не} прошёл профессиональную переподготовку по курсу «Организационные системы информационной безопасности предприятия».

    Проверочный код - {flag}

    
    Подпись - Председатель комиссии по выдаче дипломов и сертификатов ФГБУ ВО ИИИИИ Розеткин Александр Владимирович

    Печать - shtamp.png

    """
   
    # load template
    img = Image.open("certificate.png")


    width, height = img.size

    # draw username, colorize #1ba0ee
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("OpenSans-Light.ttf", 80)
    draw.text((width//2-400, height//3 +100), username, (27, 161, 226), font=font, align="center")

    # draw flag, colorize red, bold

    font = ImageFont.truetype("OpenSans-Light.ttf", 30)
    draw.text((570, height-400), flag, (255, 0, 0), font=font, align="center", stroke_width=2, stroke_fill=(0, 0, 0))
    
    # draw line under "успешно" or "неуспешно" text, black
    x = 70
    y = 950
    if not failed:
        draw.line((x, y, x + 130, y), fill=(0, 0, 0), width=3)
    else:
        x+= 150
        draw.line((x, y, x + 170, y), fill=(0, 0, 0), width=3)
    

    # convert to base64 as png
    save_buffer = BytesIO()
    img.save(save_buffer, format="PNG")
    img_str = base64.b64encode(save_buffer.getvalue()).decode()
    return img_str


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
            print(question['answers'])
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
    

    print(state)
    return key, state, xml


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



def make_app(state_dir):
    app = Flask(__name__)

    @app.route('/check/<string:key>/<string:username>/<string:state>', methods=['GET'])
    def check(key, username, state):
        """This function for validating the key and state
        key: key of the user
        username: username of the user
        state: answers for the questions. string of numbers

        If state for given key is valid - gives flag
        """
        
        real_key, real_state, _ = generate_xml(username)
        if real_key != key:
            return jsonify({"status": "bad", "picture": generate_flag_certificate(username, hashlib.sha256(key.encode() + b'ugra').hexdigest()[:38])})
        
        if real_state == state:
            return jsonify({"status": "ok", "picture": generate_flag_certificate(username, gen_flag(real_key), failed=False)})
        
        return jsonify({"status": "bad", "picture": generate_flag_certificate(username, hashlib.sha256(key.encode()+ b'ugra').hexdigest()[:38])})

    return app



if __name__ == "__main__":
    app = make_app("state")
    app.run(host='0.0.0.0', port=80)
