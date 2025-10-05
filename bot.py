from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import VoiceMessagesForbidden

API_ID = 1234567890 # your api_id
API_HASH = "" # your api_hash
BOT_TOKEN = "" # your bot token from @BotFather
ADMIN_ID = 1234567890 # your user id

app = Client("anon_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

user_targets = {}
blocked_users = set()

@app.on_message(filters.command("start"))
async def start_command(client, message):
    if message.from_user.id in blocked_users:
        await message.reply("🚫 Вы заблокированы и не можете отправлять анонимные сообщения.")
        return

    if len(message.command) > 1:
        try:
            target_id = int(message.command[1])
            user_targets[message.from_user.id] = target_id
            await message.reply(
                "✉ Вы можете отправить анонимное сообщение в любом формате:\n\n"
                "📄 Текст\n"
                "🖼 Фото\n"
                "🎬 Видео\n"
                "🎤 Голосовое сообщение\n"
                "📹 Видеокружок\n\n"
                "❌ Чтобы отменить, введите /cancel"
            )

        except ValueError:
            await message.reply("❌ Ошибка! Неверный формат ID.")
    else:
        user_id = message.from_user.id
        bot_link = f"t.me/MessAnonRobot?start={user_id}"

        text = (
            "👋 Привет! Это бот для анонимных сообщений.\n\n"
            "✅ Бесплатно и без рекламы.\n"
            f"🔗 Твоя ссылка для анонимных сообщений: {bot_link}\n\n"
            "Отправь это сообщение кому хочешь, чтобы они могли написать тебе анонимно!"
        )

        await message.reply(text, disable_web_page_preview=True, parse_mode=enums.ParseMode.MARKDOWN)

@app.on_message(filters.command("cancel"))
async def cancel_command(client, message):
    if message.from_user.id in user_targets:
        del user_targets[message.from_user.id]
        await message.reply("❌ Отправка отменена. Вы можете снова воспользоваться ботом.")
    else:
        await message.reply("❌ Нечего отменять, вы не начинали отправку сообщения.")

@app.on_callback_query()
async def handle_reply_callback(client, callback_query):
    data = callback_query.data

    if data.startswith("reply:"):
        target_id = int(data.split(":")[1])
        user_targets[callback_query.from_user.id] = target_id
        await callback_query.message.reply("✏ Введите ваш ответ (он будет отправлен анонимно) или используйте /cancel для отмены.")

@app.on_message(filters.command("block"))
async def block_user(client, message):
    if message.from_user.id != ADMIN_ID:
        return await message.reply("🚫 У вас нет прав использовать эту команду.")

    try:
        user_id = int(message.text.split()[1])
        blocked_users.add(user_id)
        await message.reply(f"✅ Пользователь `{user_id}` заблокирован.")
    except (IndexError, ValueError):
        await message.reply("❌ Используйте формат: `/block USER_ID`.")

@app.on_message(filters.command("unblock"))
async def unblock_user(client, message):
    if message.from_user.id != ADMIN_ID:
        return await message.reply("🚫 У вас нет прав использовать эту команду.")

    try:
        user_id = int(message.text.split()[1])
        if user_id in blocked_users:
            blocked_users.remove(user_id)
            await message.reply(f"✅ Пользователь `{user_id}` разблокирован.")
        else:
            await message.reply(f"ℹ Пользователь `{user_id}` не в списке блокировки.")
    except (IndexError, ValueError):
        await message.reply("❌ Используйте формат: `/unblock USER_ID`.")

@app.on_message(filters.command("blocked"))
async def list_blocked_users(client, message):
    if message.from_user.id != ADMIN_ID:
        return await message.reply("🚫 У вас нет прав использовать эту команду.")

    if blocked_users:
        blocked_list = "\n".join([f"🔹 `{user_id}`" for user_id in blocked_users])
        await message.reply(f"🚫 **Заблокированные пользователи:**\n\n{blocked_list}", parse_mode=enums.ParseMode.MARKDOWN)
    else:
        await message.reply("✅ В списке блокировки нет пользователей.")

@app.on_message(filters.command("idea"))
async def handle_idea(client, message):
    sender = message.from_user
    sender_id = sender.id
    sender_username = f"@{sender.username}" if sender.username else "❌ Нет username"
    sender_name = f"{sender.first_name or ''} {sender.last_name or ''}".strip() or "❌ Нет имени"

    if len(message.command) == 1:
        await message.reply("💡 Вы можете предложить идею для бота!\n\nИспользуйте команду:\n`/idea Ваша идея`", parse_mode=enums.ParseMode.MARKDOWN)
        return

    idea_text = " ".join(message.command[1:])
    idea_message = (
        f"💡 **Новая идея от пользователя!**\n\n"
        f"👤 **Отправитель:**\n"
        f"🔹 ID: `{sender_id}`\n"
        f"🔹 Username: {sender_username}\n"
        f"🔹 Имя: {sender_name}\n\n"
        f"📌 **Идея:**\n"
        f"{idea_text}"
    )

    await client.send_message(ADMIN_ID, idea_message, parse_mode=enums.ParseMode.MARKDOWN)
    await message.reply("✅ Ваша идея отправлена админу! Спасибо за предложение.")

@app.on_message(filters.private & (filters.text | filters.voice | filters.video_note | filters.photo | filters.video))
async def handle_anon_message(client, message):
    try:
        sender = message.from_user
        sender_id = sender.id

        if sender_id in blocked_users:
            await message.reply("🚫 Вы заблокированы и не можете отправлять анонимные сообщения.")
            return

        sender_username = f"@{sender.username}" if sender.username else "❌ Нет username"
        sender_name = f"{sender.first_name or ''} {sender.last_name or ''}".strip() or "❌ Нет имени"

        if sender_id in user_targets:
            target_id = user_targets.pop(sender_id)

            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("Ответить 🔁", callback_data=f"reply:{sender_id}")]
            ])

            if message.text:
                content = f"📩 Анонимное сообщение:\n\n{message.text}"
                await app.send_message(target_id, content, reply_markup=reply_markup)
            elif message.voice:
                content = "🎤 Анонимное голосовое сообщение"
                await app.send_message(target_id, text=content)
                await app.send_voice(target_id, message.voice.file_id, reply_markup=reply_markup)
            elif message.video_note:
                content = "🎥 Анонимный видеокружок"
                await app.send_message(target_id, text=content)
                await app.send_video_note(target_id, message.video_note.file_id, reply_markup=reply_markup)
            elif message.photo:
                content = "🖼 Анонимное изображение"
                await app.send_message(target_id, text=content)
                await app.send_photo(target_id, message.photo.file_id, reply_markup=reply_markup)
            elif message.video:
                content = "🎬 Анонимное видео"
                await app.send_message(target_id, text=content)
                await app.send_video(target_id, message.video.file_id, reply_markup=reply_markup)

            await message.reply("✅ Сообщение отправлено анонимно!")

        else:
            await message.reply("❌ Ошибка: Используйте ссылку с '?start=ID' перед отправкой сообщения.")
    except VoiceMessagesForbidden:
        await app.send_message(target_id, "Вам пытались отправить голосовое сообщения, но из за настроек конфиденциальности сообщение не было отправлено.")
        await app.send_message(sender_id, "К сожалению из за настроек конфиденциальности получателя голосовое сообщение не было отправлено.")

app.run()
