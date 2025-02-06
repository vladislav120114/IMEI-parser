import telebot, os, json
from parser import checker

bot_token = "YOUR_TOKEN"

bot = telebot.TeleBot(bot_token)

if not os.path.exists("whitelist.json"):
    whitelist = {}
else:
    with open("whitelist.json", "r") as file:
        whitelist = json.load(file)

token = ""

@bot.message_handler(commands=["start"])
def start_message(message):

    state = check_auth(message)

    if state == "token":
        bot.send_message(message.chat.id, "Введите токен авторизации")

    if state == "imei":
        bot.send_message(message.chat.id, "Введите IMEI утройства")


@bot.message_handler(content_types="text")
def check(message):

    state = check_auth(message)
    id = str(message.chat.id)

    if state == "token":
        response = checker(message.text)
        if response.status_code == 401:
            bot.send_message(message.chat.id, "Некорректный токен авторизцаии")
        else:
            if message.chat.id not in whitelist:
                whitelist[id] = message.text
                with open("whitelist.json", "w") as file:
                    json.dump(whitelist, file)
            bot.send_message(message.chat.id, "Введите IMEI утройства")

    if state == "imei":
        response = checker(whitelist[id], message.text)
        if response.status_code == 422:
            bot.send_message(whitelist[id], "Некорректный IMEI")
            print(response.json())
        else:
            data = response.json()['properties']
            text = ''
            for key, value in data.items():
                line = f'{key}: {value}'
                print(line)
                text += f'{line}\n'
            bot.send_message(message.chat.id, text)


def check_auth(message):
    if str(message.chat.id) not in whitelist:
        return "token"
    else:
        return "imei"


bot.infinity_polling()
