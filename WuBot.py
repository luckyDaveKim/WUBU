from telegram.ext import Updater
from telegram.ext import CommandHandler

token = input()

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher


def startWUBU(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="hello world!")


def helpWUBU(update, context):
    id = update.effective_chat.id
    text = "안녕하세요. WUBUBOT 입니다.\n" \
           "현재 지원하는 기능은 \n" \
           " /price [종목 코드] or [종목 명]\n" \
           "입니다.\n" \
           "\n" \
           "추후 지원 예정 기능은\n" \
           " /auto []\n" \
           "입니다.\n"
    context.bot.send_message(id, text)


start_handler = CommandHandler('start', startWUBU)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', helpWUBU)
dispatcher.add_handler(help_handler)

updater.start_polling()
