import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler
import json
from convex import ConvexClient
import os
import time

# Включаем логирование для отладки
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Этапы сбора данных
PHONE_NUMBER, MESSAGE = range(2)

# Convex URL из файла .env.local
CONVEX_URL = "https://posh-bloodhound-202.convex.cloud"
logger.info(f"Используем Convex URL: {CONVEX_URL}")
convex_client = ConvexClient(CONVEX_URL)

# Функция для сохранения данных в базу данных Convex
def save_message_to_convex(message_data):
    logger.info("Saving message to Convex...")
    try:
        # Отправляем только те поля, которые определены в схеме Convex
        convex_data = {
            "text": message_data.get("text", ""),
            "timestamp": message_data.get("timestamp", int(time.time() * 1000)),
            "userId": message_data.get("userId", ""),
            "username": message_data.get("username", "")
        }
        
        logger.info(f"Sending data to Convex: {convex_data}")
        # Используем mutation для сохранения данных
        result = convex_client.mutation("messages:save", convex_data)
        logger.info(f"Message saved to Convex! Result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error while saving message to Convex: {e}")
        logger.error(f"Error details: {str(e)}")
        return None

# Функция начала разговора
async def start(update: Update, context: CallbackContext):
    logger.info(f"Received /start command from {update.message.from_user.id}")
    user = update.message.from_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! Я собираю информацию для тебя. Пожалуйста, поделись своим номером телефона."
    )
    # Кнопка для запроса контакта
    phone_button = KeyboardButton(text="Поделиться номером", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[phone_button]], one_time_keyboard=True)
    await update.message.reply_text("Нажми кнопку, чтобы поделиться своим номером телефона.", reply_markup=reply_markup)
    return PHONE_NUMBER

# Функция для получения номера телефона
async def get_phone_number(update: Update, context: CallbackContext):
    logger.info(f"Received phone number from {update.message.from_user.id}")
    user = update.message.from_user

    # Получаем номер телефона только из контакта
    if update.message.contact:
        phone_number = update.message.contact.phone_number
        
        # Собираем данные о пользователе
        username = user.username or "Не указано"
        user_id = str(user.id)

        # Создаем структуру данных для записи в базу
        message_data = {
            "text": "",  # Будет заполнено позже
            "timestamp": int(time.time() * 1000),
            "userId": user_id,
            "username": username
        }

        # Сохраняем данные в контекст для использования в следующем шаге
        context.user_data["message_data"] = message_data

        # Запрашиваем текст сообщения
        await update.message.reply_text("Спасибо! Теперь напиши сообщение, которое ты хочешь отправить.")
        return MESSAGE
    else:
        # Если пользователь не поделился контактом через кнопку
        phone_button = KeyboardButton(text="Поделиться номером", request_contact=True)
        reply_markup = ReplyKeyboardMarkup([[phone_button]], one_time_keyboard=True)
        await update.message.reply_text(
            "Пожалуйста, поделитесь номером телефона, используя специальную кнопку ниже.",
            reply_markup=reply_markup
        )
        return PHONE_NUMBER

# Функция для получения текста сообщения
async def get_message(update: Update, context: CallbackContext):
    logger.info(f"Received message text from {update.message.from_user.id}")
    user = update.message.from_user
    
    # Получаем предыдущие данные из контекста
    message_data = context.user_data.get("message_data", {})
    
    # Обновляем текст сообщения
    message_data["text"] = update.message.text
    message_data["timestamp"] = int(time.time() * 1000)
    
    # Сохраняем данные в Convex
    save_message_to_convex(message_data)

    await update.message.reply_text("Спасибо! Ваши данные сохранены.")
    return ConversationHandler.END

# Функция отмены
async def cancel(update: Update, context: CallbackContext):
    logger.info(f"Conversation canceled by {update.message.from_user.id}")
    await update.message.reply_text("Процесс был отменен.")
    return ConversationHandler.END

# Главная функция
def main():
    # Вставь свой токен API бота
    application = Application.builder().token("8003548077:AAG4KJ711-l25VppqsKeKolRXWw5FnbaKfw").build()

    # Настройка ConversationHandler
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],

        # Этапы
        states={
            PHONE_NUMBER: [
                MessageHandler(filters.CONTACT, get_phone_number),
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone_number)
            ],
            MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_message)],
        },

        # Если пользователь отменит разговор
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conversation_handler)

    # Запуск бота
    logger.info("Starting bot...")
    application.run_polling()

# Запуск
if __name__ == '__main__':
    main()
