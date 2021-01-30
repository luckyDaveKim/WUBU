from telegram.ext import Updater
from telegram.ext import CommandHandler
import ebest
import threading
from queue import Queue
import time
import pythoncom
import requests
from bs4 import BeautifulSoup


with open("./wubot.key") as f:
    lines = f.readlines()
    token = lines[0].strip()

LOGIN=1
PRICE=2
workerQueue = Queue()

def startWUBU(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="hello world!")


def helpWUBU(update, context):
    id = update.effective_chat.id
    text = "안녕하세요. WUBUBOT 입니다.\n" \
           "현재 지원하는 기능은 \n" \
           " /login \n" \
           " /price [종목 코드] or [종목 명]  (login 필수)\n" \
           "입니다.\n" \
           "\n" \
           "추후 지원 예정 기능은\n" \
           " /auto []\n" \
           "입니다.\n"
    context.bot.send_message(id, text)


# 사용자별 로그인처리 필요
def loginEbest(update, context):
    id = update.effective_chat.id
    workerQueue.put((id, LOGIN, context))
    context.bot.send_message(id, "로그인 시도 중")


def getPrice(update, context):
    id = update.effective_chat.id
    text = update.effective_message.text
    priceCode = text.split(' ')
    workerQueue.put((id, PRICE, context, priceCode[1]), context)
    context.bot.send_message(id, priceCode[1] + " 가격 조회 중")


class WuBot:
    def __init__(self):
        self.__updater = Updater(token=token, use_context=True)
        self.__dispatcher = self.__updater.dispatcher

        start_handler = CommandHandler('start', startWUBU)
        self.__dispatcher.add_handler(start_handler)

        help_handler = CommandHandler('help', helpWUBU)
        self.__dispatcher.add_handler(help_handler)

        login_handler = CommandHandler('login', loginEbest)
        self.__dispatcher.add_handler(login_handler)

        price_handler = CommandHandler('price', getPrice)
        self.__dispatcher.add_handler(price_handler)

    def run(self):
        self.__updater.start_polling()


class Worker(threading.Thread):
    def __init__(self):
        super().__init__()
        self.__finance = ebest.Finance()


    def run(self):
        while True:
            #lock
            time.sleep(3)
            if workerQueue.empty():
                print("empty")
                continue
            work = workerQueue.get()

            if work[1] == LOGIN:
                if self.__finance.login() == self.__finance.SUCCESS:
                    self.__finance.kospiLoad()
                    self.__finance.kosdaqLoad()
                    work[2].bot.send_message(work[0], "로그인 성공")
                else:
                    work[2].bot.send_message(work[0], "로그인 실패")
                continue
            elif work[1] == PRICE:
                price = self.__finance.getPrice(work[3])
                if price == self.__finance.ERROR:
                    work[2].bot.send_message(work[0], work[3] + " 조회 실패")
                else:
                    work[2].bot.send_message(work[0], work[3] + " 가격은 " + price + "원 입니다." )
                continue


if __name__ == "__main__":
    worker = Worker()
    worker.start()
    wubot = WuBot()
    wubot.run()