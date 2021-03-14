#-*- coding: utf-8 -*-
from telegram.ext import Updater
from telegram.ext import CommandHandler
#import ebest  creon 변경
import threading
from queue import Queue
import time
#import pythoncom
import requests
from bs4 import BeautifulSoup
from enum import Enum, auto

class WorkList(Enum):
    LOGIN = auto()
    PRICE = auto()
    AUTOTEST = auto()

class Worker(threading.Thread):
    def __init__(self, workList, workerQueue):
        super().__init__()
        self.workList = workList
        self.workerQueue = workerQueue
        #self.__finance = ebest.Finance() creon


    def run(self):
        while True:
            #lock?
            time.sleep(3)
            if self.workerQueue.empty():
                continue

            work = self.workerQueue.get()

            if work[1] == self.workList.LOGIN:
                work[2].bot.send_message(work[0], "로그인 성공")

                """
                if self.__finance.login() == self.__finance.SUCCESS:
                    self.__finance.kospiLoad()
                    self.__finance.kosdaqLoad()
                    work[2].bot.send_message(work[0], "로그인 성공")
                else:
                    work[2].bot.send_message(work[0], "로그인 실패")
                    """
                continue
            elif work[1] == self.workList.PRICE:
                work[2].bot.send_message(work[0], work[3] + " 가격은 " + "xxxx 원 입니다." )
                """
                price = self.__finance.getPrice(work[3])
                if price == self.__finance.ERROR:
                    work[2].bot.send_message(work[0], work[3] + " 조회 실패")
                else:
                    work[2].bot.send_message(work[0], work[3] + " 가격은 " + price + "원 입니다." )
                """
                continue



class WuBot(threading.Thread):
    def __init__(self):
#        with open("./wubot.key") as f:
#            lines = f.readlines()
#            token = lines[0].strip()
#test
        super().__init__()
        token=""

        self.__updater = Updater(token=token, use_context=True)
        self.__dispatcher = self.__updater.dispatcher

        start_handler = CommandHandler('start', self.startWUBU)
        self.__dispatcher.add_handler(start_handler)

        help_handler = CommandHandler('help', self.helpWUBU)
        self.__dispatcher.add_handler(help_handler)

        login_handler = CommandHandler('login', self.loginCreon)
        self.__dispatcher.add_handler(login_handler)

        price_handler = CommandHandler('price', self.getPrice)
        self.__dispatcher.add_handler(price_handler)

        self.workList = WorkList
        self.workerQueue = Queue()

    def startWUBU(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="hello world!")


    def helpWUBU(self, update, context):
        id = update.effective_chat.id
        text = "안녕하세요. WUBUBOT 입니다.\n"
        context.bot.send_message(id, text)


# 사용자별 로그인처리 필요
# 외부에서 사용하기 위해서 나름의 보안 처리 필요...
# User id == 등록 계정 일때만 로그인?
    def loginCreon(self, update, context):
        id = update.effective_chat.id
        self.workerQueue.put((id, self.workList.LOGIN, context))
        context.bot.send_message(id, "로그인 시도 중")


    def getPrice(self, update, context):
        id = update.effective_chat.id
        text = update.effective_message.text
        priceCode = text.split(' ')
        self.workerQueue.put((id, self.workList.PRICE, context, priceCode[1]), context)
        context.bot.send_message(id, priceCode[1] + " 가격 조회 중")


    def run(self):
        worker = Worker(self.workList, self.workerQueue)
        worker.start()
        self.__updater.start_polling()


if __name__ == "__main__":
    wubot = WuBot()
    wubot.start()
