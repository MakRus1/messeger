from datetime import datetime

import requests
from PyQt5 import QtWidgets, QtCore
import clientui


class MyWindow(QtWidgets.QMainWindow, clientui.Ui_mainWindow):
    def __init__(self, server_url):
        super().__init__()
        self.setupUi(self)

        self.server_url = server_url

        self.Send.pressed.connect(self.send_message)

        self.after = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.load_messages)
        self.timer.start(1000)

    def pretty_message(self, message):
        dt = datetime.fromtimestamp(message['time'])
        dt_str = dt.strftime('%H:%M:%S')
        self.Messages.append(message['name'] + ' ' + dt_str)
        self.Messages.append(message['text'])
        self.Messages.append('')
        self.Messages.repaint()

    def load_messages(self):
        try:
            data = requests.get(self.server_url + '/messages',
                                params={'after': self.after}).json()
        except:
            return

        for message in data['messages']:
            self.pretty_message(message)
            self.after = message['time']

    def send_message(self):
        name = self.Name.text()
        text = self.text.toPlainText()

        data = {'name': name, 'text': text}
        try:
            response = requests.post(self.server_url + '/send',
                                     json=data)
        except:
            self.Messages.append('Сервер недоступен. Попробуйте позже.\n')
            self.Messages.repaint()
            return

        if response.status_code != 200:
            self.Messages.append('Неправильные данные\n')
            self.Messages.repaint()
            return

        self.text.setText('')
        self.text.repaint()


app = QtWidgets.QApplication([])
window = MyWindow('https://cd96e17fc5e0.ngrok.io')
window.show()
app.exec_()
