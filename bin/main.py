import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from text import TextRecognizer, TextRecognizerException
from objects import Voice, VideoNote

TOKEN = "TOKEN"
bot = AsyncTeleBot(TOKEN)


async def _get_voice_from_message(message: Message):
    file = await bot.get_file(message.voice.file_id)
    ogg_bytes = await bot.download_file(file.file_path)
    return Voice(ogg_bytes)


async def _recognize_text_in_voice_message(message):
    try:
        voice = await _get_voice_from_message(message)
        return TextRecognizer().in_voice(voice)
    except TextRecognizerException:
        return "Sorry, I cannot recognize text in this message"


@bot.message_handler(commands=["start"])
async def send_welcome_message(message: Message):
    await bot.send_message(
        message.chat.id,
        "Hi! I can recognize text in voice messages. "
        "Just record or forward message and I'll do my work!"
    )


@bot.message_handler(content_types=["voice"])
async def reply_recognized_text_from_voice(message: Message):
    text = await _recognize_text_in_voice_message(message)
    await bot.reply_to(message, text)


def main():
    asyncio.run(bot.polling(non_stop=True))


if __name__ == "__main__":
    main()
