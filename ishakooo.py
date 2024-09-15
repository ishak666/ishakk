import telebot
import requests
import time

# Bot token
bot = telebot.TeleBot('7464971830:AAEjnS9J5sQSUhTFdyTiYO-NXUx3pEPk--s')

@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.text.startswith('/start'):
        bot.send_message(message.chat.id, ' ارسل رقم الهاتف خاص بك اخي الكريم:')
        bot.register_next_step_handler(message, get_phone_number)
    elif message.text.startswith('/reset'):
        reset_bot(message)
    else:
        bot.send_message(message.chat.id, 'Invalid command. Please start with /start or /reset')

def reset_bot(message):
    bot.send_message(message.chat.id, 'Bot has been reset.')
    # Add any code here to clean up or reset the bot's state

def get_phone_number(message):
    num = message.text
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'ibiza.ooredoo.dz',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/4.9.3',
    }

    data = {
        'client_id': 'ibiza-app',
        'grant_type': 'password',
        'mobile-number': num,
        'language': 'AR',
    }

    response = requests.post('https://ibiza.ooredoo.dz/auth/realms/ibiza/protocol/openid-connect/token', headers=headers, data=data)

    if 'ROOGY' in response.text:
        bot.send_message(message.chat.id, 'تم ارسال رمز قم بإرساله هنا📲:')
        bot.register_next_step_handler(message, get_otp, num)
    else:
        bot.send_message(message.chat.id, 'خطا اعد المحاولة.')

def get_otp(message, num):
    otp = message.text
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'ibiza.ooredoo.dz',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/4.9.3',
    }

    data = {
        'client_id': 'ibiza-app',
        'otp': otp,
        'grant_type': 'password',
        'mobile-number': num,
        'language': 'AR',
    }

    response = requests.post('https://ibiza.ooredoo.dz/auth/realms/ibiza/protocol/openid-connect/token', headers=headers, data=data)
    
    access_token = response.json().get('access_token')
    if access_token:
        url = 'https://ibiza.ooredoo.dz/api/v1/mobile-bff/users/mgm/info/apply'

        headers = {
            'Authorization': f'Bearer {access_token}',
            'language': 'AR',
            'request-id': 'ef69f4c6-2ead-4b93-95df-106ef37feefd',
            'flavour-type': 'gms',
            'Content-Type': 'application/json'
        }

        payload = {
            "mgmValue": "ABC"  
        }

        counter = 0
        while counter < 12:
            response = requests.post(url, headers=headers, json=payload)
            
            if 'EU1002' in response.text:
                bot.send_message(message.chat.id, 'تم تسجيلك بنجاح قم بمشاركة البوت شكرا    ')
            else:
                bot.send_message(message.chat.id, 'تأكد من الانترنت وعد لاحقا 🦊 ....')

            counter += 1
            time.sleep(0)

    else:
        bot.send_message(message.chat.id, 'Error verifying OTP.')

bot.polling(none_stop=True)