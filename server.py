import time
from datetime import datetime, timezone
from flask import Flask, request, Response
import requests
from bs4 import BeautifulSoup as BS

app = Flask(__name__)

messages = [
    {'name': 'Olezhka-bot_Telezhki', 'time': time.time(), 'text': 'Привет! Напиши /help для получения информации'},
]
users = ['Olezhka-bot_Telezhki']


@app.route("/sendname", methods=['POST'])
def sendname():
    name = request.json.get('name')
    if not (name and isinstance(name, str)):
        return Response(status=400)
    users.append(name)
    return Response(status=200)


@app.route("/names")
def names_view():
    try:
        after = float(request.args['after'])
    except:
        return Response(status=400)


@app.route("/send", methods=['POST'])
def send():
    name = request.json.get('name')
    text = request.json.get('text')
    if not name or not isinstance(name, str) or \
            not text or not isinstance(text, str):
        return Response(status=400)
    message = {'name': name, 'time': time.time(), 'text': text}
    messages.append(message)
    if text[0] == "/":
        if text=='/help':
            message = {'name': 'Olezhka-bot_Telezhki',
                      'time': time.time(),
                      'text': '/time - текущее время \n'
                              '/weather - погода'}
            messages.append(message)
        if text=='/time':
            message = {'name': 'Olezhka-bot_Telezhki',
                       'time': time.time(),
                       'text': datetime.now().strftime('%H:%M:%S %d/%m/%Y')}
            messages.append(message)
        if text=='/weather':
            r = requests.get('https://sinoptik.ua/погода-выборг')
            html = BS(r.content, 'html.parser')

            for el in html.select('#content'):
                t_min = el.select('.temperature .min')[0].text
                t_max = el.select('.temperature .max')[0].text
                description = el.select('.wDescription .description')[0].text
                weather = 'Готово! Текущая погода: \n' + t_min + ', ' + t_max + '\n' + description
            message = {'name': 'Olezhka-bot_Telezhki',
                       'time': time.time(),
                       'text': weather}
            messages.append(message)

    return Response(status=200)


def filter_by_key(elements, key, threshold):
    filtered_elements = []

    for element in elements:
        if element[key] > threshold:
            filtered_elements.append(element)

    return filtered_elements


@app.route("/messages")
def messages_view():
    try:
        after = float(request.args['after'])
    except:
        return Response(status=400)

    filtered = filter_by_key(messages, key='time', threshold=after)
    return {'messages': filtered}


@app.route("/")
def hello():
    return "Hello, World! <a href='/status'>Статус</a>"


@app.route("/status")
def status():
    return {
        'status': True,
        'name': 'Telezhka',
        'time': datetime.now().strftime('%H:%M:%S %Y/%m/%d'),
        'users_quantity': len(users),
        'message_quantity': len(messages),
    }


app.run()
