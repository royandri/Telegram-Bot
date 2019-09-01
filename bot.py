import requests
import re
from bottle import (
    run, post, response, request as bottle_request
)

BOT_URL = 'https://api.telegram.org/bot_TOKEN_/'
DOG_URL = 'https://random.dog/woof.json'
CAT_URL = 'http://aws.random.cat/meow'


# =================================Get Image Function==============================

def get_url(image):
    if(image == "dog"):
        contents = requests.get(DOG_URL).json()
        url = contents['url']

    elif(image == "cat"):
        contents = requests.get(CAT_URL).json()
        url = contents['file']

    return url


def get_umage_url(image):
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''

    while file_extension not in allowed_extension:
        url = get_url(image)
        file_extension = re.search("([^.]*)$", url).group(1).lower()

    return url


def response_image(image):
    url = get_umage_url(image)

    return url

# =================================/Get Image Function==============================


def greeting():
    message = "Selamat datang di BotMagang, berikut adalah menu yang dapat digunakan: \n1. /greeting \n2. /dog \n3. /cat"

    return message


def response_new_user(data):
    first_name = data['message']['new_chat_participant']['first_name']

    if "last_name" in data['message']['new_chat_participant']:
        last_name = data['message']['new_chat_participant']['last_name']

    else:
        last_name = " "

    return "Selamat datang" + " " + first_name + " " + last_name


def response_user_left(data):
    first_name = data['message']['left_chat_participant']['first_name']

    if "last_name" in data['message']['left_chat_participant']:
        last_name = data['message']['left_chat_participant']['last_name']

    else:
        last_name = " "

    return "Selamat tinggal" + " " + first_name + " " + last_name


def get_chat_id(data):
    chat_id = data['message']['chat']['id']

    return chat_id


def get_response(text, data):
    response = ""

    if(text != ""):
        if(text == "/greeting"):
            response = greeting()

        elif(text == "/dog"):
            response = response_image("dog")

        elif(text == "/cat"):
            response = response_image("cat")

        else:
            response = "Menu tidak tersedia !" + "\n\n" + greeting()

    else:
        if "new_chat_participant" in data['message']:
            response = response_new_user(data)

        elif "left_chat_participant" in data['message']:
            response = response_user_left(data)

        else:
            response = ""

    return response


def get_message(data):
    if "text" in data['message']:
        message_text = data['message']['text']

    else:
        message_text = ""

    return message_text


def send_message(prepared_data):
    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=prepared_data)


def change_text_message(text, data):

    return get_response(text, data)


def prepare_data_for_answer(data):
    answer = change_text_message(get_message(data), data)
    json_data = {
        'chat_id': get_chat_id(data),
        'text': answer
    }

    return json_data


@post('/')
def main():
    data = bottle_request.json
    answer_data = prepare_data_for_answer(data)
    send_message(answer_data)

    # print(data)
    return response


if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)
