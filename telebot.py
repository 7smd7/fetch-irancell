import time
import telepot
import v1
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

adminID={0000000,9999999}

def getStatus(from_id,case):
    v1.driver.save_screenshot("status.png")
    bot.sendPhoto(from_id,open('status.png','rb'),'staus of %s'%case)

# def ask(lastPM):
#     while(bot.getUpdates()[-1]['message']['text']==lastPM):
#         pass
#     answer=bot.getUpdates()[-1]['message']['text']
#     return answer

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    from_id=msg['from']['id']
    if content_type == "text":
        command = msg['text']
    elif content_type == "contact":
        command = msg['contact']['phone_number']
        print (command)
    elif content_type == "location":
        command = msg['location']
    else:
        command = "nothing"

    if (from_id in adminID):
        if command == '/start':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='login', callback_data='login'), ],
                [InlineKeyboardButton(text='check all user', callback_data='check_alluser'), ],
                [InlineKeyboardButton(text='check self', callback_data='check_self'), ],
                [InlineKeyboardButton(text='change limit', callback_data='changelimit'), ],
                [InlineKeyboardButton(text='change limit for all', callback_data='changelimitforall'), ],
                [InlineKeyboardButton(text='buy', callback_data='buy'), ],
                [InlineKeyboardButton(text='add user', callback_data='add_user'), ],
                [InlineKeyboardButton(text='delete user', callback_data='delete_user'), ],
                [InlineKeyboardButton(text='get status of browser now', callback_data='get_status'), ],                
            ])
            bot.sendMessage(chat_id, 'hello! the user is %s if you want change user, use /change command'%v1.user,reply_markup=keyboard)
        
        if command == '/change':
            bot.sendMessage(chat_id, 'input username')
            # v1.user=ask('/change')
            bot.sendMessage(chat_id, 'input password') 
            # v1.password=ask(v1.user)
            bot.sendMessage(chat_id, 'the user is %d and pass is %s, if is correctly click /start'%(v1.user,v1.password))            

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

    if query_data == 'login':
        bot.answerCallbackQuery(query_id, text='started login')
        v1.login()
        getStatus(from_id,"login")
    elif query_data == 'check_alluser':
        bot.answerCallbackQuery(query_id, text='started checking')        
        v1.check_alluser()
        bot.sendDocument(from_id,open('export.npy','rb'),'numpy of this checking')
    elif query_data == 'check_self':
        bot.answerCallbackQuery(query_id, text='started checking')        
        v1.check_self()
        # asyncio
    elif query_data == 'changelimit':
        bot.sendMessage(from_id, 'input MSISDN')        
        # MSISDN = ask('changelimit')
        # limit = ask(MSISDN)
        v1.changelimit(MSISDN,limit)
    elif query_data == 'changelimitforall':
        bot.sendMessage(from_id, 'send export.npy')
        # bot.download_file
        v1.load()
        v1.changelimitforall()
        bot.answerCallbackQuery(query_id, text='finished changing')        
    elif query_data == 'buy':
        v1.buy()
        bot.answerCallbackQuery(query_id, text='finished buying')                
    # elif query_data == 'add_user':
        # get MSISDN
        # v1.add_user(MSISDN)
    # elif query_data == 'delete_user':
        # get MSISDN
        # v1.delete_user(MSISDN)
    elif query_data == 'get_status':
        getStatus(from_id,"now")

TOKEN = "593559044:AAEJugTRLenYaboMw81ZT1Rtg1rGcfT-tI8"
bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()

while (1):
    time.sleep(1)
