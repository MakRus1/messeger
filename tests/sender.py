import requests

name = input('name: ')
data = {'name': name}
requests.post('http://127.0.0.1:5000/sendname', json=data)


while True:
    text = input()
    data = {'name': name, 'text': text}
    requests.post('http://127.0.0.1:5000/send', json=data)
