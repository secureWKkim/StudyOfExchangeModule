from slacker import Slacker
from trading1.pusher.base_pusher import Pusher
import configparser


class PushSlack(Pusher):
    def __init__(self):
        """config.ini 파일로부터 토큰값을 읽어 들여 Slacker 객체를 생성"""
        config = configparser.ConfigParser()
        config.read('conf/config.ini')
        token = config['SLACK']['token']
        self.slack = Slacker(token)

    def send_message(self, thread="#general", message=None):
        self.slack.chat.post_message(thread, message)
