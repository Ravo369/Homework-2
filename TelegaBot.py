import telebot
from config import keys, TOKEN
from extensions import ConvertionException, ValyutaConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Приветствую тебя {message.chat.username}, я бот конвертер валют. "
                                      f"Чтобы перевести валюту введите команду в формате:\n \n "
                                      f"<Имя переводимой валюты> <В какую валюту перевести><Количество первой валюты>\n"
                                      f"Все параметры нужно вводить через пробел\n"
                                      f"Например: Евро Рубль 2\n \n"
                                      f"\nЕсли у вас не целое число валюты вводите его через точку. Например: 1.5 "
                                      f"\nУвидеть список всех доступных валют: /values"
                                      f"\nЧтобы вызвать инструкцию:/start или /help")


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message,  text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:

        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Проверьте количество вводимых параметров')

        quote, base, amount = values
        total_base = ValyutaConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        total_base = float(amount)*total_base
        text = f' {amount} {quote} = {total_base} {base} '
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
