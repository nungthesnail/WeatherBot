import telebot
import weather
import log


bot = telebot.TeleBot("BOT TOKEN HERE")


@bot.message_handler(content_types=["text"])
def handle_text_message(message):
    log.log(f"Incoming text message: {message.text}")
    msg = message.text.split(" ")
    response = ""

    try:
        if msg[:2] == ["Узнать", "погоду"]:
            tmp = weather.get_weather_by_city(msg[2].lower())
            if not tmp:
                bot.send_message(
                    message.from_user.id, text="Увы, мы не смогли запросить погоду")
                return

            response = f"Погода в городе {msg[2].capitalize()} сейчас:"
            response += "\nТемпература: " + (
                str(tmp.temperature) if tmp.temperature else "Нет данных")
            response += "\nПогодные условия: " + (
                str(tmp.condition) if tmp.condition else "Нет данных")
            response += "\nКоординаты места: " + str(tmp.coordinates)
            response += "\n\nПрогноз погоды предоставлен ventusky.com"
        else:
            response += "Увы, я не знаю такой команды"
    except (ValueError, IndexError):
        response = "В команде содержится ошибка"

    bot.send_message(message.from_user.id, text=response)
    log.log(f"Response: {response}")


bot.polling(none_stop=True, interval=0)
